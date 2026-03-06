from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

INSIDE = 0 # 0000
LEFT = 1 # 0001
RIGHT = 2 # 0010
BOTTOM = 4 # 0100
TOP = 8 # 1000

left, right, bottom, top = -4, 4, -4, 4

#Rectangle
xmin, ymin = -2, -1.2
xmax, ymax = 2, 1.2

#Line points
x1, y1, = -1.3, 1.5
x2,  y2 = 2.7, -1 

x1_Original, y1_Original = x1, y1
x2_Original, y2_Original = x2, y2


draw= True
drawInside = False
drawOutside = False

r1,g1,b1 = 1.0, 0.0, 0.0
r2,g2,b2 = 1.0, 0.0, 0.0

def InitGL():
    glClearColor(1.,1.,1.,0.) 
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 
    gluOrtho2D(left, right, bottom, top)
    

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    
    if draw:
        glColor3f(r1, g1, b1)
        glBegin(GL_LINES)
        glVertex2f(x1_Original, y1_Original)
        glVertex2f(x2_Original, y2_Original)
        glEnd()
        

    if(x1_Original != x1):
        glColor3f(r2, g2, b2)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()
        
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(xmin, ymin)
    glVertex2f(xmin, ymax)
    glVertex2f(xmax, ymax)  
    glVertex2f(xmax, ymin)
    glEnd()
    glPopMatrix()
    
    glFlush()
    return
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b'Line CLipping')
    InitGL()
    glutDisplayFunc(display)
    glutKeyboardFunc(On_Keyboard)
    glutMainLoop()
    return

def On_Keyboard(key, x, y):
    global drawOutside, drawInside
    global r1,g1,b1,r2,g2,b2
    if(key == b'1'):
        
        r1,g1,b1 = 1.0, 0.0, 0.0
        r2,g2,b2 = 1.0, 1.0, 1.0
        ClipLine()
    if(key == b'2'):
        r1,g1,b1 = 1.0, 1.0, 1.0
        r2,g2,b2 = 1.0, 0.0, 0.0
        ClipLine()
    glutPostRedisplay()

def encode(x, y):
    code = INSIDE
    if(x < xmin):
        code |= LEFT
    elif (x > xmax):
        code |= RIGHT
    if (y < ymin):
        code |= BOTTOM
    elif (y > ymax):
        code |= TOP
    
    return code

def ClipLine():
    global draw
    global x1, x2, y1, y2
    global x1_Original, x2_Original, y1_Original, y2_Original
    
    while(True): #not drawing if both points are outside
        code1 = encode(x1, y1)
        code2 = encode(x2, y2)
        if not(code1 | code2):
            draw = True
            break
        elif (code1 & code2):
            draw = False
            break
        else:
            if not(code1):
                x1, y1, x2, y2 = x2, y2, x1, y1
                x1_Original, y1_Original, x2_Original, y2_Original = x2_Original, y2_Original, x1_Original, y1_Original
                code1, code2 = code2, code1
            
            if code1 & TOP: 
                x1 = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1) 
                y1 = ymax 
            elif code1 & BOTTOM: 
                x1 = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1) 
                y1 = ymin 
            elif code1 & RIGHT: 
                y1 = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1) 
                x1 = xmax 
            elif code1 & LEFT: 
                y1 = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1) 
                x1 = xmin
    return 

if __name__ == '__main__': main()