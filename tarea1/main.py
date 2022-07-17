from gl import Gl

def point():

    render = Gl()

    render.glInit()
    render.glCreateWindow(100,100)
    render.glViewPort(5,5,90,90)   #90x90 => x = 90+5+5 = 100, y = 90+5+5 = 100

    render.glColor(0.8,0.1,0.9)  

    render.glVertex(1,1)
    render.glFinish()

point()
