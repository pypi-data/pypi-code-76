#Imports
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
        self.type = flip_type
        # Write your code here

        
    def __call__(self, image):
        if(self.type == 'horizontal'):
            return np.flip(image, axis = 0)
        elif(self.type == 'vertical'):
            return np.flip(image, axis = 1)
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
