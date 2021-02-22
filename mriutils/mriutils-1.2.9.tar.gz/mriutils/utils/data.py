#!/usr/bin/env python


import numpy as np

class Data():
    def __init__(self, data):
        self.data = data

    def save(self, save_path):
        np.save(save_path, np.array(self.data))

    def load(self, load_path):
        self.data = np.load(load_path)
        