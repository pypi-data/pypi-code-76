#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
sys.path.append("..")
from utils.tonpy import SaveDataset

class LoadPNGS():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.dataset_list = self.read_dir()
        self.data = []
    
    def read(self):
        dir_list = os.listdir(self.data_dir)
        dataset_list = []
        for item_path in dir_list:
            dataset_list.append(os.path.join(self.data_dir, item_path))
        return dataset_list
    

if __name__ == '__main__':
    data_dir = './PNGS/training'
    processed_dir = './processed'
    data_set = LoadPNGS(data_dir).read()
    sd = SaveDataset(data_set, 'train', processed_dir, (1, 256, 256))
    sd.make_pngs()
    sd.save()
    
    
    
    
    
    
    
    
    