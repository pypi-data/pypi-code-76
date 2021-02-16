#Imports
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
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        h, w, _ = image.shape
        crop_h, crop_w = self.shape
        image_cropped = np.array([])
        start_h = None
        start_w = None

        if(self.crop_type == 'center'):
            start_h = h//2-(crop_h//2)
            start_w = w//2-(crop_w//2)    
            image_cropped = image[start_h : start_h + crop_h, start_w : start_w + crop_w]

        elif(self.crop_type == 'random'):
            start_h = np.random.randint(0, h - crop_h + 1)
            start_w = np.random.randint(0, w - crop_w + 1)
            image_cropped = image[start_h : start_h + crop_h, start_w : start_w + crop_w]
        
        return image_cropped
