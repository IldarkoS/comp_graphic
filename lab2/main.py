import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Определение вершин клина
vertices = np.array([
    [0, 0, 0],  # Вершина A
    [1, 0, 0],  # Вершина B
    [0.5, 0, 1],  # Вершина C
    [0.5, 1, 0],  # Вершина D
])

# Определение граней клина
edges = [
    (0, 1),  # Ребро AB
    (0, 2),  # Ребро AC
    (0, 3),  # Ребро AD
    (1, 2),  # Ребро BC
    (1, 3),  # Ребро BD
    (2, 3),  # Ребро CD
]

# Функция для рисования клина в 3D
def draw_wedge(ax, vertices, edges):
    for edge in edges:
        vertex1 = vertices[edge[0]]
        vertex2 = vertices[edge[1]]
        x1, y1, z1 = vertex1
        x2, y2, z2 = vertex2
        ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')

# Создание 3D графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Рисование клина
draw_wedge(ax, vertices, edges)

# Настройка вида
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Клин')

# Отображение графика
plt.show()
