#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
import h5py
import numpy as np
from skimage.transform import resize


class LoadH5():
    def __init__(self, data_dir, save_path, new_shape = (50, 128, 128, 4)):
        self.data_dir = data_dir
        self.data = {'data':[], 'label': []}
        self.new_shape = new_shape
        self.save_path = save_path
        
    def readSingleH5(self, item_path):
        f = h5py.File(item_path, 'r')
        # keyset = f.keys() #get set of cine slice names enclosed in the file
        # keylist = list(f) #get list of cine slice names enclosed in the file
        key = 'MID' #define the name of the cine slice requested
        if key not in f.keys():
            print(item_path)
            print(f.keys())
            return [], []
        img = f[key]['image'][:] #get the 50*512*512*4 image array data as img
        # the label data will be a float array. You may want to normalise the data before use
        lbl = f[key]['label'][:] #get the 50*512*512 label array data as lbl
        # the label data will be a binary (0/1) float array
        f.close()
        return img, lbl
    
    def read(self):
        dir_list = os.listdir(self.data_dir)
        for item_path in dir_list:
            if os.path.exists(os.path.join(self.data_dir, item_path)) and '.h5' in item_path:
                img, lbl = self.readSingleH5(os.path.join(self.data_dir, item_path))
                if len(img) > 0 and len(lbl) > 0:
                    self.data['data'].append(self.resizeData(data = img, new_shape = self.new_shape))
                    self.data['label'].append(self.resizeData(data = lbl, new_shape = (self.new_shape[0], self.new_shape[1], self.new_shape[2], 1)))
        return self.data

    def resizeData(self, data, new_shape =(50, 128, 128, 4), order = 3):
        if len(data) > 0:
            data = resize(data, new_shape, order = order, mode='edge')
        return data

    def save(self):
        np.save(os.path.join(self.save_path, 'ic_data'), self.data['data'])
        np.save(os.path.join(self.save_path, 'ic_label'), self.data['label'])

    
if __name__ == '__main__':
    lh5 = LoadH5('/Users/kuangmeng/Documents/SpyderProjects/mengutils/mengutils', './')
    data = lh5.read()
    lh5.save()
    
    
    
    
    
    
    
    
    
    