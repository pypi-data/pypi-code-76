#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Dec  4 11:23:33 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: stats.py -*-
# -*- purpose: -*-

'''
A class that performs Gaussian statistical approximation
and keep the information in the object.

'''

from math import sqrt, exp, pi

from contextlib import suppress
import warnings

import pyhisto
from pyhisto import Histogram

# In the next part, I try to make sure the module can be
# imported even if matplotlib is not installed.
try:
    import matplotlib.pyplot as plt
except ImportError:
    class Ghost:
        ''' ghost object just to fill'''
        def __getattribute__(self, name):
            def nothing(*w, **kw):
                warnings.warn('Calling a plotting function while `matplotlib` is not available')
            return nothing
    plt = Ghost()


class GaussFit:
    '''From an histogram, extract Gaussian 'fitted' parameters '''
    def __init__(self,
                 h: Histogram):
        '''Computes sum, average x, stddev, max, bin'''
        h1 = h
        bg = h1.empty_copy()
        bg_l = h1[0].count
        bg_r = h1[-1].count
        for i, b in enumerate(bg):
            b.count = bg_l + (i / float(len(bg))) * (bg_r - bg_l)
        # making bg substracted histogram
        hsbgsub = h1.copy()
        hsbgsub -= bg
        for b in hsbgsub:
            if b.count < 0:
                b.count = 0
        # Now, counting the sum
        S = sum(hsbgsub) * hsbgsub[0].width()
        # Mean value
        with suppress(ZeroDivisionError):
            M = sum((b.center() * b.count for b in hsbgsub)) / sum(hsbgsub)
        # Stddev
        with suppress(ZeroDivisionError):
            Stdev = sum((b.center() ** 2. * b.count for b in hsbgsub)) / sum(hsbgsub)
        Stdev -= M * M
        Stdev = sqrt(Stdev)
        # making the gaussian, and residual
        G = hsbgsub.empty_copy()
        R = G.copy()
        for i, b in enumerate(G):
            b.count = S / sqrt(2. * pi * Stdev * Stdev) * exp(-(b.center() - M) ** 2. / 2. / Stdev / Stdev)
            R[i].count = hsbgsub[i] - b.count
        self.h1 = h1
        self.background = bg
        self.bgsubstracted = hsbgsub
        self.gaussian = G
        self.residuals = R
        self.integral = S
        self.mean = M
        self.stdev = Stdev

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

    def __repr__(self):
        return str({'integral': self.integral,
                    'mean': self.mean,
                    'stdev': self.stdev})

# end of class

# EOF
