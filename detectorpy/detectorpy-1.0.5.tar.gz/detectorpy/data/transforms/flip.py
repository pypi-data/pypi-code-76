#Imports
import numpy as np
from PIL import Image
from PIL.Image import fromarray


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
        self.flip_type = flip_type
        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        ''' 

        # Write your code here
        im = fromarray(image)
        if self.flip_type == 'vertical':
            out = im.transpose(Image.FLIP_TOP_BOTTOM)
            im = np.array(out)
        else:
            out = im.transpose(Image.FLIP_LEFT_RIGHT)
            im = np.array(out)
        return im


