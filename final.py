from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

width, height = 600, 600
ball_y = 2
step = 0.005
Popt = 1
ex,ey,ez = 0,0.4,35
light, blend,texture = False, False, False
r,g,b = 1., 1., 1.
shininess = 10
w = 0.4
theta, sign = 0, 1
quad_id, ball1_id, ball2_id = 0, 0, 0

def InitGL():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glColor4f(1.0, 1.0, 1.0, 0)
  glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
  glEnable(GL_LIGHT0)
  load_texture()

def setup_lighting():
  glLightfv(GL_LIGHT0,GL_DIFFUSE,[r, g, b, 1.0 ])
  glLightfv(GL_LIGHT0,GL_AMBIENT,[r, g, b, 1.0 ])
  glLightfv(GL_LIGHT0,GL_SPECULAR,[r, g, b, 1.0 ])  
  
def load_image_to_texture(filename):
  img = Image.open(filename).convert("RGB")
  img = img.transpose(Image.FLIP_TOP_BOTTOM)
  img_data = img.tobytes()
  texture_id = glGenTextures(1)
  glBindTexture(GL_TEXTURE_2D, texture_id)
  glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
  glTexImage2D(
      GL_TEXTURE_2D, 0, GL_RGB,
      img.width, img.height, 0,
      GL_RGB, GL_UNSIGNED_BYTE, img_data
  )
  glBindTexture(GL_TEXTURE_2D, 0)
  return texture_id

def load_texture():
  global quad_id, ball1_id, ball2_id
  quad_id = load_image_to_texture('./scales/world.jpg')
  ball1_id = load_image_to_texture('./scales/nebula.jpg')
  ball2_id = load_image_to_texture('./scales/moon.jpg')
  print(quad_id, ball1_id, ball2_id)   
  
  
def SetView():
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  if Popt == 1:
    glFrustum(-4, 4, -4, 4, 15, 35)
  elif Popt == 2:
    glOrtho(-6, 6, -6, 6, 15, 35)
  else:
    gluPerspective(30, 1, 15, 35) #the smaller the fov, the bigger the obj
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  gluLookAt(ex, ey, ez, 0, 0, 0, 0, 1, 0)
  
def setBlend():
  if blend:
    glEnable(GL_BLEND)
    glDisable(GL_DEPTH_TEST)
  else:
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)

def lightProperty():
  if light:
    glEnable(GL_LIGHTING)
  else:
    glDisable(GL_LIGHTING)
  
  glPushMatrix()
  glRotatef(theta, 0, 1, 0)
  glLightfv(GL_LIGHT0,GL_POSITION,[1.0, 0.0, 0.0, 0 ])
  glPopMatrix()
    
def useTexture(tex_id):
  glEnable(GL_TEXTURE_2D)
  glBindTexture(GL_TEXTURE_2D, tex_id)

def stopTexture():
  if texture:
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    
def setMaterial(diffuse, ambient, specular):
  glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
  glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
  glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
  if shininess:
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)
        
def On_arrowKey(key, x, y):
  global ex,ey,ez
  if key == GLUT_KEY_UP:
      ey += 1
  elif key == GLUT_KEY_DOWN:
      ey -= 1
  elif key == GLUT_KEY_RIGHT:
      ex  += 1
  elif key == GLUT_KEY_LEFT:
      ex -= 1
  elif key == GLUT_KEY_PAGE_UP: #press:Pg Up
      ez +=1
  elif key == GLUT_KEY_PAGE_DOWN: #press:Pg Dn
      ez -=1
  
  glutPostRedisplay()
    
def On_keyboard(key, x, y):
  global light, blend, Popt, texture
  global xe, ye, ze, w, r, g, b, shininess
  if key == b'\x1b':
      glutLeaveMainLoop()
  elif key == b'f':
      Popt = 1
  elif key == b'p':
      Popt = 0
  elif key == b'o':
      Popt = 2           
  elif key == b'l':
      light = not light   
  elif key == b'b':
      blend = not blend    
  elif key == b'i':
      if (w <= 1.0):
          w = w + 0.1
  elif key == b'd':
      if (r > 0.0):
          w = w - 0.1
  elif key == b't':
      texture = not texture
  elif key == b'0':#red
      r,g,b =1.0, 1.0, 1.0
  elif key == b'1':#red
      r,g,b =1.0, 0.0, 0.0
  elif key == b'2':#green
      r,g,b =0.0, 1.0, 0.0
  elif key == b'3':#blue
      r,g,b =0.0, 0.0, 1.0
  elif key == b'4': #red & green
      r,g,b = 1.0, 1.0, 0.0
  elif key == b'5': #red & blue
      r,g,b =1.0, 0.0, 1.0
  elif key == b'6': #green & blue
      r,g,b =0.0, 1.0, 1.0
  elif key == b's': #increase shininess
      shininess += 1
  elif key == b'w': #decrease shininess
      if shininess > 1:
        shininess -= 1
      
  glutPostRedisplay()
  
def MyIdle():
  global ball_y, step, theta, sign
    
  if (ball_y < 0.5) or (ball_y > 5.0):
    step *= -1
  ball_y += step
  
  theta = theta + (0.05*sign)
  if ((theta >= 360.0) | (theta <= 0.0)):
    sign = sign*(-1)
  glutPostRedisplay()
  
  
def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  SetView()
  setBlend()
  setup_lighting()
  lightProperty()
  
  glPushMatrix()
  glColor4f(1.0, 1.0, 1.0, 0.6)
  setMaterial([0.2, 0.0, 0.0, 0.6 ], [0.2*w, 0.0, 0.0, 0.6 ], [1., 1., 1., 1.0 ])
  if texture:
    useTexture(quad_id)
  glBegin(GL_QUADS)
  glTexCoord2f(0, 0); glVertex3f(-5, 0, -5)
  glTexCoord2f(1, 0); glVertex3f(5, 0, -5)
  glTexCoord2f(1, 1); glVertex3f(5, 0, 5)
  glTexCoord2f(0, 1); glVertex3f(-5, 0, 5)
  glEnd()
  glPopMatrix()
  stopTexture()
  
  glPushMatrix()
  glColor4f(1.0, 0.0, 0.0, 0.6)
  setMaterial([1.0, 0.0, 0.0, 0.6 ], [1.0*w, 0.0, 0.0, 0.6 ], [1., 1., 1., 1.0 ])
  glTranslatef(0.0, ball_y, 0.0)
  if texture:
    useTexture(ball1_id)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1, 80, 80)
  else: 
    glutSolidSphere(1, 80, 80)
  glPopMatrix()
  stopTexture()
    
  glPushMatrix()
  glColor4f(1.0, 0.5, 0.0, 0.6)
  setMaterial([1.0, 0.5, 0.0, 0.6 ], [1.0*w, 0.5*w, 0.0, 0.6 ], [1., 1., 1., 1.0 ])
  glTranslatef(0.0, -ball_y, 0.0)
  if texture:
    useTexture(ball2_id)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1, 80, 80) 
  else:
    glutSolidSphere(1, 80, 80)
  glPopMatrix()
  stopTexture()
  
  glFlush()
  
def main():
  glutInit()
  glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
  glutInitWindowSize(height, width)
  glutCreateWindow(b'ball')
  InitGL()
  glutDisplayFunc(display)
  glutSpecialFunc(On_arrowKey)
  glutKeyboardFunc(On_keyboard)
  glutIdleFunc(MyIdle)
  glutMainLoop()
  
  return 

if __name__ == '__main__' : main()

