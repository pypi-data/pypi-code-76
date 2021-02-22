#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 00:36:42 2020

@author: kuangmeng
"""

import numpy as np
import os
from sklearn.model_selection import train_test_split

class LoadData():
    def __init__(self, npy_dir, test_ratio = 0.3):
        self.npy_dir = npy_dir
        self.test_ratio = test_ratio
        self.lens = 0
        self.mode_list = self.generateMode()
        self.data_dict = {}
        self.train = {}
        self.test = {}
        
    def generateMode(self):
        mode_list = []
        file_list = os.listdir(self.npy_dir)
        for file in file_list:
            if '.npy' in file and file[0] != '.':
                mode_list.append(file.split('.')[0])
        return mode_list
    
    def load_data_dict(self):
        for mode in self.mode_list:
            self.data_dict[mode] = np.load(os.path.join(self.npy_dir, mode + '.npy'))
            if self.lens == 0:
                self.lens = self.data_dict[mode].shape[0]
            
    def data_split(self):
        new_list = [i for i in range(self.lens)]
        train, test = train_test_split(new_list, test_size = self.test_ratio, random_state = 1024)
        for mode in self.mode_list:
            self.train[mode] = self.data_dict[mode][train]
            self.test[mode] = self.data_dict[mode][test]
        return self.train, self.test, self.mode_list
        
if __name__ == '__main__':
    npy_dir = './processed_ACDC'
    ld = LoadData(npy_dir)
    ld.load_data_dict()
    ld.data_split()
    
        
        
            
            
            
            
            
    