#Imports
import numpy as np
from skimage.transform import resize
import math

class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''
        image_resized = np.array([])
        if(isinstance(self.output_size, tuple)):
            image_resized = resize(image, self.output_size)
        elif(isinstance(self.output_size, int)):
            h, w, _ = image.shape
            if(w < h):
                image_resized = resize(image, (math.floor(h*self.output_size/w), self.output_size))
            else:
                image_resized = resize(image, (self.output_size, math.floor(w*self.output_size/h)))    
        return image_resized
