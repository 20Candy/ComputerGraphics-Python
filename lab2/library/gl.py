import random
from library.obj import Obj
from library.utils import *
from library.vector import *
from library.matrix import *
from numpy import sin, cos
from math import sqrt 

BLACK = 0, 0, 0
MELON = 222, 195, 136
BROWN = 170,145,105
LAVENDER = 164, 152, 156

class Renderer(object):

    def glInit(self):
        self.color = color(50, 50, 50)
        self.clean_color = color(0, 0, 0)
        self.filename = 'result.bmp'
        self.pixels = [[]]
        self.zbuffer = [[]]
        self.light = V3(0, 0, 1)

        self.width = 0
        self.height = 0

        self.OffsetX = 0
        self.OffsetY = 0
        self.ImageHeight = 0
        self.ImageWidth = 0

        self.View = None

    def glClear(self):
        self.pixels = [
            [self.clean_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zbuffer = [
            [-99999 for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected color value')

        self.clean_color = color(int(r * 255), int(g * 255), int(b * 255))

    def glColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected color value')

        self.current_color = color(int(r * 255), int(g * 255), int(b * 255))

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()

    def glViewPort(self, x, y, width, height):

        if (width > self.width) or (height > self.height):
            raise Exception('Viewport larger than window')

        self.OffsetX = int(x)
        self.OffsetY = int(y)

        self.ImageWidth = int(width)
        self.ImageHeight = int(height)

    def glVertex(self, x, y):
        if not (-1 <= x <= 1) or not (-1 <= y <= 1):
            raise Exception('unexpected vertex offset')

        x = int((x+1)*(self.ImageWidth/2)+self.OffsetX)
        y = int((y+1)*(self.ImageHeight/2)+self.OffsetY)

        self.pixels[y-1][x-1] = self.current_color

    def glFinish(self):
        f = open(self.filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

    def glPoint(self, x, y):
        if not (-1 <= x <= 1) or not (-1 <= y <= 1):

            raise Exception('unexpected value')

        self.glVertex(x, y)

    def glLine(self, x0, y0, x1, y1):
        x0 = int((x0+1)*(self.ImageWidth/2)+self.OffsetX)
        y0 = int((y0+1)*(self.ImageHeight/2)+self.OffsetY)
        x1 = int((x1+1)*(self.ImageWidth/2)+self.OffsetX)
        y1 = int((y1+1)*(self.ImageHeight/2)+self.OffsetY)
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            dy = abs(y1 - y0)
            dx = abs(x1 - x0)

        offset = 0 * 2 * dx
        threshold = 0.5 * 2 * dx
        y = y0

        points = []
        for x in range(x0, x1):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx

        for point in points:
            self.glPoint(((point[0]-self.OffsetX)*(2/self.ImageWidth)-1),
                         ((point[1]-self.OffsetY)*(2/self.ImageHeight)-1))

    def transform(self, vertex):
        augmentedVertex = V4(vertex[0], vertex[1], vertex[2], 1)

        matrix1 = product_matrix_vector(self.model, augmentedVertex)
        matrix2 = product_matrix_vector(self.View,matrix1)
        matrix3 = product_matrix_vector(self.Projection,matrix2)
        transformedVertex = product_matrix_vector(self.Viewport,matrix3)

        transformedVertex = V4(*transformedVertex)

        return V3(
            transformedVertex.x / transformedVertex.w,
            transformedVertex.y / transformedVertex.w,
            transformedVertex.z / transformedVertex.w
        )

    def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1),rotate = (0, 0, 0), texture=None, shader = None):
        model = Obj(filename)
        self.loadMatrix(translate, scale, rotate)
        self.active_texture = texture
        self.active_shader = shader

        light = V3(0, 0, 1)

        for face in model.faces:
            vcount = len(face)

            if vcount == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                a = self.transform(model.vertices[f1])
                b = self.transform(model.vertices[f2])
                c = self.transform(model.vertices[f3])

                normal = norm(cross(sub(b, a), sub(c, a)))
                intensity = dot(normal, light)

                if not texture:
                    grey = round(255 * intensity)
                    if grey < 0:
                        continue
                    self.triangle(a, b, c, texture=texture, texture_coords=(0, 0, 0), texture_n= (0,0,0), intensity=intensity)
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1

                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])

                    tn1 = face[0][2] - 1
                    tn2 = face[1][2] - 1
                    tn3 = face[2][2] - 1
                    
                    tnA = V3(*model.nvertices[tn1])
                    tnB = V3(*model.nvertices[tn2])
                    tnC = V3(*model.nvertices[tn3])

                    self.triangle(a, b, c, texture=texture, texture_coords=(tA, tB, tC), texture_n= (tnA,tnB,tnC), intensity=intensity)
            else:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                vertices = [
                    self.transform(model.vertices[f1]),
                    self.transform(model.vertices[f2]),
                    self.transform(model.vertices[f3]),
                    self.transform(model.vertices[f4])
                ]

                normal = norm(cross(sub(vertices[0], vertices[1]), sub(
                    vertices[1], vertices[2])))  
                intensity = dot(normal, light)
                grey = round(255 * intensity)

                A, B, C, D = vertices
                
                if not texture:
                    grey = round(255 * intensity)
                    if grey < 0:
                        continue
                    self.triangle(A, B, C, color(grey, grey, grey))
                    self.triangle(A, C, D, color(grey, grey, grey))            
                else:
                    t1 = face[0][1] - 1
                    t2 = face[1][1] - 1
                    t3 = face[2][1] - 1
                    t4 = face[3][1] - 1
                    tA = V3(*model.tvertices[t1])
                    tB = V3(*model.tvertices[t2])
                    tC = V3(*model.tvertices[t3])
                    tD = V3(*model.tvertices[t4])

                    tn1 = face[0][2] - 1
                    tn2 = face[1][2] - 1
                    tn3 = face[2][2] - 1
                    tn4 = face[3][2] - 1
                    
                    tnA = V3(*model.nvertices[tn1])
                    tnB = V3(*model.nvertices[tn2])
                    tnC = V3(*model.nvertices[tn3])
                    tnD = V3(*model.nvertices[tn4])
                    
                    self.triangle(A, B, C, texture=texture, texture_coords=(tA, tB, tC), texture_n= (tnA,tnB,tnC), intensity=intensity)
                    self.triangle(A, C, D, texture=texture, texture_coords=(tA, tC, tD), texture_n= (tnA,tnC,tnD), intensity=intensity)

    def triangle(self, A, B, C, color=None, texture=None, texture_coords=(),texture_n= (), intensity=1):
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = V2(x, y)
                w, u, v = barycentric(A, B, C, P)

                if w < 0 or v < 0 or u < 0:
                    continue

                tA, tB, tC = texture_coords
                tnA, tnB, tnC = texture_n

                z = A.z * w + B.z * v + C.z * u

                tempx = int(((x/self.width)+1) *
                            (self.ImageWidth/2)+self.OffsetX)
                tempy = int(((y/self.height)+1) *
                            (self.ImageHeight/2)+self.OffsetY)


                if z > self.zbuffer[tempx][tempy]:

                    self.current_color = self.shader(
                        self, 
                        bar=(w,u,v),
                        light = self.light,
                        vertices = (A, B, C),
                        texture_coords = (tA,tB,tC), 
                        normals= (tnA,tnB,tnC),
                        coords= (x,y),
                    )
                    
                    self.glVertex(x/self.width, y/self.height)
                    self.zbuffer[tempx][tempy] = z


    def showZbuffer(self):
        # Prints the pixels to the screen
        f = open('result.bmp', 'bw')

        # File header (14 bytes)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bytes)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for y in range(0, self.height-1):
            for x in range(0, self.width):

                try:

                    toWrite = color(
                        self.zbuffer[x][y], self.zbuffer[x][y], self.zbuffer[x][y])

                except:
                    toWrite = color(0, 0, 0)

                f.write(toWrite)

        f.close()

    def loadMatrix(self, translate = (0, 0, 0), scale = (1, 1, 1), rotate = (0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translateMatrix = [
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
        ]

        scaleMatrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ]

        rotateXMatrix = [
            [1, 0, 0, 0],
            [0, cos(rotate.x), -sin(rotate.x), 0],
            [0, sin(rotate.x), cos(rotate.x), 0],
            [0, 0, 0, 1]
        ]

        rotateYMatrix = [
            [cos(rotate.y), 0, sin(rotate.y), 0],
            [0, 1, 0, 0],
            [-sin(rotate.y), 0, cos(rotate.y), 0],
            [0, 0, 0, 1]
        ]

        rotateZMatrix = [
            [cos(rotate.z), -sin(rotate.z), 0, 0],
            [sin(rotate.z), cos(rotate.z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        rotateMatrix = product_matrix(product_matrix(rotateYMatrix,rotateZMatrix),rotateZMatrix)
        self.model = product_matrix(product_matrix(translateMatrix,scaleMatrix),rotateMatrix)

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1 / length(sub(eye, center)))
        self.loadViewportMatrix()


    def loadViewMatrix(self, x, y, z, center):
        Mi = [
            [x.x, x.y, x.z,  0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0,     0,   0, 1]
        ]

        Op = [
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]
        ]

        self.View = product_matrix(Mi,Op)


    def loadProjectionMatrix(self, coeff):
        self.Projection =  [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]
        ]

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport =  [
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]
        ]

    def radius(self,x,y):
        return int(sqrt(x*x + y*y))

    def check_ellipse(self, x, y, a, b):
        return round((x ** 2) * (b ** 2)) + ((y ** 2) * (a ** 2)) <= round(a ** 2) * (
            b ** 2
        )

    def stars(self):
        
        for i in range(1000):
            self.current_color = color(255, 255, 255)

            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            self.glVertex(x,y)
            
            


    def shader(self, render, **kwargs):
        w, u, v = kwargs['bar']
        L = kwargs['light']
        A, B, C = kwargs['vertices']
        tA, tB, tC = kwargs['texture_coords']
        nA, nB, nC = kwargs['normals']
        x, y = kwargs['coords']

        if render.active_texture:

            nx = nA.x * w + nB.x * u + nC.x * v
            ny = nA.y * w + nB.y * u + nC.y * v
            nz = nA.z * w + nB.z * u + nC.z * v

            i = dot(norm(V3(nx,ny,nz)),L)

            tx = tA.x * w + tB.x * u + tC.x * v
            ty = tA.y * w + tB.y * u + tC.y * v

            return render.active_texture.get_color_with_intensity(tx, ty, i)

        else :
            shader_color = BLACK
            r1, g1, b1 = BLACK
            r2, g2, b2 = BLACK
            percentage = 1
            r,g,b = BLACK


            if(render.active_shader == "ring"):

                # Filling from inside to outside
                x0, y0 = x +10 , y + 10
                a, b = 600, 50

                # First ellipse
                is_ellipse = self.check_ellipse(x0, y0, a, b)
                if is_ellipse:
                    r,g,b = BROWN
                else:
                    # Second ellipse
                    a += 70
                    b += 5
                    is_ellipse = self.check_ellipse(x0, y0, a, b)
                    if is_ellipse:
                        r,g,b =  180, 161, 145
                    else:
                        # Third ellipse
                        a += 8
                        b += 5
                        is_ellipse = self.check_ellipse(x0, y0, a, b)
                        if is_ellipse:
                            r,g,b = 0, 0, 0
                        else:
                            # Fourth ellipse
                            a += 65
                            b += 10
                            is_ellipse = self.check_ellipse(x0, y0, a, b)
                            if is_ellipse:
                                r,g,b = BLACK
                            else:
                                # Fifth ellipse
                                a += 8
                                b += 5
                                is_ellipse = self.check_ellipse(x0, y0, a, b)
                                if is_ellipse:
                                    r,g,b = 0, 0, 0
                                else:
                                    r,g,b = 196, 170, 117

                return(color(r,g,b))

            if(render.active_shader == "sphere"):

                if y < 0 and y <= 80:
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - (-50))

                if y < 80 or y >= 120:
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - (-150))

                if (y < -120 and y >= -170):
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - (-200))

                if (y < -170 and y >= -220):
                    r1, g1, b1 = BROWN
                    r2, g2, b2 = LAVENDER
                    percentage = abs(y - (-200))

                if (y < -220):
                    r1, g1, b1 = LAVENDER
                    r2, g2, b2 = LAVENDER
                    percentage = abs(y - (-150))


                if y >= 0 and y <= 80:
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - 150)

                if (y > 80 and y < 120):
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - 150)

                if (y >= 120 and y < 170):
                    r1, g1, b1 = MELON
                    r2, g2, b2 = BROWN
                    percentage = abs(y - 150)

                if (y >= 170 and y < 220):
                    r1, g1, b1 = BROWN
                    r2, g2, b2 = LAVENDER
                    percentage = abs(y - 200)

                if (y >= 220):
                    r1, g1, b1 = LAVENDER
                    r2, g2, b2 = LAVENDER
                    percentage = abs(y - 150)


                # Gradient Function
                percentage = (percentage / 50)
                r = r1 + percentage * (r2 - r1)
                g = g1 + percentage * (g2 - g1)
                b = b1 + percentage * (b2 - b1)
                shader_color = r, g, b

                # Saturn gradient lines
                if (y % 40) in range(0, 14):
                    r, g, b = shader_color
                    r *= 0.98
                    g *= 0.98
                    b *= 0.98
                    shader_color = r, g, b

                return color(r, g, b)




