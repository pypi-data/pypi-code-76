#Imports
from PIL import Image
import numpy as np


class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        height, width = image.shape[0] , image.shape[1]
        new_width = self.shape[1]
        new_height = self.shape[0]
        if self.crop_type == 'center':
            left = round((width - new_width)/2)
            top = round((height - new_height)/2)
            x_right = round(width - new_width) - left
            x_bottom = round(height - new_height) - top
            right = width - x_right
            bottom = height - x_bottom
            im_crop = image[top:bottom , left:right]
            return im_crop
        else:
            im_crop = image[0: new_height , 0:new_width]
            return im_crop
        # Write your code here

        
# crop = CropImage([478,640] , 'random')

# img = np.array(Image.open('./data/imgs/0.jpg'))
# im = crop(img)

# image = Image.fromarray(im)
# image.save('crop.jpg')
 