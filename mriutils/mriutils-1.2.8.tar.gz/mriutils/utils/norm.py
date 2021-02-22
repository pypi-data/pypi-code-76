#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""

import numpy as np
from keras.utils import np_utils

class Normalization():
    def __init__(self, data, mode, classes, customization = None):
        self.data = data
        self.mode = mode
        self.classes = classes
        self.customization = customization

    def run(self):
        data = self.data
        if self.mode == 'data':
            if np.max(data) > 1:
                data /= 255
            data -= data.mean()
            data /= data.std() 
        elif self.mode == 'label':
            data = np.around(data)
            data = np_utils.to_categorical(data, self.classes)
        elif self.mode == 'pred':
            data = np.resize(data, (data.shape[1], data.shape[2], data.shape[3], data.shape[4]))
            data = np.argmax(data, -1)
        elif self.mode == 'test':
            data = np.argmax(data, -1)
        else:
            if self.customization != None:
                data = self.customization(data)
        return data

    
    
    
    
    
    
    
    
    
    