#Imports
from PIL import Image, ImageFilter
from PIL.Image import fromarray
import numpy as np


class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
            
        '''
        
        # Write your code here
        self.degrees=degrees

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        img = sample.rotate(self.degrees, Image.NEAREST, expand=1)
        return img