# -*- coding: utf-8 -*-

from __future__ import division
from safrac import jit, np


@jit(nopython=True, cache=True, nogil=True)
def _generate(fractal, center, dims, beta, lowcut, highcut):

    for idx in np.ndindex(dims):

        position = np.array(idx)

        r = np.sqrt(np.dot(position-center, position-center))
        if r < 1.e-5: r = 1.e-5 

        fractal[idx] = fractal[idx]/(r**beta)
        fractal[idx] *= (r >= lowcut)
        fractal[idx] *= (r <= highcut)


class FractalGenerator(object):

    def __init__(self, dimension, lowcut=None, highcut=None, seed=None):

        # dimension: Fractal dimension D_2

        self.beta = -(2. * dimension - 7.) / 2. # http://dx.doi.org/10.1017/CBO9781139174695, Fourier Spectral Approach, Eq. 7.75
        self.R = np.random.RandomState(seed)
        self.lowcut = lowcut
        self.highcut = highcut

    def generate(self, dims):

        center = np.asarray(dims)/2.
        fractal = np.fft.fftn(self.R.randn(*dims))

        lowcut = self.lowcut
        highcut = self.highcut

        if self.lowcut is None:
            lowcut = 0.

        if self.highcut is None:
            highcut = 1.e5

        _generate(fractal, center, dims, self.beta, lowcut, highcut)

        fractal = np.real(np.fft.ifftn(np.fft.ifftshift(fractal)))
        fractalmin = np.amin(fractal)
        fractalmax = np.amax(fractal)
        fractalrange = fractalmax - fractalmin

        return (fractal-fractalmin)/fractalrange

