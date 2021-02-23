import numpy as np


class interpolate_n:
    """
    wrapper arround 'map_coordinates'
    n-dimensional linear interpolation

    :Example:
    1. initialisation:
            from sicor.Tools.NM.interpolate_n import interpolate_n as intpn
             pn=intpn.interpolate_n(LUT,axes)
               LUT   is a Nd numpy array
               axes  is a tupel of 1d numpy arrays
                     The number of axes must correspond to the number
                     of dimensions an the size of the axes must
                     correspond to the size of the dimensions
    2. recall:
             >>> result=pn.recall(pos)
               pos   is a (ndim,nsample) array with the positions
                     if is_index=True pos is already a float index
    """

    def __init__(self, lut, axes):
        from scipy import interpolate as intp  # import here to avoid static TLS ImportError

        if not isinstance(lut, np.ndarray):
            raise ValueError('Input is not an Numpy ndarray')
        self.ndim = lut.ndim

        if not isinstance(axes, tuple):
            raise ValueError('Axes is not a tuple')

        if len(axes) != self.ndim:
            raise ValueError(
                'Number of elements of axes %i is not equal the number of dimensions (%i)' % (len(axes), self.ndim))

        for i, dim in enumerate(axes):
            if not isinstance(dim, np.ndarray):
                raise ValueError('Axes %i is not an Numpy ndarray' % i)
            if not dim.ndim == 1:
                raise ValueError('Axes %i is not an 1D Numpy ndarray' % i)
            if len(dim) != lut.shape[i]:
                raise ValueError(
                    'Axes %i does not agree with the shape of LUT Axes %i has %i elements but LUT needs %i.' % (
                        i, i, len(dim), lut.shape[i]))

        self.lut = lut
        self.axes_intp = []
        for i in range(self.ndim):
            self.axes_intp.append(intp.interp1d(axes[i], np.arange(axes[i].shape[0]), kind="linear"))
        self.axes = axes

    def recall(self, positions, is_index=False):
        from scipy.ndimage.interpolation import map_coordinates as mcrd  # import here to avoid static TLS ImportError

        if positions.shape[1] != self.ndim:
            raise ValueError('Dimensions of position are (%i,%i) but should be (Nsample,%i) ' % (
                positions.shape[0], positions.shape[1], self.ndim))
        pss = positions.copy()
        if not is_index:
            for i in range(self.ndim):
                pss[:, i] = self.axes_intp[i](positions[:, i])
        return mcrd(self.lut, pss.T, order=1)
