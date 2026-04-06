from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import math

name = b'Transformation'

left, right, bottom, top = -4., 4., -1., 4.

o = np.array([[0, 0, 1], [0,2, 1], [2, 0, 1]])
transform = False
  
def InitGL():
  glClearColor(1.0,1.0,1.0,0.0)
  #glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(left, right, bottom, top)    
  
def display():
  glClear(GL_COLOR_BUFFER_BIT)
  glPushMatrix()
  glColor3f(0.0,0.0,0.0)
  glBegin(GL_LINES)
  for y in range (-1,5):
    glVertex2f(-4., y)
    glVertex2f(4., y)
  for x in range (-4, 5):
    glVertex2f(x, 4)
    glVertex2f(x, -1)  
  glEnd()
  glPopMatrix()
  
  glPushMatrix()
  if transform:
    glColor3f(0.0,1.0,0.0)
    glTranslatef(-3,3,0)
    glScalef(2,-1,0)
  else:
    glColor3f(1.0,0.0,0.0)
    
  glBegin(GL_TRIANGLES)
  for p in o:
    glVertex2f(p[0], p[1])
  glEnd()
  glPopMatrix() 
    
  glFlush()
  
def OnKeyboard(key, x, y):
  global transform
  if (key.lower() == b'\r'):
    transform = not transform
  glutPostRedisplay()
  
def main():
  glutInit()
  glutInitDisplayMode(GLUT_RGB)
  glutInitWindowSize(800, 500)
  glutCreateWindow(name)
  InitGL()
  glutDisplayFunc(display)
  glutKeyboardFunc(OnKeyboard)
  glutMainLoop()
  return

if __name__ == '__main__': main()