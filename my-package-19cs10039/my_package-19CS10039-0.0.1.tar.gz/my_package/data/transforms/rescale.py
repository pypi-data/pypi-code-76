#Imports
from PIL import Image

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
        self.output_size = output_size


    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here
        x, y = image.size
        new_x = None
        new_y = None

        if type(self.output_size) == int:
            if y > x:
                new_x = self.output_size
                new_y = y * new_x // x

            else:
                new_y = self.output_size
                new_x = x * new_y // y
        else:
            new_y, new_x = self.output_size

        return image.resize((new_x, new_y), Image.ANTIALIAS)