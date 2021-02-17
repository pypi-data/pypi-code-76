#Imports
from PIL import Image
import numpy as np

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

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        return np.array(Image.fromarray(image).rotate(self.degrees, Image.NEAREST, expand = 1))

# img = Image.open("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/sample_imgs/bbox.png")
        
# rotator = RotateImage(45)
# rotatedImage = Image.fromarray(rotator(np.array(img)))
# rotatedImage.show()

# rotator = RotateImage(90)
# rotatedImage = Image.fromarray(rotator(np.array(img)))
# rotatedImage.show()
