#Imports
from PIL import Image
import numpy as np

class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''
        
        # Write your code here
        self.degrees = degrees

    def __call__(self, sample):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        sample = Image.fromarray(sample)
        rotated_image = sample.rotate(self.degrees , expand = True)
        rotated_image = np.array(rotated_image)
        return rotated_image


# rotate = RotateImage(-90)

# img = np.array(Image.open('./data/imgs/0.jpg'))
# im = rotate(img)

# image = Image.fromarray(im)
# image.save('rotate.jpg')
 