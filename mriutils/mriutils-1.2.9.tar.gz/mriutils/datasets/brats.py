#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
import platform
sys.path.append("..")
from utils.tonpy import SaveDataset

class LoadBraTS():
    def __init__(self, data_dir, mode_list):
        self.data_dir = data_dir
        self.mode_list = mode_list
        self.data_set = []
        self.sysstr = platform.system()

    def readSingleItem(self, item_path):
        file_dict = {}
        item_name = ''
        if self.sysstr == 'Windows':
            item_name = item_path.split('\\')[-1] if len(item_path.split('\\')[-1]) > 0 else item_path.split('\\')[-2]
        else:
            item_name = item_path.split('/')[-1] if len(item_path.split('/')[-1]) > 0 else item_path.split('/')[-2]
        for i in range(len(self.mode_list)):
            file_name = os.path.join(item_path, item_name + '_%s' % (self.mode_list[i]) + '.nii.gz')
            if os.path.exists(file_name):
                file_dict[self.mode_list[i]] = file_name
            else:
                file_dict[self.mode_list[i]] = '-'
        return file_dict
    
    def read(self):
        dir_list = os.listdir(self.data_dir)
        for item_path in dir_list:
            if os.path.isdir(os.path.join(self.data_dir, item_path)) and 'BraTS' in item_path:
                self.data_set.append(self.readSingleItem(os.path.join(self.data_dir, item_path)))
        return self.data_set
    
if __name__ == '__main__':
    '''
    seg - label
    flair/t2 - data
    '''
    data_dir = './BraTS'
    processed_dir = './processed/brats/'
    mode_list = ['flair', 'seg', 't1', 't1ce', 't2']
    from tonpy import SaveDataset
    data_set = LoadBraTS(data_dir, mode_list).read()
    for item in mode_list:
        sd = SaveDataset(data_set, item, processed_dir, (155, 256, 256))
        sd.make()
        sd.save()
        print(item)
    
    
    
    
    
    
    
    
    