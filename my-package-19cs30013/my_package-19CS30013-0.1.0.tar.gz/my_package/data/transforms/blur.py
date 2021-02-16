import cv2

class BlurImage(object):
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        '''

        self.size = 2*radius + 1
        

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL Image)

            Returns:
            image (numpy array or PIL Image)
        '''
        img = image.transpose((1, 2, 0))
        blur = cv2.GaussianBlur(img,(self.size, self.size),0)
        blur = blur.transpose((2, 0, 1))
        
        return blur

