#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: 2019 05 02 -*-
# -*- copyright: GH/IPHC 2019 -*-
# -*- file: findpeaks.py -*-
# -*- purpose: -*-

'''
FindPeaks method
'''
from pyhisto import Histogram


class FindPeaks:
    '''From an histogram object, find n peakes'''
    def __init__(self,
                 h: Histogram,
                 npeaks: int = 1,
                 width: float = 1.0):
        '''
        npeak=int, width=float (if negative: relative width)
        '''
        sorted_bins = sorted(h.bins, reverse=True)
        self.peaks = []
        width_func = lambda x: width
        if width < 0.:
            width_func = lambda x: abs(width) * x
        self.peaks.append(sorted_bins.pop(0))
        for b in sorted_bins:
            if all([abs(p.lowedge - b.lowedge) > width_func(p.lowedge) for p in self.peaks]) \
               and len(self.peaks) < npeaks:
                self.peaks.append(b)
            # end if
        self.peaks = sorted(self.peaks, key=lambda b: b.lowedge)
        # end for
# end findpeaks

# EOF
