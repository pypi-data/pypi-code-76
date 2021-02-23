"""Fast interpolation in 12-dim arrays."""
import numpy as np
from numba import jit, int8, float32
from cachetools import LRUCache

__author__ = "Niklas Bohn, Andre Hollstein"


@jit(nopython=True)
def int1d(nx, xx, yy, x):
    """
    nx: length of xx and yy vector
    xx: indepent data
    yy: dependent data
    return: linearly interpolated point
    """
    if (x >= xx[0]) and (x <= xx[nx - 1]):
        in_range = 1
    else:
        in_range = 0

    ii = 0
    for ii in range(nx):
        if x <= xx[ii]:
            break
    vv = xx[ii] - xx[ii - 1]
    return yy[ii - 1] * (xx[ii] - x) / vv + yy[ii] * (x - xx[ii - 1]) / vv, (yy[ii] - yy[ii - 1]) / vv, in_range


@jit(nopython=True)
def sign(x):
    """Jit version of signum function."""
    if x > 0.0:
        return 1.0
    else:
        return -1.0


@jit(nopython=True)
def __dx__(pt, rt, mx):
    """
    pt: float index
    rt: 1D numpy array of ints
    returns in rt array, float and ceil of pt
    """
    rt[0] = np.floor(pt)
    rt[1] = rt[0] + 1

    if rt[1] == mx:
        rt[0] -= 1
        rt[1] -= 1


@jit(nopython=True, locals={'vi': float32,
                            'b0': int8, 'b1': int8, 'b2': int8, 'b3': int8, 'b4': int8, 'b5': int8, 'b6': int8,
                            'b7': int8, 'b8': int8, 'b9': int8, 'b10': int8, 'b11': int8,
                            'v0': float32, 'v1': float32, 'v2': float32, 'v3': float32, 'v4': float32, 'v5': float32,
                            'v6': float32, 'v7': float32, 'v8': float32, 'v9': float32, 'v10': float32,
                            'v11': float32, })
def __intp_spectral__(data, res, grad, ndim,
                      p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11,
                      d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, ):
    """
    3D interpolation, but easy to generalize to n dimentions
    data: 1D+3D numpy array of arbitrary shape, first dimension is "spectral" and interpolation is carried over
    res: 1D numpa vector with shape of spectral dimension
    ndim: length of spectral dimension
    p0-p3: float index at which is interpolated
    d0-d2: 1D numpy array of shape 2, contain floor and ceil of p0-p3
    returns interpolation point
    """

    for i0 in d0:
        for i1 in d1:
            for i2 in d2:
                for i3 in d3:
                    for i4 in d4:
                        for i5 in d5:
                            for i6 in d6:
                                for i7 in d7:
                                    for i8 in d8:
                                        for i9 in d9:
                                            for i10 in d10:
                                                for i11 in d11:

                                                    vi = np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))

                                                    v0 = sign(p0 - i0) * np.abs(
                                                        1.0 * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v1 = sign(p1 - i1) * np.abs(
                                                        (p0 - i0) * 1.0 * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v2 = sign(p2 - i2) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * 1.0 * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v3 = sign(p3 - i3) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * 1.0 * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v4 = sign(p4 - i4) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * 1.0 * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v5 = sign(p5 - i5) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            1.0) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v6 = sign(p6 - i6) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * 1.0 * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v7 = sign(p7 - i7) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * 1.0 * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v8 = sign(p8 - i8) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * 1.0 * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))
                                                    v9 = sign(p9 - i9) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * 1.0 * (
                                                                p10 - i10) * (p11 - i11))
                                                    v10 = sign(p10 - i10) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                1.0) * (p11 - i11))
                                                    v11 = sign(p11 - i11) * np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * 1.0)
                                                    # works only in numba since the integer conversion of the b is
                                                    # handled trough the interface block, without
                                                    # numba add int()'s here
                                                    b0 = int(i0 + sign(p0 - i0))
                                                    b1 = int(i1 + sign(p1 - i1))
                                                    b2 = int(i2 + sign(p2 - i2))
                                                    b3 = int(i3 + sign(p3 - i3))
                                                    b4 = int(i4 + sign(p4 - i4))
                                                    b5 = int(i5 + sign(p5 - i5))
                                                    b6 = int(i6 + sign(p6 - i6))
                                                    b7 = int(i7 + sign(p7 - i7))
                                                    b8 = int(i8 + sign(p8 - i8))
                                                    b9 = int(i9 + sign(p9 - i9))
                                                    b10 = int(i10 + sign(p10 - i10))
                                                    b11 = int(i11 + sign(p11 - i11))
                                                    # when writing, numba didn't support array striding,
                                                    # meant is: res[:] += vi*data[:,b0,b1,b2]
                                                    for ii in range(ndim):
                                                        # <- here decide weather spectral dimension is first or last
                                                        dat = data[b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, ii]
                                                        res[ii] += vi * dat

                                                        grad[0, ii] += v0 * dat
                                                        grad[1, ii] += v1 * dat
                                                        grad[2, ii] += v2 * dat
                                                        grad[3, ii] += v3 * dat
                                                        grad[4, ii] += v4 * dat
                                                        grad[5, ii] += v5 * dat
                                                        grad[6, ii] += v6 * dat
                                                        grad[7, ii] += v7 * dat
                                                        grad[8, ii] += v8 * dat
                                                        grad[9, ii] += v9 * dat
                                                        grad[10, ii] += v10 * dat
                                                        grad[11, ii] += v11 * dat


