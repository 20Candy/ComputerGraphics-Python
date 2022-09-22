import struct 
from library.utils import *

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4) 
        header_size = struct.unpack("=l", image.read(4))[0]  
        image.seek(2 + 4 + 4 + 4 + 4)
        
        self.width = struct.unpack("=l", image.read(4))[0]  
        self.height = struct.unpack("=l", image.read(4))[0]  
        self.pixels = []
        image.seek(header_size)
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                
                self.pixels[y].append(color(r,g,b))
        image.close()

    def get_color(self, tx, ty):
        x = int(tx * self.width)
        y = int(ty * self.height)
        
        return self.pixels[y][x]

    def get_color_with_intensity(self, tx, ty, intensity=1):
        x = round(tx * self.width)
        y = round(ty * self.height)


        int_values = [temp for temp in (self.pixels[y][x])]

        b = round(int_values[0] * intensity)
        g = round(int_values[1] * intensity)
        r = round(int_values[2] * intensity)

        if(r<0):
            r = 0

        if(g<0):
            g = 0

        if(b<0):
            b = 0

        return color(r,g,b)
    
    
