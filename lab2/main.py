from library.gl import Renderer
from library.texture import Texture
from library.vector import *

r = Renderer()
r.glInit()
r.glCreateWindow(1000, 1000)
r.glViewPort(0, 0, 1000, 1000)

r.lookAt(V3(0,-9,50),V3(0,0,0),V3(0,1,10))

# t = Texture('./models/bench.bmp')
# r.load('./models/bench.obj',(0, -2, 0), (0.2, 0.2, 0.1),(1, 0, 0), texture=t)

# t = Texture('./models/lamp.bmp')
# r.load('./models/lamp.obj',(-2.5, -2, 0), (0.02, 0.02, 0.02),(0, 0, 0), texture=t)

# t = Texture('./models/hollow.bmp')
# r.load('./models/hollow.obj',(-1.5, -2.2, 0), (0.25, 0.25, 0.8),(0, 0.5, 0), texture=t)

# t = Texture('./models/hornet.bmp')
# r.load('./models/hornet.obj',(-0.5, -2.2, 0), (0.15, 0.15, 0.5),(0, -0.5, 0), texture=t)


r.stars()

r.load('./models/ring.obj',(-1, -1, 0), (1, 1, 1),(0,0,0), shader = "ring")
r.load('./models/sphere.obj',(-1, -1, 0), (1.2, 1.2, 1.5),(0, 0, 0), shader = "sphere")

r.glFinish()