@jit(nopython=True, locals={'vi': float32,
                            'b0': int8, 'b1': int8, 'b2': int8, 'b3': int8, 'b4': int8, 'b5': int8, 'b6': int8,
                            'b7': int8, 'b8': int8, 'b9': int8, 'b10': int8, 'b11': int8,
                            'v0': float32, 'v1': float32, 'v2': float32, 'v3': float32, 'v4': float32, 'v5': float32,
                            'v6': float32, 'v7': float32, 'v8': float32, 'v9': float32, 'v10': float32,
                            'v11': float32, })
def __intp_spectral_no_jac__(data, res, ndim,
                             p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11,
                             d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, ):
    """
    3D interpolation, but easy to generalize to n dimentions
    data: 1D+3D numpy array of arbitrary shape, first dimension is "spectral" and interpolation is carried over
    res: 1D numpa vector with shape of spectral dimension
    ndim: length of spectral dimension
    p0-p3: float index at which is interpolated
    d0-d2: 1D numpy array of shape 2, contain floor and ceil of p0-p3
    returns interpolation point
    """
    for i0 in d0:
        for i1 in d1:
            for i2 in d2:
                for i3 in d3:
                    for i4 in d4:
                        for i5 in d5:
                            for i6 in d6:
                                for i7 in d7:
                                    for i8 in d8:
                                        for i9 in d9:
                                            for i10 in d10:
                                                for i11 in d11:

                                                    vi = np.abs(
                                                        (p0 - i0) * (p1 - i1) * (p2 - i2) * (p3 - i3) * (p4 - i4) * (
                                                            p5 - i5) * (p6 - i6) * (p7 - i7) * (p8 - i8) * (p9 - i9) * (
                                                                p10 - i10) * (p11 - i11))

                                                    # works only in numba since the integer conversion of the b is
                                                    # handled trough the interface block, without numba
                                                    # add int()'s here
                                                    b0 = int(i0 + sign(p0 - i0))
                                                    b1 = np.int(i1 + sign(p1 - i1))
                                                    b2 = np.int(i2 + sign(p2 - i2))
                                                    b3 = np.int(i3 + sign(p3 - i3))
                                                    b4 = np.int(i4 + sign(p4 - i4))
                                                    b5 = np.int(i5 + sign(p5 - i5))
                                                    b6 = np.int(i6 + sign(p6 - i6))
                                                    b7 = np.int(i7 + sign(p7 - i7))
                                                    b8 = np.int(i8 + sign(p8 - i8))
                                                    b9 = np.int(i9 + sign(p9 - i9))
                                                    b10 = np.int(i10 + sign(p10 - i10))
                                                    b11 = np.int(i11 + sign(p11 - i11))
                                                    # when writing, numba didn't support array striding,
                                                    # meant is: res[:] += vi*data[:,b0,b1,b2]
                                                    for ii in range(ndim):
                                                        # <- here decide weather spectral dimension is first or last
                                                        dat = data[b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, ii]
                                                        res[ii] += vi * dat


