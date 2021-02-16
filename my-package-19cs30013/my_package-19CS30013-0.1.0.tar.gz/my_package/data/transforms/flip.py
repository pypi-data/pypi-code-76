import cv2
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

        if flip_type == 'horizontal':
            self.flip_type = 1
        else:
            self.flip_type = 0

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        img = image.transpose((1, 2, 0))
        img_flip = cv2.flip(img, self.flip_type)
        img_flip = img_flip.transpose((2, 0, 1))

        return img_flip
        

       