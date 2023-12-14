import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import customtkinter
import threading
import numpy as np
R, h1, h2 = 1.0, 0.5, 0.5
N = 10
R_X, R_Y, R_Z, R_W = 1.0, 1.0, 1.0, 1.0
L1, L2, L3, L4 = 1.0, 1.0, 1.0, 1.0
M1, M2, M3, M4 = 1.0, 1.0, 1.0, 1.0
TARGET_POINT = [1,1,1]
M1_X_START, M2_X_START, M3_X_START, M4_X_START = 0, 0, 0, 0
DELTA = np.pi / 200
S_X, S_Y, S_Z = 1.0, 1.0, 1.0
UPDATE_DATA_FLAG = False
VERTICES = []
DELTA = np.pi / 200


def calculate_transparency(normal, direction, target_point):
    normal = normal / np.linalg.norm(normal)
    direction = direction / np.linalg.norm(direction)

    angle_cosine = np.dot(normal, direction)

    to_target = np.array(target_point) - np.zeros(3)

    if np.dot(normal, to_target) < 0:
        angle_cosine = -angle_cosine

    transparency = max(0, min(1, abs(angle_cosine)))

    return transparency


# Основной цикл отображения
def doit():
    global UPDATE_DATA_FLAG
    global M1_X_START, M2_X_START, M3_X_START, M4_X_START

    # Функция для создания вершин эллипсоида
    def create_circle(R,h1,h2, N):
        global VERTICES

        VERTICES = []
        for i in range(N + 1):
            phi = i * 2*math.pi / N
            cos_phi = math.cos(phi)
            sin_phi = math.sin(phi)

            for j in range(N + 1):
                # при 2п будет обычный эллипсоид
                theta = j * math.pi / N
                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)

                x = R * sin_theta * cos_phi
                y = R * sin_theta * sin_phi

                z = R*cos_theta
                if z > 0 and z > h1:
                    z = h1
                elif z< 0 and z < -h2:
                    z = -h2




                VERTICES.append((x, y, z))

    create_circle(R, h1, h2, N)

    # Инициализация Pygame и OpenGL
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_BLEND);
    i = 0
    transparency = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if UPDATE_DATA_FLAG:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            create_circle(R, h1, h2, N)
            UPDATE_DATA_FLAG = False
        glLightfv(GL_LIGHT0, GL_POSITION, [L1, L2, L3, L4])
        glLightfv(GL_LIGHT0, GL_AMBIENT,  [L1, L2, L3, L4])

        M4_X_START += DELTA

        glRotatef(R_X, R_Y, R_Z, R_W)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glScalef(S_X, S_Y, S_Z)
        glBegin(GL_QUADS)
        for i in range(N):
            for j in range(N):
                vertex1 = VERTICES[i * (N + 1) + j]
                vertex2 = VERTICES[i * (N + 1) + j + 1]
                vertex3 = VERTICES[(i + 1) * (N + 1) + j + 1]
                vertex4 = VERTICES[(i + 1) * (N + 1) + j]
                normal = np.cross(np.array(vertex2) - np.array(vertex1), np.array(vertex3) - np.array(vertex1))
                direction = np.array(TARGET_POINT) - np.array(vertex1)
                transparency = calculate_transparency(normal, direction, TARGET_POINT)

                glMaterial(GL_FRONT, GL_DIFFUSE,
                           [0.4, 0.5, 0.1, transparency])
                glVertex3fv(vertex1)
                glVertex3fv(vertex2)
                glVertex3fv(vertex3)
                glVertex3fv(vertex4)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3fv((0.0, 0.0, 0.0))
        for i in range(N):
            glVertex3fv(VERTICES[i * N + i])
            glVertex3fv(VERTICES[(i + 1) * N + i + 1])

            glVertex3fv(VERTICES[(i + 1) * N + i])
            glVertex3fv(VERTICES[(i + 1) * N + i + N + 1])
        glEnd()
        # красим низ
        glBegin(GL_TRIANGLE_FAN)
        glVertex3fv((0.0, 0.0, 0.0))

        for i in range(N):
            glVertex3fv(VERTICES[i * N + i])
            glVertex3fv(VERTICES[(i + 1) * N + i + 1])

            glVertex3fv(VERTICES[(i + 1) * N + i])
            glVertex3fv(VERTICES[(i + 1) * N + i + N + 1])
        glEnd()

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


def DoIt():
    global THREAD
    global R, h1, h2
    global TARGET_POINT

    global N
    global R_X, R_Y, R_Z, R_W
    global L1, L2, L3, L4
    global M1, M2, M3, M4
    global M1_X_START, M2_X_START, M3_X_START, M4_X_START

    R, h1, h2 = list(map(lambda x: float(x), entry1.get().split()))
    N = int(entry1_1.get())
    R_X, R_Y, R_Z, R_W = list(map(lambda x: float(x), entry2.get().split()))
    L1, L2, L3, L4 = list(map(lambda x: float(x), entry4.get().split()))
    TARGET_POINT = list(map(lambda x: float(x), entry5.get().split()))

    THREAD.start()


def update_values():
    global UPDATE_DATA_FLAG
    global R, h1, h2
    global TARGET_POINT
    global N
    global R_X, R_Y, R_Z, R_W
    global L1, L2, L3, L4
    global M1, M2, M3, M4
    global M1_X_START, M2_X_START, M3_X_START, M4_X_START

    R, h1, h2 = list(map(lambda x: float(x), entry1.get().split()))
    N = int(entry1_1.get())
    R_X, R_Y, R_Z, R_W = list(map(lambda x: float(x), entry2.get().split()))
    L1, L2, L3, L4 = list(map(lambda x: float(x), entry4.get().split()))
    TARGET_POINT = list(map(lambda x: float(x), entry5.get().split()))


THREAD = threading.Thread(target=doit, args=())

# интерфейс
customtkinter.set_appearance_mode("system")

customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("270x600")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="Параметры шара")
label1.pack(pady=5, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="а(R) b(h1) c(h2)")
entry1.pack(pady=5, padx=10)

label1_1 = customtkinter.CTkLabel(master=frame, text="Детализация[1]:")
label1_1.pack(pady=5, padx=10)

entry1_1 = customtkinter.CTkEntry(master=frame, placeholder_text="n")
entry1_1.pack(pady=5, padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Параметры вращения[4]:")
label2.pack(pady=5, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="x y z w")
entry2.pack(pady=5, padx=10)

label3 = customtkinter.CTkLabel(master=frame, text="Параметры масштабирования[3]:")
label3.pack(pady=5, padx=10)

entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="x y z")
entry3.pack(pady=5, padx=10)

label4 = customtkinter.CTkLabel(master=frame, text="Параметры освещения[4]:")
label4.pack(pady=5, padx=10)

entry4 = customtkinter.CTkEntry(master=frame, placeholder_text="x y z w")
entry4.pack(pady=5, padx=10)

label5 = customtkinter.CTkLabel(master=frame, text="Входная точка[3]:")
label5.pack(pady=5, padx=10)

entry5 = customtkinter.CTkEntry(master=frame, placeholder_text="x y z ")
entry5.pack(pady=5, padx=10)

button1 = customtkinter.CTkButton(master=frame, text="Запустить", command=DoIt)
button1.pack(pady=5, padx=10)

button3 = customtkinter.CTkButton(master=frame, text="Применить изменения", command=update_values)
button3.pack(pady=5, padx=10)

root.mainloop()