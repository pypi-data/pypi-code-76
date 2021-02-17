#Imports
from PIL import Image, ImageFilter
from scipy.ndimage.filters import gaussian_filter
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
        blur_image = gaussian_filter(image , sigma = self.radius)
        return blur_image
        

# blur = BlurImage(2)

# img = np.array(Image.open('./data/imgs/0.jpg'))
# im = blur(img)

# image = Image.fromarray(im)
# image.save('blur.jpg')