from library.gl import Renderer
from library.texture import Texture
from library.vector import *

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(500, 500)
r.glViewPort(0, 0, 500, 500)

r.lookAt(V3(0,0,10),V3(0,0,0),V3(0,1,1))
t = Texture('./models/figura.bmp')
r.load('./models/figura.obj',(-1, -3, 0), (0.5, 0.5, 0.5),(0, 0, 0), texture=t)
r.glFinish()