def __intp__(data, pt, dv, jacobean):
    """
    data: numpy array, here 3D, arbitrary shape
    pt: 1D numpy array of shape (3), this is the wanted interpolation point
    return: interpolated value
    """
    d0 = np.zeros(2, dtype=int)
    d1 = np.zeros(2, dtype=int)
    d2 = np.zeros(2, dtype=int)
    d3 = np.zeros(2, dtype=int)
    d4 = np.zeros(2, dtype=int)
    d5 = np.zeros(2, dtype=int)
    d6 = np.zeros(2, dtype=int)
    d7 = np.zeros(2, dtype=int)
    d8 = np.zeros(2, dtype=int)
    d9 = np.zeros(2, dtype=int)
    d10 = np.zeros(2, dtype=int)
    d11 = np.zeros(2, dtype=int)
    __dx__(pt[0], d0, data.shape[0])
    __dx__(pt[1], d1, data.shape[1])
    __dx__(pt[2], d2, data.shape[2])
    __dx__(pt[3], d3, data.shape[3])
    __dx__(pt[4], d4, data.shape[4])
    __dx__(pt[5], d5, data.shape[5])
    __dx__(pt[6], d6, data.shape[6])
    __dx__(pt[7], d7, data.shape[7])
    __dx__(pt[8], d8, data.shape[8])
    __dx__(pt[9], d9, data.shape[9])
    __dx__(pt[10], d10, data.shape[10])
    __dx__(pt[11], d11, data.shape[11])

    ndim_spectral = data.shape[-1]  # <- here decide weather spectral dimension is first or last
    res = np.zeros(ndim_spectral)
    if jacobean:
        grad = np.zeros((12, ndim_spectral))
        __intp_spectral__(data, res, grad, ndim_spectral,
                          pt[0], pt[1], pt[2], pt[3], pt[4], pt[5], pt[6], pt[7], pt[8], pt[9], pt[10], pt[11],
                          d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10,
                          d11)  # <- here decide weather spectral dimension is first or last

        grad[0, :] *= dv[0]
        grad[1, :] *= dv[1]
        grad[2, :] *= dv[2]
        grad[3, :] *= dv[3]
        grad[4, :] *= dv[4]
        grad[5, :] *= dv[5]
        grad[6, :] *= dv[6]
        grad[7, :] *= dv[7]
        grad[8, :] *= dv[8]
        grad[9, :] *= dv[9]
        grad[10, :] *= dv[10]
        grad[11, :] *= dv[11]
        return res, grad
    else:
        __intp_spectral_no_jac__(data, res, ndim_spectral,
                                 pt[0], pt[1], pt[2], pt[3], pt[4], pt[5], pt[6], pt[7], pt[8], pt[9], pt[10], pt[11],
                                 d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10,
                                 d11)  # <- here decide weather spectral dimension is first or last
        return res


