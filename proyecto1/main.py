from library.gl import Renderer
from library.texture import Texture
from library.vector import *

r = Renderer()
r.glInit()
r.glCreateWindow(1000, 1000)
r.glViewPort(0, 0, 1000, 1000)

r.lookAt(V3(0,0,50),V3(0,0,0),V3(0,1,1))

background = Texture('./models/background.bmp')
r.pixels = background.pixels

t = Texture('./models/lamp2.bmp')
r.load('./models/lamp2.obj',(-2.4, -2.75, 0), (1.2, 1.2, 1),(0, 0, 0), texture=t)

t = Texture('./models/bench2.bmp')
n = Texture('./models/normal_bench.bmp')
r.load('./models/bench2.obj',(-0.9, -2.15, 0), (0.007, 0.007, 0.0001),(0, 1.5, 0), texture=t)

t = Texture('./models/hollow.bmp')
r.load('./models/hollow.obj',(-1.4, -3, 0), (0.25, 0.25, 1),(0, 0.5, 0), texture=t)

t = Texture('./models/hornet.bmp')
r.load('./models/hornet.obj',(-0.4, -2.8, 0), (0.13, 0.13, 1.8),(0, -0.6, 0), texture=t)

t = Texture('./models/espada.bmp')
n = Texture('./models/normal.bmp')
r.load('./models/espada.obj',(-2.1, -1.5, 0), (0.12, 0.12, 0.12),(0, 0, 1.9), texture=t)

r.glFinish()
