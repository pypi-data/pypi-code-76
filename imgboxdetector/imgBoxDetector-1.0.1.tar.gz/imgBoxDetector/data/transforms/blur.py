#Imports
from PIL import Image, ImageFilter  
# from scipy.ndimage.filters import gaussian_filter
import numpy as np

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''

        # Write your code here
        self.radius = radius        

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''

        # Write your code here
        # return gaussian_filter(image , sigma = self.radius)
        return np.array(Image.fromarray(image).filter(ImageFilter.GaussianBlur(radius=self.radius)))

# blurrer = BlurImage(2)

# img = Image.open("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/sample_imgs/bbox.png")
# blurredImage =Image.fromarray(blurrer(np.array(img)))
# blurredImage.show()
