from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import math

name = b'Transformation'

left, right, bottom, top = -3., 8., -3., 8.

d, c = 0., 0.
triangle = np.array([[-1.5, 5, 1], [0,6.5, 1], [1.5, 5, 1]])
rectangle = np.array([[-1,3,1], [-1, 5,1], [1, 5,1], [1,3,1]])
T = np.zeros([3,3], dtype = float)
transform = False

CompositionM = ""

def init():
  global d, c
  syT, syR = 0., 0.
  for p in triangle:
    syT += p[1]
  for p in rectangle:
    syR += p[1]
  d = syT/len(triangle)
  c = syR/len(rectangle)

def myPushMatrix():
  global T, CompositionM
  T = np.identity(3, dtype=float)
  CompositionM += str(T) + "\n"

def myRotatef(theta):
  global T, CompositionM
  R = np.identity(3, dtype=float)
  ang = (theta*np.pi)/180
  R[0,0] = math.cos(ang)
  R[0,1] = math.sin(ang)
  R[1,0] = -math.sin(ang)
  R[1,1] = math.cos(ang)
  T = np.matmul(R,T)
  
  CompositionM += str(R) + "\n"
  
def myTranslatef(tx,ty):
  global T, CompositionM
  Ts =  np.identity(3, dtype = float)
  Ts[2,0] = tx
  Ts[2,1] = ty
  T = np.matmul(Ts, T)
  CompositionM += str(Ts) + "\n"
  
def myScalef(sx, sy):
  global T, CompositionM
  Sc = np.identity(3, dtype=float)
  Sc[0,0] = sx
  Sc[1,1] = sy
  T = np.matmul(Sc, T)
  CompositionM += str(Sc) + "\n"
  
def myPopMatrix():
  T = np.zeros([3,3], dtype=float)
  
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
  glVertex2f(-3., 0.)
  glVertex2f(8., 0.)
  glVertex2f(0., 8.)
  glVertex2f(0., -3)
  glEnd()
  glPopMatrix()
  
  if not transform:
    glPushMatrix()
    glBegin(GL_TRIANGLES)
    for p in triangle:
      glVertex2f(p[0], p[1])
    glEnd()
    
    glBegin(GL_QUADS)
    for p in rectangle:
      glVertex2f(p[0], p[1])
    glEnd()
    glPopMatrix() 
  else: 
    myPushMatrix()
    myTranslatef(d, 0) 
    myRotatef(90)
    myTranslatef(0 , -c) 
    obj = np.matmul(rectangle,T)
    print("=========== Rectangle ==========")
    print(str(rectangle)+ "\n" + CompositionM)
    obj2 = np.matmul(triangle,T)
    
    print("=========== Triangle ==========")
    print(str(triangle)+ "\n" + CompositionM)
    glBegin(GL_QUADS)
    for p in obj:
      glVertex2f(p[0], p[1])
    glEnd()    
    
    glBegin(GL_TRIANGLES)
    for p in obj2:
      glVertex2f(p[0], p[1])
    glEnd()
    myPopMatrix()
    
  glutSwapBuffers()
  
def OnKeyboard(key, x, y):
  global transform
  if (key.lower() == b'\r'):
    transform = not transform
  glutPostRedisplay()
  
def main():
  glutInit()
  glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
  glutInitWindowSize(600, 600)
  glutCreateWindow(name)
  init()
  InitGL()
  glutDisplayFunc(display)
  glutKeyboardFunc(OnKeyboard)
  glutMainLoop()
  
  return

if __name__ == '__main__': main()