#Imports
from PIL import Image
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
        if isinstance(self.output_size,int):
            w,h = Image.fromarray(image).size
            aspect = w/h
            if w<h:
                w = self.output_size
                h = self.output_size * 1/aspect
            else :
                h = self.output_size
                w = self.output_size * aspect
            return np.array(Image.fromarray(image).resize((int(w),int(h))))
        elif isinstance(self.output_size,tuple):
            return np.array(Image.fromarray(image).resize(self.output_size))
        elif(isinstance(self.output_size, float)):
            w,h = Image.fromarray(image).size
            w *= self.output_size
            h *= self.output_size
            return np.array(Image.fromarray(image).resize((int(w),int(h))))

# img = Image.open("/home/anish/Software Development Lab/Assignment-3/CS29006_SW_Lab_Spr2021/Python_DS_Assignment/AssignmentQs2/sample_imgs/bbox.png")
# print(img.size)

# rescaller = RescaleImage(250)
# rescaledImage = Image.fromarray(rescaller(np.array(img)))
# print(rescaledImage.size)
# rescaledImage.show()


# rescaller = RescaleImage((100,100))
# RescaledImage = Image.fromarray(rescaller(np.array(img)))
# print(RescaledImage.size)
# RescaledImage.show()
