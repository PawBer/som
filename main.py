from network import SOM
import tkinter as tk
from random import random
from typing import List   

def update():
    input: List[float] = [random() for _ in range(2)]
    som.learn(input)
    som.draw(canvas, neuron_size)
    root.after(10, update)

if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack()

    som = SOM(10, 2, 0.1, 0.9999, 0.999)

    neuron_size = 5
    neuron_padding = 1000 / len(som.neurons)
        
    root.after(10, update)

    root.mainloop()