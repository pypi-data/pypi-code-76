#Imports
from PIL import Image, ImageFilter
from PIL.Image import fromarray
import numpy as np

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

        # Write your code here
        self.output_size=output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here
        initH=image.size[0]
        initW=image.size[1]
        if isinstance(self.output_size, int):
            if initH>=initW:
                finW = self.output_size*initW
                finH = round((initH*finW)/initW)
            else:
                finH = self.output_size
                finW = round((initW*finH)/initH)
            img=image.resize((int(finW), int(finH)))
        elif isinstance(self.output_size, float):
            finW = initW*self.output_size
            finH = initH*self.output_size
            img=image.resize((int(finH), int(finW)))
        else:
            img = image.resize(self.output_size)
        return img
