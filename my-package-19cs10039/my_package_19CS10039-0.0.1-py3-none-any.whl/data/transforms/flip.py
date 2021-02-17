#Imports
from PIL import Image

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

        if self.flip_type == 'horizontal':
            return image.transpose(Image.FLIP_LEFT_RIGHT)
                
        elif self.flip_type == 'vertical':
            return image.transpose(Image.FLIP_TOP_BOTTOM)