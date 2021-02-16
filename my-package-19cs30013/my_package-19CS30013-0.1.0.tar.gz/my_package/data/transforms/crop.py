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
        _, y, x = image.shape
        cropy = self.shape[0]
        cropx = self.shape[1]

        if self.crop_type == 'center':
            startx = x // 2
            starty = y // 2
        else:
            startx = np.random.randint(x)
            starty = np.random.randint(y)
            
            while(starty < cropy // 2 or starty > y - cropy // 2):
                starty = np.random.randint(y)
            
            while(startx < cropx // 2 or startx > x - cropx // 2):
                startx = np.random.randint(x)

        
        startx -= cropx // 2
        starty -= cropy // 2

        return image[:,starty:starty+cropy,startx:startx+cropx]

        

 