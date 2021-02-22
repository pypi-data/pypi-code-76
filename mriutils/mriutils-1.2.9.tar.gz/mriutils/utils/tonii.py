#!/usr/bin/env python


import skimage.io as skio
from skimage.transform import resize
import nibabel as nib


class SaveNiiFile():
    def __init__(self, data, save_path, new_shape = (10, 256, 256), order = 3):
        self.data = data
        self.save_path = save_path
        self.new_shape = new_shape
    
    def showSingleMRI(self, frame):
        skio.imshow(self.data[int(frame)], cmap = 'gray')
        skio.show()

    def resizeData(self):
        if len(self.data) > 0:
            self.data = resize(self.data, self.new_shape, order = self.order, mode='edge')
    
    def load_nii(self, img_path):
        nimg = nib.load(img_path)
        return nimg.get_data(), nimg.affine, nimg.header

    def save_nii(self, data = None, save_path = None, affine = None, header = None):
        if data == None:
            data = self.data
        if save_path == None:
            save_path = self.save_path
        nimg = nib.Nifti1Image(data, affine = affine, header = header)
        nimg.to_filename(save_path)
    
    
    