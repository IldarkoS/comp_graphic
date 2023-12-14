from math import cos, sin, radians, sqrt

import pygame
import numpy as np
from tkinter import Tk, Button, Entry, Label

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def rotate_matrix(x: float = 360, y: float = 360, z: float = 360) -> np.array:
    x, y, z = radians(x), radians(y), radians(z)
    return np.array([[round(cos(y)*cos(z), 14), round(sin(x)*sin(y)*cos(z)-cos(x)*sin(z), 14), round(cos(x)*sin(y)*cos(z)+sin(x)*sin(z), 14)],
                     [round(cos(y)*sin(z), 14), round(sin(x)*sin(y)*sin(z)+cos(x)*cos(z), 14), round(cos(x)*sin(y)*sin(z)-sin(x)*cos(z), 14)],
                     [round(-sin(y), 14), round(sin(x)*cos(y), 14), round(cos(x)*cos(y), 14)]])


class Paraboloid:
    def __init__(self, height: float, outer_radius: float, sides: int = 10,
                 x0: float = 0, y0: float = 0, z0: float = 0):

        self.height = height

        self.sides = sides
        angle_step = 360 / (2 * sides)
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0

        self.outer_up_center = np.array([x0, y0 + height, z0])
        self.outer_down_center = np.array([x0, y0, z0])
        self.inner_center = np.array([x0, y0, z0])

        k = height/(outer_radius**2)
        h = height/sides

        self.side_coordinates = list()
        for j in range(1, sides + 1):
            self.side_coordinates.append(np.array([[x0 + sqrt(h*j/k) * cos(radians(i * angle_step)),
                                                    y0 + h*j,
                                                    z0 + sqrt(h*j/k) * sin(radians(i * angle_step))] for i in range(2 * sides + 1)]))

    def rotate(self, x: float = 360, y: float = 360, z: float = 360):
        self.inner_center = np.dot(self.inner_center, rotate_matrix(x, y, z))
        self.outer_up_center = np.dot(self.outer_up_center, rotate_matrix(x, y, z))
        self.outer_down_center = np.dot(self.outer_down_center, rotate_matrix(x, y, z))
        self.side_coordinates = [np.dot(coordinates, rotate_matrix(x, y, z)) for coordinates in self.side_coordinates]

    def scale(self, value: float):
        self.inner_center *= value
        self.outer_up_center *= value
        self.outer_down_center *= value
        self.side_coordinates = [coordinates * value for coordinates in self.side_coordinates]


def move(paraboloid: Paraboloid, dx: float = 0, dy: float = 0, dz: float = 0):

    for coordinates in paraboloid.side_coordinates:
        coordinates[:, 0] += dx
    paraboloid.inner_center[0] += dx
    paraboloid.outer_up_center[0] += dx
    paraboloid.outer_down_center[0] += dx

    for coordinates in paraboloid.side_coordinates:
        coordinates[:, 1] += dy
    paraboloid.inner_center[1] += dy
    paraboloid.outer_up_center[1] += dy
    paraboloid.outer_down_center[1] += dy

    for coordinates in paraboloid.side_coordinates:
        coordinates[:, 2] += dz
    paraboloid.inner_center[2] += dz
    paraboloid.outer_up_center[2] += dz
    paraboloid.outer_down_center[2] += dz


def draw_taper(paraboloid: Paraboloid):
    side_cords = paraboloid.side_coordinates
    for k in range(len(side_cords)-1):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(2 * paraboloid.sides + 1):
            glVertex3f(side_cords[k][i][0], side_cords[k][i][1], side_cords[k][i][2])
            glVertex3f(side_cords[k+1][i][0], side_cords[k+1][i][1], side_cords[k+1][i][2])
        glEnd()

    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(*paraboloid.outer_down_center)
    for i in range(2 * paraboloid.sides + 1):
        glVertex3f(paraboloid.side_coordinates[0][i][0],
                   paraboloid.side_coordinates[0][i][1],
                   paraboloid.side_coordinates[0][i][2])
    glEnd()


def animation(barrel: Paraboloid, iteration: float, flag: bool = False):
    speed = 5 * sin(radians(iteration))
    if flag:
        barrel.rotate(z=speed)


def key_handler(pressed_keys, paraboloid: Paraboloid):
    alpha, betta, gamma = 0, 0, 0
    speed = 3

    if pressed_keys[pygame.K_d]:
        betta += speed
    if pressed_keys[pygame.K_a]:
        betta -= speed
    if pressed_keys[pygame.K_s]:
        alpha -= speed
    if pressed_keys[pygame.K_w]:
        alpha += speed
    if pressed_keys[pygame.K_q]:
        gamma -= speed
    if pressed_keys[pygame.K_e]:
        gamma += speed

    if pressed_keys[pygame.K_UP]:
        move(paraboloid, dy=0.02)
    if pressed_keys[pygame.K_DOWN]:
        move(paraboloid, dy=-0.02)
    if pressed_keys[pygame.K_LEFT]:
        move(paraboloid, dx=0.02)
    if pressed_keys[pygame.K_RIGHT]:
        move(paraboloid, dx=-0.02)
    if pressed_keys[pygame.K_LCTRL]:
        move(paraboloid, dz=0.02)
    if pressed_keys[pygame.K_SPACE]:
        move(paraboloid, dz=-0.02)

    if pressed_keys[pygame.K_EQUALS]:
        paraboloid.scale(1.01)
    if pressed_keys[pygame.K_MINUS]:
        paraboloid.scale(0.99)

    paraboloid.rotate(alpha, betta, gamma)


def main():
    paraboloid = Paraboloid(height=float(fill_hight.get()), outer_radius=float(fill_radius.get()), sides=int(fill_approx.get()))

    pygame.init()
    pygame.display.set_caption('Параболоид')
    display = (900, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, -float(fill_hight.get()) * 0.5, -max(float(fill_hight.get()), float(fill_radius.get())) * 4)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0.4, float(fill_radius.get()) * 2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glEnable(GL_LIGHT0)

    glMaterial(GL_FRONT, GL_DIFFUSE, [0.0, 1.0, 0.0, 1.0])
    glMaterial(GL_FRONT, GL_AMBIENT, [0.0, 0.5, 0.0, 1.0])

    iteration = -1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClearColor(1.0, 0.95, 0.9, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        key_handler(pygame.key.get_pressed(), paraboloid)
        draw_taper(paraboloid)

        iteration = (iteration + 1) % 360
        animation(paraboloid, iteration, False)

        pygame.display.flip()
        pygame.time.wait(5)


frame = Tk()
frame.title("Параболоид 3д")
frame.geometry("400x300")
Label(frame, text='Высота', font=120).pack(pady=5, padx=10)
fill_hight = Entry(frame)
fill_hight.pack(pady=15, padx=10)
Label(frame, text='Радиус', font=120).pack(pady=5, padx=10)
fill_radius = Entry(frame)
fill_radius.pack(pady=10, padx=10)
Label(frame, text='Степень аппроксимации', font=120).pack(pady=5, padx=60)
fill_approx = Entry(frame)
fill_approx.pack(pady=10, padx=10)
btn = Button(text='Нарисовать', height=3, width=10, command=main)
btn.pack(pady=10, padx=10)
frame.mainloop()
