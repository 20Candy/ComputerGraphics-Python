from gl import Renderer

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(300, 300)
r.glViewPort(100, 100, 100, 100)

r.glLine(-1, -1, 0.5, 0.5)
r.glLine( -1, 1, 0.5, 0.5)
r.glLine( -0.5, 0.5, 1, -1)
r.glLine(-1, 0, 1, 0)
r.glFinish()