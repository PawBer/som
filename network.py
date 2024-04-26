import random
from typing import List
from math import sqrt, exp
from tkinter import Canvas


class Neuron:
    def __init__(self, num_dimensions: int) -> None:
        self.weights: List[float] = [
            (random.random() - 0.5) * 0.01 + 0.5 for _ in range(num_dimensions)
        ]


class SOM:
    def __init__(
        self,
        width: int,
        height: int,
        num_dimensions: int,
        learning_rate: float,
        learning_rate_decay_rate: float,
        neighbour_radius_decay_rate: float,
    ) -> None:
        self.neurons: List[List[Neuron]] = []
        for i in range(height):
            self.neurons.append([])
            for _ in range(width):
                self.neurons[i].append(Neuron(num_dimensions))

        self.learning_rate = learning_rate
        self.neighbour_radius: float = sqrt(width * height) / 2
        self.neigbour_radius_decay_rate: float = neighbour_radius_decay_rate
        self.learning_rate_decay_rate: float = learning_rate_decay_rate

    def neighbour_function(self, distance: float) -> float:
        sigma: float = self.neighbour_radius
        return exp(-(distance**2) / (2 * sigma**2))

    def find_closest(self, input: List[float]):
        min_idx_i, min_idx_j = 0, 0
        min_dist: float = calculate_distance(
            self.neurons[min_idx_i][min_idx_j].weights, input
        )

        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[i])):
                dist: float = calculate_distance(self.neurons[i][j].weights, input)
                if dist < min_dist:
                    min_idx_i, min_idx_j = i, j
                    min_dist = dist

        return min_idx_i, min_idx_j

    def learn(self, input: List[float]) -> None:
        min_idx_i, min_idx_j = self.find_closest(input)

        for row_idx, row in enumerate(self.neurons):
            for neuron_idx, neuron in enumerate(row):
                grid_distance: float = sqrt(
                    (min_idx_i - row_idx) ** 2 + (min_idx_j - neuron_idx) ** 2
                )
                if grid_distance < self.neighbour_radius:
                    neigbourhood: float = self.neighbour_function(grid_distance)
                    neuron.weights = [
                        w + (x - w) * self.learning_rate * neigbourhood
                        for w, x in zip(neuron.weights, input)
                    ]

        self.learning_rate *= self.learning_rate_decay_rate
        self.neighbour_radius *= self.neigbour_radius_decay_rate

    def draw(self, canvas: Canvas, neuron_size: int) -> None:
        canvas.delete("all")

        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[i])):
                neuron = self.neurons[i][j]
                x = neuron.weights[0] * 1000
                y = neuron.weights[1] * 1000
                canvas.create_oval(
                    x - neuron_size,
                    y - neuron_size,
                    x + neuron_size,
                    y + neuron_size,
                    fill="blue",
                )
                if i + 1 < len(self.neurons):
                    x1: float = self.neurons[i + 1][j].weights[0] * 1000
                    y1: float = self.neurons[i + 1][j].weights[1] * 1000
                    canvas.create_line(x, y, x1, y1)
                if j + 1 < len(self.neurons[i]):
                    x1: float = self.neurons[i][j + 1].weights[0] * 1000
                    y1: float = self.neurons[i][j + 1].weights[1] * 1000
                    canvas.create_line(x, y, x1, y1)


def calculate_distance(a: List[float], b: List[float]) -> float:
    sum: float = 0.0
    for i, j in zip(a, b):
        sum += (i - j) ** 2
    return sqrt(sum)