# class intp12_dx(object):
class intp(object):
    """
    Wrapper class for 3D interpolation with intp 12 dimensions
    """

    def __init__(self, data, axes=None, jacobean=True, caching=False, maxsize=2000,
                 hash_pattern="%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,"):
        """
        data : data: numpy array, last dimension is spectral one, over which interpolation is beeing carried over
        axes : list of 1D numpy arrays of shape data.shape(i), contaoning the scales for each dimension,
        not including values for the spectral dimension
        maxsize: max number of cached results, both for Jacobean and non Jacobean caches
        hash_pattern: string to convert py array/list to hash, e.g. n_dim"%.4f" % tuple(pt)
        """
        assert isinstance(jacobean, bool)
        assert isinstance(caching, bool)
        assert isinstance(hash_pattern, str)
        assert isinstance(data, np.ndarray)
        if axes is not None:
            assert len(axes) == len(data.shape) - 1
            for axe in axes:
                assert isinstance(axe, np.ndarray)
                assert len(axe.shape) == 1
        # define base settings
        self.n_dim = 12
        self.data = data
        self.cache = None
        self.__jacobean__ = None
        self.__caching__ = None
        self.hash_pattern = hash_pattern
        # use separate caches for with and without Jacobean computations
        self.cache_no_jac = LRUCache(maxsize=maxsize)
        self.cache_jac = LRUCache(maxsize=maxsize)
        # apply settings
        self.settings(jacobean=jacobean, caching=caching)
        # initialize axes
        # excluding spectral dimension from axes, <- here decide weather spectral dimension is first or last
        self.axes_y = [np.arange(ii) for ii in self.data.shape[:-1]]
        if axes is not None:
            self.axes_x = axes
        else:
            self.axes_x = self.axes_y

    def __call__(self, pt):
        """ Implement callable protocoll"""
        if self.__caching__:
            return self.__call_from_cache__(pt)
        else:
            return self.__call_no_cache__(pt)

    def __call_from_cache__(self, pt):
        """ Before interpolation, check cache for result """
        try:
            return self.cache[self.__hash__(pt)]
        except Exception:
            res = self.interpolate(pt)
            self.cache[self.__hash__(pt)] = res
            return res

    def __call_no_cache__(self, pt):
        """ Don't check hash"""
        return self.interpolate(pt)

    def settings(self, jacobean, caching):
        """ Consistently set values for jacobean and caching (separate for Jacobean)"""
        assert isinstance(jacobean, bool)
        assert isinstance(caching, bool)

        self.__jacobean__ = jacobean
        self.__caching__ = caching

        if self.__caching__:
            if self.__jacobean__:
                self.cache = self.cache_jac
            else:
                self.cache = self.cache_no_jac

    def __hash__(self, pt):
        """ Hash function for pt array/list, used for caching """
        return self.hash_pattern % tuple(pt)

    def interpolate(self, pt):
        """
        point at which should be interpolated
        pt: nump float array, interpolation point
        return: interpolation point,gradient
        """
        p0, d0, r0 = int1d(self.data.shape[0], self.axes_x[0], self.axes_y[0], pt[0])
        p1, d1, r1 = int1d(self.data.shape[1], self.axes_x[1], self.axes_y[1], pt[1])
        p2, d2, r2 = int1d(self.data.shape[2], self.axes_x[2], self.axes_y[2], pt[2])
        p3, d3, r3 = int1d(self.data.shape[3], self.axes_x[3], self.axes_y[3], pt[3])
        p4, d4, r4 = int1d(self.data.shape[4], self.axes_x[4], self.axes_y[4], pt[4])
        p5, d5, r5 = int1d(self.data.shape[5], self.axes_x[5], self.axes_y[5], pt[5])
        p6, d6, r6 = int1d(self.data.shape[6], self.axes_x[6], self.axes_y[6], pt[6])
        p7, d7, r7 = int1d(self.data.shape[7], self.axes_x[7], self.axes_y[7], pt[7])
        p8, d8, r8 = int1d(self.data.shape[8], self.axes_x[8], self.axes_y[8], pt[8])
        p9, d9, r9 = int1d(self.data.shape[9], self.axes_x[9], self.axes_y[9], pt[9])
        p10, d10, r10 = int1d(self.data.shape[10], self.axes_x[10], self.axes_y[10], pt[10])
        p11, d11, r11 = int1d(self.data.shape[11], self.axes_x[11], self.axes_y[11], pt[11])
        # all ri must be one for pt to to be in the table
        rr = r0 * r1 * r2 * r3 * r4 * r5 * r6 * r7 * r8 * r9 * r10 * r11
        if rr != 1:
            raise ValueError("At least one dimension is out of bounds.")
        else:
            return __intp__(self.data, [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11],
                            [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11], jacobean=self.__jacobean__)
