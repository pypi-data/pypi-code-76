#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Dec  4 10:59:10 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: parzen_estimator.py -*-
# -*- purpose: -*-

'''
Made o estimate the value of the function follwing the histogram
(not fully implemented yet)
'''

import math

import pyhisto
from pyhisto import Histogram


def kernel_gauss(u, w) -> float:
    '''Gaussian kernel'''
    return 0.39894228 * math.exp(-.5 * u * u)

def kernel_parabol(u, w) -> float:
    '''Parabolic kernel'''
    if (u >=- 1 and u <= 1):
        return 3. / 4. * ( 1. - u * u)
    return 0.0


class ParzenEstimator:
    '''Create an estimator'''

    def __init__(self,
                 h,
                 kernel=kernel_gauss,
                 width=lambda b: b.width(),
                 normalize=True):
        raise NotImplementedError
        self.h = h.copy()
        self.width = width
        self.kernel = kernel

        def estim(x):
            ' internal function for estimation '
            f = 0.0
            for b in h:
                w = self.width(b)
                u = (x - b.center()) / w
                f+= self.kernel(u, w) * b.count
            f /= 1.0 * len(self.h)
            return f
        self.Norm = 1.0
        if normalize:
            S = sum(self.h)
            estS = 0.0
            nint = int(self.h.nbins * 2.33)
            wint = (self.h.xmax - self.h.xmin) / nint
            for i in range(nint):
                estS += estim(self.h.xmin + i * wint ) * wint
            self.Norm = S / estS
        elif normalize == 'to1':
            estS = 0.0
            nint = int(self.h.nbins * 2.33)
            wint = (self.h.xmax - self.h.xmin) / nint
            for i in range(nint):
                estS += estim(self.h.xmin + i * wint) * wint
            self.Norm = 1. / estS
        self.estimator = estim

    def __repr__(self):
        return "<ParzenEstimator of {0}>".format(repr(self.h))

    def __call__(self, x):
        return self.estimator(x) * self.Norm

# end of class

# EOF

