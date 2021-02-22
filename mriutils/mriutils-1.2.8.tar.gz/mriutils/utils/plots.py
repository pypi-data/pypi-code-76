#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt  

class Plots():
    def __init__(self, x_val, y_val, x_range, y_range, title = None, x_label = None, y_label = None):
        self.x_val = x_val
        self.y_val = y_val
        self.x_range = x_range
        self.y_range = y_range
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def draw(self):
        line = plt.plot(self.x_val, self.y_val)
        x, y = self.x_range, self.y_range
        plt.plot(self.x_val, self.y_val)
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.legend()
        plt.show()
    