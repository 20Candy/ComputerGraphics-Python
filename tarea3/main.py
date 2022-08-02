from gl import Renderer

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(500, 500)
r.glViewPort(0, 0, 500, 500)

r.glLoad('./models/hollowknight.obj', (4, 3), (1000, 1000))

r.glFinish()