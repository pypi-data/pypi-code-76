#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:42:15 2020

@author: kuangmeng
"""
import os
import SimpleITK as sitk
import skimage.io as skio
from skimage.transform import resize
import numpy as np
sys.path.append("..")
from utils.tonpy import SaveDataset
import platform

class LoadMMWHS():
    def __init__(self, data_dir, mode_list):
        self.data_dir = data_dir
        self.mode_list = mode_list
        self.data_set = []
        self.sysstr = platform.system()
        self.datadict = {}
        self.labeldict = {}
        self.generateDict()

    def generateDict(self):
        filelist = os.listdir(self.data_dir)
        for file in filelist:
            if 'nii' in file:
                if 'label' in file:
                    self.labeldict[int(file.split('_')[2])] = os.path.join(self.data_dir, file)
                else:
                    self.datadict[int(file.split('_')[2])] = os.path.join(self.data_dir, file)
    
    def read(self):
        keys = self.datadict.keys()
        for item in keys:
            itemdict = {}
            itemdict['image'] = self.datadict[item]
            itemdict['label'] = self.labeldict[item]
            self.data_set.append(itemdict)
        return self.data_set
    
if __name__ == '__main__':
    data_dir = './MMWHS'
    processed_dir = './processed/mmwhs'
    mode_list = ['image', 'label']
    data_set = LoadMMWHS(data_dir, mode_list).read()
    print(len(data_set))
    for item in mode_list:
        sd = SaveDataset(data_set, item, processed_dir, (120, 128, 128))
        sd.make()
        sd.save()
        print(item)
    
    
    
    
    
    
    
    
    