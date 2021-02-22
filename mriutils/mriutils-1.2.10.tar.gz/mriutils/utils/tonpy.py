#!/usr/bin/env python


import os
import SimpleITK as sitk
import skimage.io as skio
from skimage.transform import resize
import numpy as np
from PIL import Image

class SaveDataset():
    def __init__(self, data_set, data_type, save_path, new_shape):
        self.data_type = data_type
        self.data_set = data_set
        self.save_path = save_path
        self.save_file = data_type + '.npy'
        self.lens = len(data_set)
        self.new_shape = new_shape
        self.data = []
    
    def make(self):
        for i in range(self.lens):
            self.data.append(self.resizeData(self.readSingleNiiFile(self.data_set[i][self.data_type]), self.new_shape))
    
    def make_pngs(self):
        for i in range(self.lens):
            self.data.append(self.resizeData(self.readSinglePngFile(self.data_set[i]), self.new_shape))
    
    def save(self):
        np.save(os.path.join(self.save_path, self.save_file), self.data)
        
    def readSingleNiiFile(self, nii_path):
        if 'nii' in nii_path:
            img = sitk.ReadImage(nii_path)
            data = sitk.GetArrayFromImage(img)
            return data
        else:
            return []
    
    def readSinglePngFile(self, png_path):
        if 'png' in png_path:
            I = Image.open(png_path)
            data = np.array(I)
            return data
        else:
            return []
    
    def showSingleMRI(self, no, frame):
        skio.imshow(self.data[int(no)][int(frame)], cmap = 'gray')
        skio.show()

    def resizeData(self, data, new_shape = (10, 256, 256), order = 3):
        print(data.shape)
        if len(data) > 0:
            data = resize(data, new_shape, order = order, mode='edge')
            # data -= data.mean()
            # data /= data.std()
        return data
    
    
    
    