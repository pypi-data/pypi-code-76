#Imports
import numpy as np
from PIL import Image
from PIL.Image import fromarray
import random

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.shape=shape
        self.crop_type=crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        imgH=image.size[0]
        imgW=image.size[1]
        cropH=self.shape[0]
        cropW=self.shape[1]
        if str(self.crop_type) == "center":
            top = round((imgH-cropH)/2)
            left = round((imgW-cropW)/2)
            right = cropW + left
            down = cropH + top
        else:
            top=random.randint(0, imgH-cropH)
            left=random.randint(0, imgW-cropW)
            right = cropW + left
            down = cropH + top
        img = image.crop((left, top, right, down))
        return img

        

 