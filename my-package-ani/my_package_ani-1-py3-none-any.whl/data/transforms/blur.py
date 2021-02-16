# Imports
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''
    data = None
    blurred = None
    rad=None
    def __init__(self, radius=3):
        '''
            Arguments:
            radius (int): radius to blur
        '''
        # Write your code here
        self.rad=radius

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''
        # Write your code here
        self.data = image
        self.blurred = gaussian_filter(self.data, sigma=(self.rad,self.rad,0))
        return self.blurred

# test=BlurImage(20)
# blurarr=test(np.asarray(Image.open('./test_img.jpeg')))
# blurimg=Image.fromarray(blurarr)
# blurimg.show()
    
