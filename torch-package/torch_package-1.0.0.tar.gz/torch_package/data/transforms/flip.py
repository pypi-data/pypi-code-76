#Imports
import numpy as np
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
        if self.flip_type == 'vertical':
            im = np.flip(image , axis = 0)
            return im
        else:
            im = np.flip(image , axis = 1)
            return im


# flip = FlipImage('vertical')

# img = np.array(Image.open('./data/imgs/0.jpg'))
# im = flip(img)

# image = Image.fromarray(im)
# image.save('flip.jpg')