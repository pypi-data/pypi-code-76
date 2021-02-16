# Imports

from PIL import Image
import numpy as np


class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''
    data = None
    crop_img = None
    crop_width = None
    crop_height = None
    crop_type = 1

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''
        if(crop_type != 'center'):
            self.crop_type = 0
        self.crop_height, self.crop_width = shape
        # Write your code here

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        self.data = Image.fromarray(image)
        self.img_width, self.img_height = (self.data.size)
        # print(self.img_width,self.img_height)
        if(self.crop_type == 1):
            self.crop_img = self.data.crop(((self.img_width - self.crop_width) // 2,
                                            (self.img_height -
                                             self.crop_height) // 2,
                                            (self.img_width + self.crop_width) // 2,
                                            (self.img_height + self.crop_height) // 2))
        else:
            left = np.random.randint(0, self.img_width - self.crop_width)
            upper = np.random.randint(0, self.img_height - self.crop_height)
            self.crop_img = self.data.crop(
                (left, upper, left+self.crop_width, upper+self.crop_height))
        self.crop_img = np.asarray(self.crop_img)
        return self.crop_img

# test=CropImage((200,100),'lol')
# lol=np.asarray(Image.open('./test_img.jpeg'))
# print(lol.shape)
# arr=test(lol)
# img=Image.fromarray(arr)
# img.show()
