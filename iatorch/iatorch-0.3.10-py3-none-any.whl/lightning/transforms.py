
import numpy as np
from iatorch.audio import transforms as iaTransforms

################################################################
#### RecipeMel
################################################################
class RecipeMel(object):
    '''
    Shape: H x W x C
    Output: H x W x C
    '''
    
    def __init__(self, sr=None, n_fft=1000, shape=(3,224,224)):
        self.sr = None
        self.n_fft = n_fft
        self.shape = shape
        self.channel, self.height, self.width = shape
        
    def __call__(self, y, sr=None, augment=True):
        x1, _ = iaTransforms.STFT(self.n_fft)(y, sr)
        x = []
        for i in range(self.channel):
            x.append(x1)
        x = np.stack(x, -1)
        x = iaTransforms.Resize(self.height)(x)
        x = iaTransforms.SquareCrop('left')(x)
        if augment:
            x = iaTransforms.Rolling()(x)
        return x
