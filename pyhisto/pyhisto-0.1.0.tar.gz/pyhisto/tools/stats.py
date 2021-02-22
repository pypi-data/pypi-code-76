#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Tue Dec  4 11:23:33 CET 2018 -*-
# -*- copyright: GH/IPHC 2018 -*-
# -*- file: stats.py -*-
# -*- purpose: -*-

'''
Returns a stat object

(Could use a namedtuple, but kept this way for historical reason)
'''

from math import sqrt

from pyhisto import Histogram


class Stats:
    '''From an histogram object, computes statistics and keep them int he object'''
    def __init__(self,
                 h: Histogram):
        '''computes sum, average x, stddev, max, bin'''
        self.sum = sum(h)
        self.average_count = self.sum / len(h)
        self.max = max(h)
        self.mean = sum([b.center() * b.count for b in h]) / self.sum
        self.stddev = sqrt(sum([b.count * b.center() ** 2.0 for b in h]) / self.sum - self.mean ** 2.0)

    def __repr__(self):
        return f"""{{'sum': {self.sum},
'max': {self.max},
'average_count': {self.average_count},
'mean': {self.mean},
'stddev': {self.stddev},
}}"""
# end class

# EOF
