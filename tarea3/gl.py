from utils import *
from obj import Obj

class Renderer(object):

    def glInit(self):
        self.color = color(250,250,250)
        self.clean_color = color(0,0,0)
        self.filename = 'result.bmp'
        self.pixels = [[]]

        self.width = 0
        self.height = 0
        
        self.OffsetX = 0
        self.OffsetY = 0
        self.ImageHeight = 0
        self.ImageWidth = 0

    def glClear(self):
        self.pixels = [
        [self.clean_color for x in range(self.width)]
        for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected color value')

        self.clean_color =  color(int(r * 255), int(g * 255), int(b * 255))

    def glColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected color value')

        self.current_color =  color(int(r * 255), int(g * 255), int(b * 255))

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

        x = int( (x+1)*(self.ImageWidth/2)+self.OffsetX )
        y = int( (y+1)*(self.ImageHeight/2)+self.OffsetY )

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
        if not (-1 <= x <= 1) or not (-1<= y <= 1):
            raise Exception('unexpected value')
        
        self.glVertex(x,y)

    def glLine(self, x0, y0, x1, y1):
        x0 = int( (x0+1)*(self.ImageWidth/2)+self.OffsetX )
        y0 = int( (y0+1)*(self.ImageHeight/2)+self.OffsetY )
        x1 = int( (x1+1)*(self.ImageWidth/2)+self.OffsetX )
        y1 = int( (y1+1)*(self.ImageHeight/2)+self.OffsetY )
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx
        if x1 < x0:
            t,t1 = x0,y0
            x0, y0 = x1, y1
            x1, y1 = t, t1
        
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
            self.glPoint(((point[0]-self.OffsetX)*(2/self.ImageWidth)-1), ((point[1]-self.OffsetY)*(2/self.ImageHeight)-1))

    def glLoad(self, filename, translate, scale):
        model = Obj(filename)
        
        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                
                x1 = round((v1[0] + translate[0]) * scale[0])
                y1 = round((v1[1] + translate[1]) * scale[1])
                x2 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])

                self.line((x1, y1), (x2, y2))

    


  

