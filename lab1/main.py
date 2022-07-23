from gl import Renderer

r = Renderer()
r.glInit()
r.glColor(1, 1, 1)
r.glClearColor(0, 0, 0)
r.glCreateWindow(1000, 500)
r.glViewPort(0, 0, 1000, 500)

r.glColor(1, 1, 1)
r.glPoligon('lab1/poligons/figura1.txt')
r.glFill('lab1/poligons/figura1.txt')

r.glPoligon('lab1/poligons/figura2.txt')
r.glFill('lab1/poligons/figura2.txt')

r.glPoligon('lab1/poligons/figura3.txt')
r.glFill('lab1/poligons/figura3.txt')

r.glPoligon('lab1/poligons/figura4.txt')
r.glFill('lab1/poligons/figura4.txt')

r.glPoligon('lab1/poligons/figura5.txt')
r.glFill('lab1/poligons/figura5.txt')

r.glFinish()