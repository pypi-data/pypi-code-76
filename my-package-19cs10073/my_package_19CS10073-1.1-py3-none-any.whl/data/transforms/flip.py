#Imports
import numpy as np

class FlipImage(object):
    '''
        Flips the image.
    '''

    def __init__(self, flip_type = 'horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''
        self.flip_type = flip_type

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        image_flipped = np.array([])
        if(self.flip_type == 'horizontal'):
            image_flipped = np.flip(image, axis = 0)
        elif(self.flip_type == 'vertical'):
            image_flipped = np.flip(image, axis = 1)
        
        return image_flipped