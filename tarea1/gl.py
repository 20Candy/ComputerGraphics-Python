from utils import *


class Gl(object):

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

    def glCreateWindow(self,width,height):

        if (width < 0) or (height < 0):
            raise Exception('unexpected windows size')

        self.width = width
        self.height = height

        self.glClear()


    def glViewPort(self, x, y, width, height):
        if (width > self.width) or (height > self.height):
            raise Exception('Viewport larger than window')

        self.OffsetX = x 
        self.OffsetY = y 

        self.ImageHeight = height
        self.ImageWidth = width
      

    def glVertex(self, x, y):
        if not (-1 <= x <= 1) or not (-1 <= y <= 1):
            raise Exception('unexpected vertex offset')

        x0 = int(self.OffsetX + (self.ImageWidth/2) + (x*self.ImageWidth/2))
        y0 = int(self.OffsetY+ (self.ImageHeight/2) + (y*self.ImageHeight/2))

        self.pixels[x0][y0] = self.color

    def glClear(self):
        self.pixels = [
            [self.clean_color for x in range(self.width)] 
            for y in range(self.height)
            ]

    def glClearColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected color value')
        
        self.clean_color = color(int(r * 255), int(g * 255), int(b * 255))

    def glColor(self, r, g, b):
        if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
            raise Exception('unexpected value for color')
        
        self.color  = color(int(r * 255), int(g * 255), int(b * 255))

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


