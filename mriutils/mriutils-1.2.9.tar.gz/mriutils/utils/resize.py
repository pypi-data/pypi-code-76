#!/usr/bin/env python


import numpy as np
from skimage import transform

class Resize:
    def __init__(self, data, mode, new_shape):
        if '.npy' in data:
            self.data = np.load(data)
        else:
            self.data = data
        self.mode = mode
        self.new_shape = new_shape
        
    def run(self):
        data_new = transform.resize(self.data, self.new_shape)
        if self.mode == 'label':
            data_new = np.around(data_new)
        self.data = np.array(data_new)
        return self.data
