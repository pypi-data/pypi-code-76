#Imports
from  PIL import Image
import numpy as np
from random import randint

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


    # def cropCenter(self,pil_img):
    #     img_width, img_height = pil_img.size
    #     return pil_img.crop(((img_width - self.shape.second) // 2,
    #                         (img_height - self.shape.first) // 2,
    #                         (img_width + self.shape.second) // 2,
    #                         (img_height + self.shape.second) // 2))


    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        # Write your code here

        if self.crop_type == "center":
            img_width, img_height = Image.fromarray(image).size
            return np.array(Image.fromarray(image).crop(((img_width - self.shape[1]) // 2,
                            (img_height - self.shape[0]) // 2,
                            (img_width + self.shape[1]) // 2,
                            (img_height + self.shape[0]) // 2)))

        elif self.crop_type == "random":
            img_width, img_height = Image.fromarray(image).size
            new_height, new_width = self.shape
            left = randint(0, img_width-new_width)
            top = randint(0, img_height-new_height)
            right = left + new_width
            bottom = top + new_height
            return np.array(Image.fromarray(image).crop((left,top,right,bottom)))
            # assert img.shape[0] >= height
            # assert img.shape[1] >= width
            # assert img.shape[0] == mask.shape[0]
            # assert img.shape[1] == mask.shape[1]
            # x = random.randint(0, img.shape[1] - width)
            # y = random.randint(0, img.shape[0] - height)
            # img = img[y:y+height, x:x+width]
            # mask = mask[y:y+height, x:x+width]
            # return img, mask


# img = Image.open("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/sample_imgs/bbox.png")
        

# Cropper = CropImage((250,250))

# croppedImage = Image.fromarray(Cropper(np.array(img)))

# croppedImage.show()

# a = (5,10)
# print(a[0])