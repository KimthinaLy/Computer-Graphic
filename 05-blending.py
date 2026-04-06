from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

r_bg,g_bg,b_bg = 1.0, 1.0, 1.0
rdes, gdes, bdes, ades = 1.0, 0.0, 0.0, 0.8
rsrc,gsrc,bsrc, asrc = 0.0, 0.0, 1.0, 0.2
rtar, gtar, btar, atar = 0.0, 0.0, 0.0, 1.0

def init():
    global rtar, btar, gtar, atar
    glClearColor(r_bg, g_bg, b_bg, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,5,0,0,0,0,1,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-8, 8, -8, 8, -8, 8)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
    rtar, gtar, btar = blend_colors((rsrc,gsrc,bsrc), (rdes, gdes, bdes), asrc, ades)
    
def blend_colors(source_color, destination_color, sfactor, dfactor):    
    blended_color = [(s * sfactor) + (d * dfactor)   for s, d in zip(source_color, destination_color)]
    blended_color = [min(1, max(0, x)) for x in blended_color]
    print("Intersect colors: ", blended_color)
    return tuple(blended_color)

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glPushMatrix()
    glColor4f(0.0, 0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0,8) #after view transfrom zeye = -5
    glVertex2f(0,-8)
    glVertex2f(8,0)
    glVertex2f(-8,0)
    glEnd()
    glPopMatrix
    
    glPushMatrix()
    glColor4f(rdes, gdes, bdes, ades)
    glutSolidSphere(2.0, 80, 80) #after view transfrom zeye = -3, -7
    glPopMatrix()
    
    glPushMatrix()
    glColor4f(rsrc,gsrc,bsrc, asrc)
    glTranslatef(-2.0, 0.0, 0.0) #after view transfrom zeye = -8, -4
    glutSolidCube(4.0)
    glPopMatrix()
    
    glPushMatrix()
    glColor4f(rtar, gtar, btar, atar)
    print("Small Sphere colors: " , rtar, gtar, btar)
    glTranslatef(3.0, -3.0, 0.0)
    glutSolidSphere(1, 80, 80)
    glPopMatrix()
    
    glFlush()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b'Blending')
    init()
    glutDisplayFunc(display)
    glutMainLoop()
    

if __name__ == '__main__': main()