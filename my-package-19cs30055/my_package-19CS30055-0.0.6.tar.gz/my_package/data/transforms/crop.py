#Imports
import numpy as np

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        self.crop_type = crop_type
        self.shape = shape
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        y,x,_ = image.shape
        cropx = self.shape[1]
        cropy = self.shape[0]
        if(self.crop_type == 'center'):
            startx = x//2-(cropx//2)
            starty = y//2-(cropy//2)    
            return image[starty:starty+cropy,startx:startx+cropx]
        elif(self.crop_type == 'random'):
            startx = np.random.randint(0,x-cropx+1)
            starty = np.random.randint(0,y-cropy+1)
            return image[starty:starty+cropy,startx:startx+cropx]
