from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import math

name = b'Transformation'

left, right, bottom, top = -4., 4., -1., 4.

cx, cy = 0., 0.
o = np.array([[0, 0, 1], [0,2, 1], [2, 0, 1]])
T = np.zeros([3,3], dtype = float)
transform = False

def init():
  global cx,cy
  sx, sy = 0., 0.
  for p in o:
      sx =sx + p[0]
      sy =sy + p[1]
  cx = sx/len(o)
  cy = sy/len(o)

def myPushMatrix():
  global T
  T = np.identity(3, dtype=float)
  print("Identity\n", T)

def myRotatef(theta):
  global T
  R = np.identity(3, dtype=float)
  ang = (theta*np.pi)/180
  R[0,0] = math.cos(ang)
  R[0,1] = math.sin(ang)
  R[1,0] = -math.sin(ang)
  R[1,1] = math.cos(ang)
  T = np.matmul(R,T)
  print("Rotate\n", T)
  
def myTranslatef(tx,ty):
  global T
  Ts =  np.identity(3, dtype = float)
  Ts[2,0] = tx
  Ts[2,1] = ty
  T = np.matmul(Ts, T)
  print("Translate\n", T)
  
def myScalef(sx, sy):
  global T
  Sc = np.identity(3, dtype=float)
  Sc[0,0] = sx
  Sc[1,1] = sy
  T = np.matmul(Sc, T)
  print("Scale\n", T)
  
def myPopMatrix():
  T = np.zeros([3,3], dtype=float)
  print("Pop\n", T)
  
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
  
  if not transform:
    glPushMatrix()
    glBegin(GL_TRIANGLES)
    glColor3f(0.0,1.0,0.0)
    for p in o:
      glVertex2f(p[0], p[1])
    glEnd()
    glPopMatrix() 
  else: 
    myPushMatrix()
    glColor3f(1.0,0.0,0.0)
    myTranslatef(cx-3, cy+1.68) 
    myRotatef(270)
    myTranslatef(-cx, -cy) 
    myScalef(1,2)
    obj = np.matmul(o,T)
    glBegin(GL_TRIANGLES)
    for p in obj:
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
  glutInitWindowSize(800, 500)
  glutCreateWindow(name)
  init()
  InitGL()
  glutDisplayFunc(display)
  glutKeyboardFunc(OnKeyboard)
  glutMainLoop()
  return

if __name__ == '__main__': main()