# Imports
from PIL import Image
import numpy as np


class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''
    data = None
    scale_img = None
    out_sz = None

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''
        self.out_sz = output_size
        # Write your code here

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''
        self.data = Image.fromarray(image)
        self.og_size=(self.data.size)
        self.aspect_ratio=self.og_size[0]/self.og_size[1]    
        if(isinstance(self.out_sz,int)):
            if (self.og_size[0]<self.og_size[1]):
                self.scale_img=self.data.resize((self.out_sz,int(self.out_sz/self.aspect_ratio)))
            else:
                self.scale_img=self.data.resize((int(self.out_sz*self.aspect_ratio),self.out_sz))
                
        else:
            self.scale_img=self.data.resize(self.out_sz)
        # Write your code here
        self.scale_img=np.asarray(self.scale_img)
        return self.scale_img


# test=RescaleImage(50) #-> test an image with adifferent aspect ratio 
# arr=test(np.asarray(Image.open('./test_img.jpeg')))
# img=Image.fromarray(arr)
# img.show()
