import numpy as np
import matplotlib.pyplot as plt


def cardinal_spline(t,points, tension=0.5):

    t2 = t * t
    t3 = t2 * t
    s = (1 - tension) / 2.0

    b1 = s * (-t3 + 2 * t2 - t)
    b2 = s * (3 * t3 - 5 * t2 + 2)
    b3 = s * (-3 * t3 + 4 * t2 + t)
    b4 = s * (t3 - t2)

    x = 0.5 * (points[0][0] * b1 + points[1][0] * b2 + points[2][0] * b3 + points[3][0] * b4)
    y = 0.5 * (points[0][1] * b1 + points[1][1] * b2 + points[2][1] * b3 + points[3][1] * b4)

    return x, y





# Задаем точки для первого сегмента
P0 = np.array([0, 1])
P1 = np.array([1, 1])
P2 = np.array([2, -1])
P3 = np.array([3, 0])

# Задаем точки для второго сегмента
Q0 = np.array([3, 0])
Q1 = np.array([4, 1])
Q2 = np.array([5, -1])
Q3 = np.array([6, 111])

# Определяем параметрический диапазон t
t_values = np.linspace(0, 1, 100)

# Вычисляем значения для первого и второго сегментов
SP_values = np.array([cardinal_spline(t, np.array([P0, P1, P2, P3]),tension=0.1) for t in t_values])
SQ_values = np.array([cardinal_spline(t, np.array([Q0, Q1, Q2, Q3]),tension=0.7) for t in t_values])

# Рисуем кривые
plt.plot(SP_values[:, 0], SP_values[:, 1], label='Сегмент 1')
plt.plot(SQ_values[:, 0], SQ_values[:, 1], label='Сегмент 2')


plt.show()