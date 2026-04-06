from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import math

name = b'Transformation'

left, right, bottom, top = -5., 15., -5., 15.

c,d = 6,8
step = 2 
triangle = np.array([[-2.5, 0+c+step], [0,2+c+step], [2.5,0+c+step]])
rectangle = np.array([[-2,-2+c], [-2,2+c], [2,2+c], [2,-2+c]])

transform = False
  
def InitGL():
  glClearColor(1.0,1.0,1.0,0.0)
  glColor3f(0.0,0.0, 0.0)
  glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(left, right, bottom, top)    
  
def display():
  glClear(GL_COLOR_BUFFER_BIT)
  glPushMatrix()
  glBegin(GL_LINES)
  glVertex2f(-5., 0.)
  glVertex2f(15., 0.)
  glVertex2f(0., 15.)
  glVertex2f(0., -5)
  glEnd()
  glPopMatrix()
  
  glPushMatrix()
  
  if transform:
    glTranslatef(d,0,0)
    glRotatef(90,0,0,1)
    glTranslatef(0,-c,0)
    
  glBegin(GL_TRIANGLES)
  for p in triangle:
    glVertex2f(p[0], p[1])
  glEnd()
  
  glBegin(GL_QUADS)
  for p in rectangle:
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
  glutInitWindowSize(600, 600)
  glutCreateWindow(name)
  InitGL()
  glutDisplayFunc(display)
  glutKeyboardFunc(OnKeyboard)
  glutMainLoop()
  
  return

if __name__ == '__main__': main()