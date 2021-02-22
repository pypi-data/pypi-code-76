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

class LoadACDC():
    def __init__(self, data_dir, mode_list):
        self.data_dir = data_dir
        self.mode_list = mode_list
        self.data_set = []
        self.sysstr = platform.system()
    
    def readSinglePatient(self, patient_path):
        cfg_file = os.path.join(patient_path, 'Info.cfg')
        config = {}
        with open(cfg_file) as f:
            for line in f.readlines():
                config[line.split(':')[0]] = line.split(':')[1].strip()
        file_dict = {}
        patient_name = ''
        if self.sysstr == 'Windows':
            patient_name = patient_path.split('\\')[-1] if len(patient_path.split('\\')[-1]) > 0 else patient_path.split('\\')[-2]
        else:
            patient_name = patient_path.split('/')[-1] if len(patient_path.split('/')[-1]) > 0 else patient_path.split('/')[-2]
        for i in range(len(self.mode_list)):
            if 'GT' in self.mode_list[i]:
                file_dict[self.mode_list[i]] = os.path.join(patient_path, 
                                                           patient_name + 
                                                           '_frame'+ 
                                                           '%02.0d' % (int(config[self.mode_list[i - 1]])) + 
                                                           '_gt.nii.gz')
            else:
                file_dict[self.mode_list[i]] = os.path.join(patient_path, 
                                                           patient_name + 
                                                           '_frame'+ 
                                                           '%02.0d' % (int(config[self.mode_list[i]])) + 
                                                           '.nii.gz')
        return file_dict
    
    def read(self):
        dir_list = os.listdir(self.data_dir)
        for patient_path in dir_list:
            if os.path.isdir(os.path.join(self.data_dir, patient_path)) and 'patient' in patient_path:
                self.data_set.append(self.readSinglePatient(os.path.join(self.data_dir, patient_path)))
        return self.data_set
    
if __name__ == '__main__':
    data_dir = './ACDC'
    processed_dir = './processed/acdc'
    mode_list = ['ED', 'ED_GT', 'ES', 'ES_GT']
    data_set = LoadACDC(data_dir, mode_list).read()
    for item in mode_list:
        sd = SaveDataset(data_set, item, processed_dir, (10, 128, 128))
        sd.make()
        sd.save()
        print(item)
    
    
    
    
    
    
    
    
    