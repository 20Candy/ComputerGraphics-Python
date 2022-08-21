from gl import Renderer
from obj import Texture

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(500, 500)
r.glViewPort(0, 0, 500, 500)

t = Texture('./models/figura.bmp')
r.load('./models/figura.obj',(0, -4, 0), (130, 130, 130), texture=t)
r.glFinish()
