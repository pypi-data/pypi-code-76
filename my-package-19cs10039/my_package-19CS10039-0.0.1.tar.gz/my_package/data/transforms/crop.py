#Imports
import numpy as np
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
        x, y = image.size
        cropy, cropx = self.shape

        if self.crop_type == 'center':
            startx = x//2 - (cropx//2)
            starty = y//2 - (cropy//2)
            return image.crop((startx, starty, startx+cropx, starty+cropy))
        else:
            startx = random.randint(0, (x - cropx + 1))
            starty = random.randint(0, (y - cropy + 1))
            return image.crop((startx, starty, startx+cropx, starty+cropy))