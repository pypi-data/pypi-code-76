#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Oct  9 11:31:54 CEST 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: lazy_histogram.py -*-
# -*- purpose: -*-

'''
Ghost Histogram has the outside API of a real one,
but nothing happens behind.
This is to be used in filling situation, where it's easier to
fill a 'ghost' rather than test if the channel is defined, ...
'''


class GhostHistogram:
    '''
    Behave like a 1D histogram, but does nothing
    '''
    def __init__(self, *w, **kw):
        self.nbins = 0
        self.xmin = 0
        self.xmax = 0
        self.binwidth = 0.
        self.bins = []
        self.outofrange = 0

    def __str__(self):
        '''Dump the histogram in string format'''
        z = f'# nbins = {self.nbins}\n'
        z += f'# xmin = {self.xmin}\n'
        z += f'# xmax = {self.xmax}\n'
        for i in range(0, self.nbins):
            lowedge = self.xmin + i * self.binwidth
            z += f"{lowedge} {self.binwidth} {self.bins[i]}\n"
        z += f'# out of range = {self.outofrange}\n'
        return z
    # end __str__

    # Next, define cContainer like behavior
    def __getitem__(self, k):
        return self.bins[k]

    def __setitem__(self, k, v):
        self.bins[k] = v

    def __len__(self) -> int:
        return len(self.nbins)

    def fast_index(self, x) -> int:
        ' false index finder '
        return 0

    def __iter__(self):
        ''' provides iteration over bin directly '''
        return iter(self.bins)

    def fast_fill(self, x: float,
                  w: int = 1):
        ' false filler '
        pass
# end of class

# EOF
