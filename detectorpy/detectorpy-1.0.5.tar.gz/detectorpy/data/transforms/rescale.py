#Imports
import numpy as np
from PIL import Image
from PIL.Image import fromarray


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

        # Write your code here

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''
    
        # Write your code here
        height = image.shape[0]
        width = image.shape[1]
        im = fromarray(image)
        if(isinstance(self.output_size,int)):
            if(height > width):
                ar = height/width
                width = self.output_size
                height = round(ar*width)
                im = im.resize((width, height))
                im = np.array(im)
            else:
                ar = width/height
                height = self.output_size
                width = round(ar*height)
                im = im.resize((width, height))
                im = np.array(im)
        else:
            im = im.resize((width, height))
            im = np.array(self.output_size)
        return im