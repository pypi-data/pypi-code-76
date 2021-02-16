#Imports


from PIL import Image
import numpy as np

class FlipImage(object):
    '''
        Flips the image.
    '''
    data = None
    flip_img = None
    mode=None
    
    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''
        if(flip_type=='horizontal'):
            self.mode=Image.FLIP_LEFT_RIGHT
        elif (flip_type=='vertical'):
            self.mode=Image.FLIP_TOP_BOTTOM
        else:
            print("Wrong Flip type")
        # Write your code here

        
    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        
        self.data=Image.fromarray(image)
        self.flip_img = np.asarray(self.data.transpose(self.mode))
        # Write your code here
        return self.flip_img

# test=FlipImage('vertical')
# arr=test(np.asarray(Image.open('./test_img.jpeg')))
# img=Image.fromarray(arr)
# img.show()
    
       