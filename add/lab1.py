import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()

ax = fig.add_subplot(111,projection = "3d")
n = 6
size = 5
heigth = 10
def point(size, i):
    angle_deg = 360/n * i - 360/(2*n)
    angle_rad = np.pi / 180 * angle_deg
    return size * np.cos(angle_rad),size * np.sin(angle_rad)

verticles = []
for i in range(n):
    p = point(size,i)
    verticles.append([p[0],p[1],-heigth])

for i in range(n):
    p = point(size,i)
    verticles.append([p[0], p[1], heigth])
del verticles[3]
verticles = np.array(verticles)
faces = []
for i in range(n):
    j1 = i
    j2 = i + 1
    j3 = i + n +1
    j4 =  i + n
    if (i + 1) % n == 0:
        j2 =  i + 1 - n
        j3 =  i + n +1 - n

    faces.append([
        j1,j2,j3,j4])

faces =  np.array(faces)

top_face = []
down_face = []
for i in range(n):
    top_face.append(n+i)
    down_face.append(i)
top_face = np.array([top_face])
down_face = np.array([down_face])
top = [
    Poly3DCollection(
        [verticles[face] for face in top_face],
        facecolor = 'orange',
        edgecolor = 'k')
]
down = [
    Poly3DCollection(
        [verticles[face] for face in down_face],
        facecolor = 'orange',
        edgecolor = 'k')
]
prizma = [
    Poly3DCollection(
        [verticles[face] for face in faces],
        facecolor = 'orange',
        edgecolor = 'k')
]


ax.add_collection3d(prizma[0])
ax.add_collection3d(top[0])
ax.add_collection3d(down[0])


ax.auto_scale_xyz([-2,2],[-2,2],[-2,2])
plt.show()