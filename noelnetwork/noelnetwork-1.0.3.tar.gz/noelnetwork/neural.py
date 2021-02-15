import random as r
import ast as a
import math
import numpy as np
import copy
import time
from tkinter import *
from statistics import mean

class Neural:

    def __init__(self, nodes):
        self.weights = {}
        self.change = {}
        self.nodes = []
        for layer in nodes:
            new_layer = []
            for neuron in layer:
                node_dict = {"output" : 0.0, "weights" : [], "layer":0}
                new_layer.append(node_dict)
            self.nodes.append(new_layer)
            
        for i in range(len(nodes) - 1):
            for k in range(len(nodes[i+1])):
                self.generate_weights(i+1,k, i)

        for layer, i in zip(self.nodes, range(len(self.nodes))):
            for node in layer:
                node["layer"] = i

    def generate_weights(self, node_i, node_k, prev_layer):
        for n in range(len(self.nodes[prev_layer])):
            self.nodes[node_i][node_k]["weights"].append(0.0)

    def input(self, inputs):
        for i in range(len(self.nodes[0])):
            self.nodes[0][i]["output"] = float(inputs[i])
        self.calculate()
        out = list()
        for o in self.nodes[-1]:
            out.append(o["output"])
        return out

    def calculate(self):
        for i in range(len(self.nodes) - 1):
            for k in range(len(self.nodes[i + 1])):
                ergebnis = []
                for n in range(len(self.nodes[i])):
                    weight = self.nodes[i+1][k]["weights"][n]
                    v = self.nodes[i][n]["output"] * weight
                    ergebnis.append(v)
                calculated_value = self.sigmoid(mean(ergebnis))
                self.nodes[i+1][k]["output"] = calculated_value
                
    def sigmoid(self, x):
        if x < 0: return np.exp(x) / (1 + np.exp(x))
        else: return 1 / (1+ np.exp(-x))

    def shuffle(self):
        for layer in range(len(self.nodes)):
            for node in range(len(self.nodes[layer])):
                for weight in range(len(self.nodes[layer][node]["weights"])):
                    rndm_float = r.randint(-100,100) / 100
                    self.nodes[layer][node]["weights"][weight] = rndm_float

    def save(self, file_name):
        file.write(str(self.nodes))

    def load(self, file):
        self.nodes = a.literal_eval(file.read())

    def shuffle_amount(self, amount):
        for layer in range(len(self.nodes)):
            for node in range(len(self.nodes[layer])):
                for weight in range(len(self.nodes[layer][node]["weights"])):
                    self.nodes[layer][node]["weights"][weight] += r.randint(-amount, amount) / 100

    def derivative(self, output):
        return output * (1.0 - output)

    def backpropagation(self, expected):
        for i in reversed(range(len(self.nodes))):
            layer = self.nodes[i]
            errors = []
            if i != len(self.nodes)-1:
                for j in range(len(layer)):
                    error = 0.0
                    for neuron in self.nodes[i + 1]:
                        error += (neuron['weights'][j] * neuron['delta'])
                    errors.append(error)
            else:
                for j in range(len(layer)):
                    neuron = layer[j]
                    errors.append(expected[j] - neuron['output'])
            for j in range(len(layer)):
                self.nodes[i][j]['delta'] = errors[j] * self.derivative(self.nodes[i][j]['output'])
                
    def update_weights(self, row, l_rate):
        for i in range(1, len(self.nodes)):
            inputs = row[:-1]
            if i != 0:
                inputs = [neuron['output'] for neuron in self.nodes[i-1]]
            for k in range(len(self.nodes[i])):
                for j in range(len(inputs)):
                    self.nodes[i][k]['weights'][j] += l_rate * self.nodes[i][k]["delta"] * inputs[j]

    def load_training_data(self, file):
        lines = file.readlines()
        inputs, outputs = [], []
        for line in lines:
            inputs.append(line.replace("\n", "").split("=")[0].split(","))
            outputs.append(line.replace("\n", "").split("=")[1].split(","))

        for i in range(len(inputs)):
            for inp in range(len(inputs[i])):
                inputs[i][inp] = int(inputs[i][inp])
            for out in range(len(outputs[i])):
                outputs[i][out] = int(outputs[i][out])
        return inputs, outputs

    def get_total_score(self, inputs, outputs):
        score, max_score = 0, len(inputs)
        for i, o in zip(inputs, outputs):
            out = self.input(i)
            if out.index(max(out)) == o.index(max(o)):
                score += 1
        return score, max_score
     
    def train(self, learning_rate, cycles, inputs, expected, print_status = False):
        all_times = []
        for cycle in range(cycles):
            start_time = time.time()
            sum_error = 0
            for row in range(len(inputs)):
                outputs = self.input(inputs[row])
                sum_error += sum([(expected[row][i]-outputs[i])**2 for i in range(len(expected[row]))])
                self.backpropagation(expected[row])
                self.update_weights(inputs[row], learning_rate)
            all_times.append(time.time() - start_time)
            time_diff = mean(all_times) * (cycles - cycle)
            minutes = math.floor(time_diff / 60)
            seconds = round(time_diff % 60)
            if print_status:
                print(f"error: {round(sum_error,10):15} | cycle: {cycle:4} | approx. time left: {minutes}m {seconds}s")

    def show(self, size=[1400,700]):
        nodes = self.nodes
        if type(size) != list or len(size) != 2:
            raise Exception("size expected to be list: (x,y)")
        
        root  = Tk()

        canvas = Canvas(root, width=size[0], height=size[1])
        canvas.pack()

        max_link = self.get_max(nodes)
        for i in range(1, len(nodes)):
            for k in range(len(nodes[i])):
                for j in range(len(nodes[i][k]["weights"])):
                    x1, y1 = self.get_node_coords(nodes, i, k, size)
                    x2, y2 = self.get_node_coords(nodes, i-1, j, size)
                    c, w = self.get_color(nodes[i][k]["weights"][j], max_link)
                    canvas.create_line(x1, y1, x2, y2, fill=c, width=w)

        for node, x_pos in zip(nodes, self.get_layer_pos(nodes, size[0])):
            for y_pos in self.get_layer_pos(node, size[1]):
                self.circle(canvas, x_pos, y_pos, 30)

        mainloop()

    def get_max(self, nodes):
        maximal = 0
        for i in range(1, len(nodes)):
            for k in range(len(nodes[i])):
                for j in range(len(nodes[i][k]["weights"])):
                    if abs(nodes[i][k]["weights"][j]) > maximal:
                        maximal = abs(nodes[i][k]["weights"][j])
        return maximal

    def get_color(self, value, max_link):
        if max_link == 0: max_link = 1
        percent = 100 * abs(value) / max_link
        if value > 0: out = "#0000" + format(int(percent)*2, '#04x')[2:]
        if value <= 0: out = "#" + format(int(percent)*2, '#04x')[2:] + "0000"
        return out, percent / 15

    def get_node_coords(self, nodes, i, node, size):
        x = (i + 1) * (size[0] // (len(nodes) + 1))
        y = (node + 1) * (size[1] // (len(nodes[i]) + 1))
        return [x,y]

    def circle(self, canvas,x,y, r):
        id = canvas.create_oval(x-r,y-r,x+r,y+r, width=3)
        return id

    def get_layer_pos(self, nodes, size):
        step = size // (len(nodes) + 1)
        output_layer_pos = []
        for i in range(len(nodes)):
            output_layer_pos.append(step * (i + 1))
        return output_layer_pos
