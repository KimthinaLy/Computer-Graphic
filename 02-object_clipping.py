from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

#Rectangle
XMax = 200.0
YMax = 200.0
XMin = -XMax
YMin = -YMax

Left = 1
Right = 2
Bottom = 4
Top = 8

drawInside = False

originalP = []
p = []
p_temp = []

r1,g1,b1 = 0.0, 0.5, 0.5
r2,g2,b2 = 0.0, 0.5, 0.5

def SetPoint():
  global p, originalP
  p = [[-290.,110.], [-60.,330.], [270.,115.], [125, 20], [340.,-90.], [165.,-270.], [20, -120],[-30., -280.],[-300,-125], [-60, 20]]
  originalP = p
  
def init():
  glClearColor(1.0, 1.0, 1.0, 0.0)
  glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(-600, 600, -600, 600)
  SetPoint()
  
def main():
  glutInit()
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
  glutInitWindowSize(600, 600)
  glutCreateWindow(b'Clip Object')
  init()
  glutDisplayFunc(display)
  glutKeyboardFunc(OnKeyboard)
  glutMainLoop()
  
def display():
  glClear(GL_COLOR_BUFFER_BIT)
  
  #Draw Original Points
  glPushMatrix()
  glColor3f(r1, g1, b1)
  glBegin(GL_POLYGON)
  for i in originalP:
    glVertex2f(i[0], i[1])
  glEnd()
  glPopMatrix()
  
  
  #Draw Clipped Points in white color

  glPushMatrix()  
  glColor3f(r2, g2, b2)
  glBegin(GL_POLYGON)
  for i in p:
    glVertex2f(i[0], i[1])
  glEnd()
  glPopMatrix()
  
  #Draw Window
  glPushMatrix()
  glColor3f(1.0, 0.0, 0.0)
  glBegin(GL_QUADS)
  glVertex2f(XMin,YMin)
  glVertex2f(XMin,YMax)
  glVertex2f(XMax,YMax)
  glVertex2f(XMax,YMin)
  glEnd()
  glPopMatrix()
  
  glFlush()
  
def OnKeyboard(key, X, Y):
  global r1,g1,b1,r2,g2,b2
  
  if(key.lower() == b'o'):
    r1,g1,b1 = 1.0, 1.0, 1.0
    r2,g2,b2 = 0.0, 0.5, 0.5
    ClipObj()
  if(key.lower() == b'i'):
    r1,g1,b1 = 0.0, 0.5, 0.5
    r2,g2,b2 = 1.0, 1.0, 1.0
    ClipObj()
  glutPostRedisplay() 

def ClipObj():
  global p, p_temp
  
  for s in range(4):
    p_temp = []
    m = len(p)
    
    for i in range(m):
      if (i == m-1):
        ClipSide(p[i], p[0], s)
      else:
        ClipSide(p[i], p[i+1], s)
        
    p = p_temp
    
def ClipSide(s, p, side):
  global p_temp
  
  sx, sy = s
  px, py = p
  
  dy = py - sy
  dx = px - sx
  if (dx == 0):
    dx = 0.000000001
  m = dy / dx
  
  # left side
  if (side == 0):
    if px >= XMin:
      if sx < XMin:
        y = py - m*(px - XMin)
        x = XMin
        p_temp.append([x,y])
      p_temp.append(p)
    else:
      if sx >= XMin:
        y = py - m*(px - XMin)
        x = XMin
        p_temp.append([x,y])
  elif side == 1:           # Right Side
    if px <= XMax:
      if sx > XMax:
          y = py - m*(px - XMax)
          x = XMax
          p_temp.append([x,y])
      p_temp.append(p)
    else:
      if s[0] <= XMax:
        y = py - m*(px - XMax)
        x = XMax
        p_temp.append([x,y]) 
  elif side == 2:     # Bottom Side
    if py >= YMin:
      if sy < YMin:
        x = px - (py - YMin)/m
        y = YMin
        p_temp.append([x,y])
      p_temp.append(p)
    else:
      if sy >= YMin:
        x = px - (py - YMin)/m
        y = YMin
        p_temp.append([x,y])
  elif side == 3: #Top
    if py <= YMax:
      if sy > YMax:
        x = px - (py - YMax)/m
        y = YMax
        p_temp.append([x,y])
      p_temp.append(p)
    else:
      if sy <= YMax:
        x = px - (py - YMax)/m
        y = YMax
        p_temp.append([x,y])
        
if __name__ == '__main__': 
  main()       