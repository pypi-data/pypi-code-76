#!/usr/bin/env python


import skimage.io as skio
import numpy as np
from scipy import ndimage

class Show():
    def __init__(self, data, mode):
        if '.npy' in data:
            self.data = np.load(data)
            if self.data.shape[0] == 1:
                self.data = self.data[0]
        else:
            self.data = data
        self.mode = mode 
    
    def single(self, layer, channel):
        data = np.copy(self.data)
        if len(self.data.ndim) == 3:
            if data.shape[2] * 5 < data.shape[1]:
                data = self.data[:,:, int(channel)]
            else:
                data = self.data[int(layer), :, :]
        elif len(self.data.ndim) == 4:
            data = self.data[int(layer), :, :, int(channel)]
        return data
            
    def show(self, layer, channel):
        data = self.single(layer, channel)
        skio.imshow(data, cmap = 'gray')
        skio.show()
        
    def smooth(self, data, alpha = 0.3, truncate = 5.0):
        return ndimage.filters.gaussian_filter(data, alpha, order = 0, output = None, mode = 'reflect', cval = 0.0, truncate = truncate)

    def out(self, layer, channel):
        data = self.single(layer, channel)
        for i in range(len(data)):
            for j in range(len(data[i])):
                print(data[i][j], end = ' ')
            print()
        print()
        
        