import numpy as np
from skimage import color
class LabTransformer():
    # here you define the operation it should perform
    def transform(self, X, y=None, **fit_params):
        return color.rgb2lab(X.astype(np.uint8)).astype(np.float32)

    # just return self
    def fit(self, X, y=None, **fit_params):
        return self
