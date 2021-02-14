from __future__ import division

from safrac import jit, np
from safrac import FractalGenerator


@jit(nopython=True, cache=True, nogil=True)
def _fill_volume(vol, distances):

    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            vol[i, j, 0:int(distances[i, j])] = 1


class FractalMask(object):
    # Not yet done.

    def __init__(self, *args, **kwargs):

        self.fractal_generator = FractalGenerator(*args, **kwargs)

    def generate(self, dims, fill_range, fill_offset=0):

        fractal_dims = dims[0:2]
        distances = self.fractal_generator.generate(fractal_dims)
        distances = np.round(distances * fill_range) + fill_offset

        mask = np.zeros(dims)
        _fill_volume(mask, distances)

        return mask
