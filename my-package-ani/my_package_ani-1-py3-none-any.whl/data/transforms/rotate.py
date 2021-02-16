#Imports
from PIL import Image
import numpy as np
from scipy.ndimage import rotate

class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''
    data = None
    rot_img = None
    deg=None
    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''
        self.deg=degrees
        # Write your code here

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        self.data=sample
        self.rot_img = rotate(self.data,self.deg, reshape=True)
        # Write your code here
        return self.rot_img

# test=RotateImage(45)
# arr=test(np.asarray(Image.open('./test_img.jpeg')))
# img=Image.fromarray(arr)
# img.show()
    
