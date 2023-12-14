import sys
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QMainWindow
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class GLWidget(QOpenGLWidget):
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glutSolidSphere(1.0, 100, 50)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        central_widget = GLWidget(self)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
