from gl import Renderer

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(1000, 1000)
r.glViewPort(0, 0, 1000, 1000)

r.glLoad('./models/hollowknight.obj', (0, -1.3), (0.45, 0.45))

r.glFinish()