#Imports
import numpy as np
from scipy.ndimage.filters import gaussian_filter
class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        self.radius = radius
        '''
            Arguments:
            radius (int): radius to blur
        '''


        # Write your code here
        

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''
        return (gaussian_filter(image, sigma=[self.radius, self.radius, 0]))


