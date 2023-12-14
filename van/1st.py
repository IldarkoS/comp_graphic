import matplotlib.pyplot as plt
import numpy as np
import customtkinter


def f(x, y, a):
    return (x ** 2 + y ** 2 + a * x) ** 2 - (a ** 2) * (x ** 2 + y ** 2)


def doit(a):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5

    x = np.linspace(x_min, x_max, 100, axis=0)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)

    plt.contour(X, Y, f(X, Y, a), levels=[0], colors='green')
    plt.axis('equal')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


# интерфейс
customtkinter.set_appearance_mode("light")

customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("320x240")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="Ввод")
label1.pack(pady=10, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Параметр")
entry1.pack(pady=5, padx=10)


def DoIt():
    v1 = float(entry1.get())
    doit(v1)


button = customtkinter.CTkButton(master=frame, text="Нарисовать", command=DoIt)
button.pack(pady=10, padx=10)

root.mainloop()
