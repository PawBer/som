from network import SOM
import tkinter as tk
from random import random  

NEURON_SIZE: int = 5

def update():
    x, y = random(), random()

    if (abs((x - 0.5) / 0.5) + abs((y - 0.5) / 0.5)) <= 1:
        som.learn([x, y])

    som.draw(canvas, NEURON_SIZE)

    root.after(1, update)

if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    som = SOM(15, 15, 2, 0.15, 0.99999, 0.999)

    root.after(1, update)

    root.mainloop()