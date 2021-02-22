#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Dec  4 11:23:33 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: stats.py -*-
# -*- purpose: -*-

'''
Performs a real fit of a gaussian function using scipy methods!
'''

from math import sqrt, exp, pi
import warnings

from pyhisto import Histogram

from pyhisto.tools import GaussFit

# Here, in case the requirements are not met...
class Ghost:
    ''' ghost object just to fill'''
    def __getattribute__(self, name):
        def nothing(*w, **kw):
            warnings.warn('Calling a plotting function while `matplotlib` is not available')
        return nothing


try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = Ghost()

try:
    import numpy as np
    import scipy
    from scipy.optimize import curve_fit
except ImportError:
    raise ImportError("Could not implement Real Fit because `numpy` and `scipy` are not availble")


class GaussRealFit:
    '''From an histogram, extract Gaussian 'fitted' parameters '''
    def __init__(self,
                 h: Histogram):
        '''computes sum, average x, stddev, max, bin'''
        self.h1 = h
        _simplefit = GaussFit(self.h1)

        def GaussFunc(x,
                      S, M, R,
                      B, SL):
            return B + SL * (x - M) + S / np.sqrt(2. * pi * R * R) * np.exp(-(x - M) ** 2. / 2. / R / R)

        first_guess = [_simplefit.integral,
                       _simplefit.mean,
                       _simplefit.stdev,
                       self.h1[0].count,
                       0.0]
        limits = list(zip((0., np.inf),
                          (self.h1[0].lowedge, self.h1[-1].upedge),
                          (0., np.inf),
                          (-np.inf, np.inf),
                          (-np.inf, np.inf)
                          ))
        fitrslt, cov = curve_fit(GaussFunc,
                                 *self.h1.xy(),
                                 p0=first_guess,
                                 bounds=limits)
        uncerts = np.sqrt(np.diag(cov))
        self.integral = fitrslt[0]
        self.integral_u = uncerts[0]
        self.mean = fitrslt[1]
        self.mean_u = uncerts[1]
        self.stdev = fitrslt[2]
        self.stdev_u = uncerts[2]
        # Filling histograms for display
        self.background = self.h1.empty_copy()
        for b in self.background:
            b.count = fitrslt[3] + fitrslt[4] * (b.center() - self.mean)
        self.bgsubstracted = self.h1.copy()
        self.bgsubstracted -= self.background
        self.gaussian = self.h1.empty_copy()
        for b in self.gaussian:
            b.count = self.integral / sqrt(2. * pi * self.stdev * self.stdev) * exp(-(b.center() - self.mean) ** 2. / 2. / self.stdev / self.stdev)
        self.residuals = self.bgsubstracted.copy()
        self.residuals -= self.gaussian

    def add_to_plot(self):
        '''If a figure is already 'in progress',  add to the plot'''
        plt.step(*self.h1.xy())
        plt.step(*self.background.xy())
        plt.step(*self.bgsubstracted.xy())
        plt.step(*self.gaussian.xy())
        plt.step(*self.residuals.xy())

    def plot(self,
             target='screen'):
        '''Plot in a new figure (alone) and send to `target` (screen or file)'''
        plt.figure()
        plt.grid(True)
        plt.step(*self.h1.xy(), label='original')
        plt.step(*self.background.xy(), label='background')
        plt.step(*self.bgsubstracted.xy(), label='bacground subracted')
        plt.step(*self.gaussian.xy(), label='Gaussian')
        plt.step(*self.residuals.xy(), label='residual')
        plt.legend()
        if target == 'screen':
            plt.show()
        else:
            plt.savefig(target)

    def __repr__(self) -> str:
        return str({'integral': self.integral,
                    'integral_u': self.integral_u,
                    'mean': self.mean,
                    'mean_u': self.mean_u,
                    'stdev': self.stdev,
                    'stdev_u': self.stdev_u})
# end of class

# EOF
