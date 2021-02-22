#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Aug 11 10:22:50 CEST 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file: histogram2D.py -*-
# -*- purpose: -*-

'''
The module contains the Lazy Histogram2D class.
'''


import array

from pyhisto.histogram2D import Histo2DError


class LazyHistogram2D:
    ''' Implement 2D hisotgram'''

    def __init__(self,
                 xnbins=1, xmin=None, xmax=None,
                 ynbins=1, ymin=None, ymax=None,
                 arraytype='H'):
        '''Initilize the Lazy Hisotgram2D
        ``Histogram2D(nxbins, xmin, xmax, nybins, ymin, ymax)``
        '''
        self.xnbins = xnbins
        self.ynbins = ynbins
        if xmin is None:
            xmin = -0.5
        if xmax is None:
            xmax = xmin + xnbins
        if ymin is None:
            ymin = -0.5
        if ymax is None:
            ymax = ymin + ynbins
        if xmin == xmax:
            raise Histo2DError("X Bounds values in histogram should be different")
        if ymin == ymax:
            raise Histo2DError("Y Bounds values in histogram should be different")
        xmin, xmax = min(xmax, xmin), max(xmax, xmin)
        ymin, ymax = min(ymax, ymin), max(ymax, ymin)
        self.xmin = xmin
        self.xmax = xmax
        self.xbinwidth = (self.xmax - self.xmin) / float(self.xnbins)
        self.ymin = ymin
        self.ymax = ymax
        self.ybinwidth = (self.ymax - self.ymin) / float(self.ynbins)
        self.bins = array.array(arraytype, [0 for j in range(self.ynbins * self.xnbins)])
        self.outofrange = 0
        self.export_threshold = 0.
    # end __init__

    def __str__(self):
        '''Dump the histogram in string format'''
        z = ''
        z += f'# xnbins = {self.xnbins}\n'
        z += f'# xmin = {self.xmin}\n'
        z += f'# xmax = {self.xmax}\n'
        z += f'# ynbins = {self.ynbins}\n'
        z += f'# ymin = {self.ymin}\n'
        z += f'# ymax = {self.ymax}\n'
        if self.export_threshold > 0.:
            z += f'# Exporting bins with more than {self.export_threshold} counts\n'
        for i in range(0, self.xnbins):
            for j in range(0, self.ynbins):
                if self.bins[i + j * self.xnbins] > self.export_threshold:
                    z += f"{i} {j} {self.bins[i+j*self.xnbins]}\n"
        z += f'# out of range = {self.outofrange}\n'
        return z
    # end __str__

    def __repr__(self):
        '''Writting the histogram2D as a dictionnary'''
        z = "{ \n"
        z += f"   'xnbins':{self.xnbins},\n"
        z += f"   'xmin':{self.xmin},\n"
        z += f"   'xmax':{self.xmax},\n"
        z += f"   'ynbins':{self.ynbins},\n"
        z += f"   'ymin':{self.ymin},\n"
        z += f"   'ymax':{self.ymax},\n"
        z += f"   'outofrange':{self.outofrange},\n"
        z += f"   'bins':{self.bins},\n"
        z += "}"
        return z
    # end __repr__

    def fast_fill(self, x: float, y: float,
                  w: int = 1):
        '''Add one (or w) counts to the bin, in a fast way'''
        try:
            self.bins[int((x - self.xmin) / self.xbinwidth) + self.xnbins * int((y - self.ymin) / self.ybinwidth)] += w
        except IndexError:
            self.outofrange += w

# end class

# EOF
