#Imports
import cv2

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
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''
        img = image.transpose((1, 2, 0))

        if isinstance(self.output_size, int):
            size = self.output_size
            if (img.shape[0] < img.shape[1]):
                self.output_size = (size, int(img.shape[1] * size/img.shape[0]))
            else:
                self.output_size = (int(img.shape[0] * size/img.shape[1]), size)
        else:
            self.output_size = (int(self.output_size[0]), int(self.output_size[1]))

        resized = cv2.resize(img, self.output_size, interpolation = cv2.INTER_AREA)
        resized = resized.transpose((2, 0, 1))

        return resized