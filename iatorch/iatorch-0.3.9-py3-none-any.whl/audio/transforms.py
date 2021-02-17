import numpy as np
import torch, librosa, cv2


################################################################################################################################
#### Recipes
####
################################################################################################################################

################################################################
#### RecipeMel
################################################################
class RecipeMel(object):
    
    def __init__(self, height=224, hop_sec=0.01, n_fft_factors=[8, 8, 8], tensor=True):
        self.spec = MelSpectrogram(height=height, hop_sec=hop_sec)
        self.n_fft_factors = n_fft_factors
        self.tensor = tensor
        
    def __call__(self, y, sr, augment=False):
        # Stack Mel spec.
        channels = []
        for n_fft_factor in self.n_fft_factors:
            S = self.spec(y, sr, n_fft_factor)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)        
        
        # Augmentation
        if augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        # ToTensor
        if self.tensor:
            x = ToTensor()(x)
        
        return x

    
################################################################
#### RecipeSTFT ~ multi layer
################################################################
class RecipeSTFT(object):
    def __init__(self, height=224, hop_sec=0.01, n_fft_factors=[8, 16, 32], tensor=True):
        self.spec = STFT(height=height, hop_sec=hop_sec)
        self.n_fft_factors = n_fft_factors
        self.tensor = tensor
        
    def __call__(self, y, sr, augment=False):
        
        # Stack STFT spec.
        channels = []
        for n_fft_factor in self.n_fft_factors:
            S = self.spec(y, sr, n_fft_factor)
            S = ((S-S.min())/(S.max()-S.min()) * 255).astype(np.int)
            channels.append(S)
        x = np.stack(channels, -1)
        
        # Augmentation
        if augment:
            x = SquareCrop('random')(x)
            x = Roll()(x)
            x = Flip()(x)
        else:
            x = SquareCrop('left')(x)
        
        # ToTensor
        if self.tensor:
            x = ToTensor()(x)
        
        return x


################################################################################################################################
#### Spectrograms
####
################################################################################################################################


################################################################
#### Mel Spectrogram
################################################################
class MelSpectrogram(object):
    
    def __init__(self, height=224, hop_sec=0.01):
        self.height = height
        self.hop_sec = hop_sec
    
    def __call__(self, y, sr, n_fft_factor=8):
        hop_length = int(sr * self.hop_sec)
        n_fft = hop_length * n_fft_factor
        S = librosa.feature.melspectrogram(y, sr, n_fft=n_fft, hop_length=hop_length, n_mels=self.height)
        S = librosa.power_to_db(S)
        
        return S
    
################################################################
#### STFT
################################################################
class STFT(object):
    
    def __init__(self, height=224, hop_sec=0.01):
        self.height = height
        self.hop_sec = hop_sec
        cv2.setNumThreads(0)
        
    def __call__(self, y, sr, n_fft_factor=8):
        hop_length = int(sr * self.hop_sec)
        n_fft = hop_length * n_fft_factor
        S = librosa.stft(y, n_fft, hop_length, )
        S = np.abs(S)
        S = librosa.amplitude_to_db(S)
        S = cv2.resize(S, (S.shape[1], self.height))
        
        return S

    
################################################################
#### DWT
################################################################



################################################################
#### CWT
################################################################



################################################################
#### Scale
################################################################
# 0 ~ 1 float
# 0 ~ 255 uint8
class Scale(object):
    def __init__(self, mean=None, std=None, cutoff=(-3, 3)):
        self.mean = mean
        self.std = std
        self.cutoff = cutoff
    def __call__(self, y, sr):
        if all([x is not None for x in [self.mean, self.std]]):
            y = (y - self.mean) / self.std
            cutL, cutH = self.cutoff
            y = np.clip(y, cutL, cutH)
            y = (y - cutL) / (cutH - cutL) 
        return y, sr


################################################################################################################################
# Images
#
################################################################################################################################


################################################################
#### Square Crop
################################################################
class SquareCrop(object):   
    
    def __init__(self, position='left', order='hwc'):
        self.position = position
        self.order = order
    
    def __call__(self, x):
        if self.order == 'chw':
            x = np.transpose(x, (1, 2, 0))
        elif self.order == 'hwc':
            x = x
        else:
            print('ERROR!!!')
        h, w, c = x.shape
            
        #### if width is smaller than height, drop the data 
        if w <= h:
            return x

        #### do crop
        if self.position == 'left':
            x = x[:, :h, :]
        elif self.position == 'center':
            x = x[:, w//2-h//2:w//2+h//2, :]
        elif self.position == 'right':
            x = x[:, -h:, :]
        elif self.position == 'random':
            l = np.random.randint(0, w - h)
            x = x[:, l:l+h, :]
        else:
            print('ERROR!!! crop options: [left, center, right, random]')  
            
        ##### reorder
        if self.order == 'chw':
            x = np.transpose(x, (2, 0, 1))
            
        return x


################################################################
#### Resize
################################################################
class Resize(object):
    def __init__(self, height=224, width='fixed_aspect', order='hwc'):
        self.height = height
        self.width = width
        self.order = order
        cv2.setNumThreads(0)
        
    def __call__(self, x):
        
        #### REORDER
        if self.order == 'chw':
            x = np.transpose(x, (1, 2, 0))
        elif self.order == 'hwc':
            x = x
        else:
            print('ERROR!!!')
        h, w, c = x.shape
        
        #### SET WIDTH
        if self.width == 'fixed_aspect':
            width = int(w * self.height / h)
        elif self.width == 'fixed_width':
            width = w
        elif type(width) is int:
            width = width
        else:
            print('ERROR!!! resize options: "fixed_aspect", "fixed_width", int()')
        
        #### RESIZE
        x = cv2.resize(x, (width, self.height))
        
        #### REORDER
        if self.order == 'chw':
            x = np.transpose(x, (2, 0, 1))
        
        return x

    
################################################################
#### Rolling
################################################################
class Roll(object):
    
    def __init__(self, shift='random', freq=0.3, order='hwc'):
        self.shift = shift
        self.order = order
        self.freq = freq
    
    def __call__(self, x):
        
        if np.random.random() < self.freq:
            
            #### Get Order
            axis = self.order.index('w')
            width = x.shape[axis]
            
            #### ROLL
            if self.shift == 'random':
                shift = np.random.randint(0, width)
            elif type(self.shift) is int:
                shift = self.shift
            else:
                print("ERROR!!! only 'random' and integer are available now")
            x = np.roll(x, shift, axis)
            
        return x
    
    
################################################################
#### Flip
################################################################
class Flip(object):
    
    def __init__(self, shift='random', freq=0.3, order='hwc'):
        self.shift = shift
        self.order = order
        self.freq = freq
    
    def __call__(self, x):
        
        if np.random.random() < self.freq:
            #### REORDER
            if self.order == 'chw':
                x = np.transpose(x, (1, 2, 0))
            elif self.order == 'hwc':
                x = x
            else:
                print('ERROR!!!')

            #### Flip (mirror)
            x = cv2.flip(x, 1)

            #### REORDER
            if self.order == 'chw':
                x = np.transpose(x, (2, 0, 1))

        return x

    
################################################################
#### ToTensor
################################################################
class ToTensor(object):
    
    def __init__(self, dtype=torch.float32):
        self.dtype = dtype
    
    def __call__(self, x):
        x = np.transpose(x, (2, 0, 1))
        x = torch.tensor(x, dtype=self.dtype)
        return x
