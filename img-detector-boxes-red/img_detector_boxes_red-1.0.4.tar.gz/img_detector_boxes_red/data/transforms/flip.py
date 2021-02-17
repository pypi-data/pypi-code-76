#Imports
from PIL import Image, ImageFilter
from PIL.Image import fromarray
import numpy as np

class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''

        # Write your code here
        self.flip_type=str(flip_type)

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if self.flip_type=="horizontal":
            img = image.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            img = image.transpose(Image.FLIP_LEFT_RIGHT)
        return img