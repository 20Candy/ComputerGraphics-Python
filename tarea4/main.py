from gl import Renderer

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(800, 800)
r.glViewPort(0, 0, 800, 800)

r.load('./models/o.obj', (0, -50, 0), (10, 10, 10))

r.glFinish()
r.showZbuffer()
