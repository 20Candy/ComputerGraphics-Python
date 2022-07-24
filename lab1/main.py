from gl import Renderer

r = Renderer()
r.glInit()
r.glClearColor(0, 0, 0)
r.glCreateWindow(1000, 500)
r.glViewPort(0, 0, 1000, 500)

r.glColor(1, 1, 0)
r.glPoligon('lab1/poligons/figura1.txt')
r.glFill('lab1/poligons/figura1.txt')

r.glColor(0, 0, 1)
r.glPoligon('lab1/poligons/figura2.txt')
r.glFill('lab1/poligons/figura2.txt')

r.glColor(0.5, 0, 0.5)
r.glPoligon('lab1/poligons/figura4.txt')
r.glFill('lab1/poligons/figura4.txt')

r.glColor(0, 0, 0)
r.glPoligon('lab1/poligons/figura5.txt')
r.glFill('lab1/poligons/figura5.txt')

r.glColor(1, 0, 0)
r.glPoligon('lab1/poligons/figura3.txt')
r.glFill('lab1/poligons/figura3.txt')

r.glFinish()