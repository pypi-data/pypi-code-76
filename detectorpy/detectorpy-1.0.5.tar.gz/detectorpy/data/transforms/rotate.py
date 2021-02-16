#Imports
import numpy as np
from PIL import Image
from PIL.Image import fromarray


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
        self.degrees = degrees

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        im = fromarray(sample)
        angle = self.degrees
        out = im.rotate(angle,expand=True)
        im = np.array(out)
        return im