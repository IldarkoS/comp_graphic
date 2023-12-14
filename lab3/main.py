import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.text import Text
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button

fig = plt.figure()
fig.subplots_adjust(bottom=0.3)
ax = fig.add_subplot(111, projection='3d')

R, h = map(float, input("Введите параметры полушария (R, h): ").split())
N = int(input("Введите точность аппроксимации: "))

vertices = []
sides = []

for i in range(N + 1):
    phi = i * math.pi / N
    cos_phi = math.cos(phi)
    sin_phi = math.sin(phi)

    for j in range(N + 1):
        theta = j * 2 * math.pi / N
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        x = R * sin_phi * cos_theta
        y = R * sin_phi * sin_theta
        z = R * cos_phi + h

        if z > h:
            z = h

        vertices.append((x, y, z))

for i in range(N):
    for j in range(N):
        vertex1 = vertices[i * (N + 1) + j]
        vertex2 = vertices[i * (N + 1) + j + 1]
        vertex3 = vertices[(i + 1) * (N + 1) + j + 1]
        vertex4 = vertices[(i + 1) * (N + 1) + j]

        sides.append([vertex1, vertex2, vertex3, vertex4])

ax.add_collection3d(Poly3DCollection(sides, facecolors='green', linewidth=0.1, edgecolors='black', alpha=1))


def remove_func(event):
    ax.add_collection3d(Poly3DCollection(sides, facecolors='green', linewidths=0.1, edgecolors='black', alpha=1))
    plt.draw()


def show_func(event):
    global visible
    if visible:
        visible = False
        ax.add_collection3d(Poly3DCollection(sides, facecolors='green', alpha=0.5, edgecolors='black', linewidths=0.1))
        plt.draw()
    else:
        visible = True
        remove_func(event)


show_button_ax = fig.add_axes([0.1, 0.25, 0.5, 0.05])
show_button = Button(show_button_ax, "Показать невидимые линии", color='g')
visible = True
show_button.on_clicked(show_func)

ax.grid(False)
ax.axis(False)
ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_zlim(0, h + R)
plt.show()
