#Imports
from PIL import Image, ImageFilter
from PIL.Image import fromarray
import numpy as np


class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''
        

        # Write your code here
        self.radius=int(radius)
        

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''

        # Write your code here
        img = image.filter(ImageFilter.GaussianBlur(radius=self.radius))
        return img
