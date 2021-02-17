#Imports
from PIL import Image, ImageOps
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
        self.flip_type = flip_type
        # Write your code here

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        # Write your code here
        if self.flip_type == 'horizontal':
            # print(25)
            return np.array(ImageOps.mirror(Image.fromarray(image)))
        elif self.flip_type == 'vertical':
            # print(35)
            return np.array(ImageOps.flip(Image.fromarray(image)))
       

# img = Image.open("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/sample_imgs/bbox.png")
        

# horizontalFlipper = FlipImage('horizontal')
# verticalFlipper = FlipImage('vertical')

# flippedImage = Image.fromarray(horizontalFlipper(np.array(img)))
# flippedImage.show()


# flippedImage = Image.fromarray(verticalFlipper(np.array(img)))
# flippedImage.show()