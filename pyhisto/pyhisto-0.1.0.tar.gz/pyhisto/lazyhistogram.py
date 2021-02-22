#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Oct  9 11:31:54 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: lazy_histogram.py -*-
# -*- purpose: -*-

'''
The LazyHistogram is to be used when speed and memory are keys
(typically filling).
It is backed by the `array` module to store the values (integter)
with smaller footprint.
'''

import array

from typing import Union, Optional, List

class LazyHistogram:
    '''
    This Histogram is a liteweight version of 1D histo, for purpose of filling
    '''
    def __init__(self,
                 nbins: int = 1,
                 xmin: float = -0.5,
                 xmax: Union[float, None] = None,
                 arraytype: str = 'L'):
        self.nbins: int = nbins
        self.xmin: float = xmin
        self.xmax: float = xmin + nbins
        if not (xmax is None):
            self.xmax = xmax
        self.xmin, self.xmax = min(self.xmin, self.xmax), max(self.xmin, self.xmax)
        self.binwidth: float = (self.xmax - self.xmin) / self.nbins
        self.bins = array.array(arraytype,
								[0] * self.nbins)
        self.outofrange = 0
    # end __init__

    def __str__(self) -> str:
        '''Dump the histogram in string format'''
        z = ''
        z += '# nbins = {0}\n'.format(self.nbins)
        z += '# xmin = {0}\n'.format(self.xmin)
        z += '# xmax = {0}\n'.format(self.xmax)
        for i in range(0, self.nbins):
            lowedge = self.xmin + i * self.binwidth
            z += f"{lowedge} {self.binwidth} {self.bins[i]}\n"
        # end for bins
        z += f'# out of range = {self.outofrange}\n'
        return z
    # end __str__

    def __del__(self):
        del self.nbins
        del self.xmin
        del self.xmax
        del self.binwidth
        del self.outofrange
        del self.bins
    # end __del__

    # following: the two working functions
    def fast_index(self, x: float) -> int:
        ''' returns the index for `x` '''
        return int((x - self.xmin) / self.binwidth)

    def fast_fill(self,
                  x: float,
                  w=1):
        ''' fast filling of the histogram
        find the bin corresponding to `x` and adding `w` into its count
        '''
        try:
            self.bins[int((x - self.xmin) / self.binwidth)] += w
        except IndexError:
            self.outofrange += w

    # The following 4 fucntions provide container like behavior
    def __getitem__(self, k):
        return self.bins[k]

    def __setitem__(self, k, v):
        self.bins[k] = v

    def __len__(self) -> int:
        return len(self.bins)

    def __iter__(self):
        ''' provides iteration over bin directly '''
        return iter(self.bins)

# end of file
