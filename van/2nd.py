import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

scale_size = 5

vertex = np.array([
    np.array([-scale_size * np.sqrt(3) / 2, -scale_size / 2, 0]),
    np.array([-scale_size * np.sqrt(3) / 2, scale_size / 2, 0]),
    np.array([0, scale_size, 0]),
    np.array([scale_size * np.sqrt(3) / 2, scale_size / 2, 0]),
    np.array([scale_size * np.sqrt(3) / 2, -scale_size / 2, 0]),
    np.array([0, -scale_size, 0]),
    np.array([-scale_size * np.sqrt(3) / 3, scale_size, scale_size * np.sqrt(2 / 3)]),
    np.array([2 * scale_size * np.sqrt(3) / 3, 0, scale_size * np.sqrt(2 / 3)]),
    np.array([-scale_size * np.sqrt(3) / 3, -scale_size, scale_size * np.sqrt(2 / 3)]),
    np.array([-scale_size * np.sqrt(3) / 6, scale_size / 2, 2 * scale_size * np.sqrt(2 / 3)]),
    np.array([scale_size * np.sqrt(3) / 3, 0, 2 * scale_size * np.sqrt(2 / 3)]),
    np.array([-scale_size * np.sqrt(3) / 6, -scale_size / 2, 2 * scale_size * np.sqrt(2 / 3)])
])
edges = [
    [0, 5, 8],
    [1, 2, 6],
    [3, 4, 7],
    [9, 10, 11],
    [0, 1, 2, 3, 4, 5],
    [0, 1, 6, 9, 11, 8],
    [2, 3, 7, 10, 9, 6],
    [5, 4, 7, 10, 11, 8]
]

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection([vertex[edge] for edge in edges], alpha=0.7, facecolor='#8c00ac', edgecolor='#4d4d4d'))
    ax.auto_scale_xyz([-5, 5], [-5, 5], [0, 10])
    # ax.grid(False)
    # plt.axis('off')
    plt.show()
