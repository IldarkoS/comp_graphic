import matplotlib.pyplot as plt
import window
import numpy as np
from typing import *
import customtkinter


def func(phi)->float:
    return phi

def Plot(a,B):
    phi = np.linspace(0,B,1000)
    a = np.linspace(0,a*B,1000)
    ax = plt.subplot(111,polar = True)
    ax.plot(phi,a)
    ax.set_yticklabels([])
    plt.show()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("320x280")
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady = 20,padx = 60,fill = "both",expand = True)

label = customtkinter.CTkLabel(master = frame,text = "Введите параметры а и В")
label.pack(pady = 30,padx = 10)


input_a = customtkinter.CTkEntry(master = frame,placeholder_text="Параметр а")
input_a.pack(pady = 10 ,padx = 10)
input_B = customtkinter.CTkEntry(master = frame,placeholder_text="Параметр B")
input_B.pack(pady = 10 ,padx = 10)
def get_inputs():
    a,B = float(input_a.get()),float(input_B.get())
    Plot(a,B)

button = customtkinter.CTkButton(master=  frame,text = "Enter",command= get_inputs)
button.pack(pady = 10,padx = 10)


root.mainloop()