"""
.. module:: safrac 
   :platform: Unix, Windows, Macos
   :synopsis: Self Affine Fractal Volume Filling/Filtering.

.. moduleauthor:: Christoph Statz <christoph.statz@tu-dresden.de>


"""

import numpy as np

try:
    from numba import jit, float64, complex128, int_, void 
except:
    def jit(*jit_args, **jit_kwargs):
        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **kwargs)
            return wrapper
        return decorator

np.seterr(divide='raise')


from .generator import FractalGenerator
from .mask import FractalMask
