import matplotlib.pyplot as plt


def input_data(x, y):
    for i in range(int(input("Количество точек: "))):
        x.append(float(input("Координата x для точки №" + str(i + 1) + ": ")))
        y.append(float(input("Координата y для точки №" + str(i + 1) + ": ")))


def bezier():
    for i in range(len(xLast)):
        plt.plot(xLast[i], yLast[i], '.m')


def get_value(x1, x2, t):
    return x1 + (x2 - x1) * t


def draw(x, y, num):
    if num == 3:
        x0 = get_value(x[0], x[1], i / frequency)
        y0 = get_value(y[0], y[1], i / frequency)
        x1 = get_value(x[1], x[2], i / frequency)
        y1 = get_value(y[1], y[2], i / frequency)
        plt.plot([x0, x1], [y0, y1], ':k')
        xLast.append(get_value(x0, x1, i / frequency))
        yLast.append(get_value(y0, y1, i / frequency))
        plt.plot(xLast[i], yLast[i], '.b')

    else:
        xNext, yNext = [], []
        for j in range(num - 1):
            xNext.append(get_value(x[j], x[j + 1], i / frequency))
            yNext.append(get_value(y[j], y[j + 1], i / frequency))
        plt.plot(xNext, yNext, '-.y')
        draw(xNext, yNext, num - 1)


def show():
    plt.grid(True)
    plt.plot(x, y, 'k')
    bezier()


x, y, xLast, yLast = [], [], [], []
frequency = 100
input_data(x, y)
fig = plt.figure()
ax = fig.add_subplot(111)
show()
for i in range(frequency + 1):
    draw(x, y, len(x))
    plt.pause(0.03)
    plt.cla()
    show()
plt.cla()
show()
plt.plot(xLast, yLast, 'r')
plt.show()
