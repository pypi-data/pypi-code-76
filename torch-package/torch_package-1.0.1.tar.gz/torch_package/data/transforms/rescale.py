#Imports
import numpy as np
from PIL import Image

class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple (W,H)or int): Desired output size. If tuple, output is
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
        width, height = image.shape[1] , image.shape[0]
        image = Image.fromarray(image)
        if isinstance(self.output_size , int):
            if width < height:
                aspect_ratio = height/width
                width = self.output_size
                height = round(aspect_ratio * width)
                im = image.resize((width,height))
                im = np.array(im)
            else:
                aspect_ratio = width/height
                height = self.output_size
                width = round(aspect_ratio * height)
                im = image.resize((width,height))
                im = np.array(im)
            return im
        else:
            im = image.resize(self.output_size)
            im = np.array(im)
            return im


# rescale = RescaleImage(240)

# img = np.array(Image.open('./data/imgs/0.jpg'))
# im = rescale(img)
# print(im.shape)
# image = Image.fromarray(im)
# image.save('rescale.jpg')
 