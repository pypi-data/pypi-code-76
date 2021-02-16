#Imports
import numpy as np
from PIL import Image
from PIL.Image import fromarray


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
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        imageheight = image.shape[0]
        imagewidth = image.shape[1]
        dheight = self.shape[0]
        dwidth = self.shape[1]
        if self.crop_type == 'center':
            top = round((imageheight - dheight)/2)
            left = round((imagewidth - dwidth)/2)
            right = dwidth + left
            down = dheight + top
            newimage = image[top:down , left:right]
            return newimage
        else:
            newimage = image[0:dheight , 0:dwidth]
            return newimage

        

 