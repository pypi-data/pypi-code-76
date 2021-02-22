#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
sys.path.append("..")
from utils.tonpy import SaveDataset

class LoadMRBrainS():
    def __init__(self, data_dir, mode_list):
        self.data_dir = data_dir
        self.mode_list = mode_list
        self.data_set = []
    
    def readSingleItem(self, item_path):
        file_dict = {}
        for i in range(len(self.mode_list)):
            file_name = os.path.join(item_path, str(self.mode_list[i]) + '.nii')
            if os.path.exists(file_name):
                file_dict[self.mode_list[i]] = file_name
            else:
                file_dict[self.mode_list[i]] = '-'
        return file_dict
    
    def read(self):
        dir_list = os.listdir(self.data_dir)
        for item_path in dir_list:
            if os.path.isdir(os.path.join(self.data_dir, item_path)):
                self.data_set.append(self.readSingleItem(os.path.join(self.data_dir, item_path)))
        return self.data_set
    
if __name__ == '__main__':
    '''
    labelfortraining - label
    T1_IR - data
    '''
    data_dir = './MRBrainS'
    processed_dir = './processed'
    mode_list = ['LabelsForTesting', 'LabelsForTraining', 'T1_1mm', 'T1_IR', 'T1', 'T2_FLAIR']
    from tonpy import SaveDataset
    data_set = LoadMRBrainS(data_dir, mode_list).read()
    for item in mode_list:
        sd = SaveDataset(data_set, item, processed_dir, (48, 256, 256))
        sd.make()
        sd.save()
        sd.showSingleMRI(0, 3)
        print(item)
    
    
    
    
    
    
    
    
    