#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Aug 11 10:22:50 CEST 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file: histogram2D.py -*-
# -*- purpose: -*-

'''
The module contain a Ghost Histogram2D class.
'''


class GhostHistogram2D:
    ''' Implement 2D hisotgram'''

    def __init__(self,
                 xnbins=1, xmin=None, xmax=None,
                 ynbins=1, ymin=None, ymax=None):
        '''Initilize the Ghost Hisotgram2D

        ``Histogram2D(nxbins, xmin, xmax, nybins, ymin, ymax)``
        '''
        self.xnbins = 1
        self.ynbins = 1
        self.xmin = -0.5
        self.xmax = 0.5
        self.xbinwidth = 1
        self.ymin = -0.5
        self.ymax = 0.5
        self.ybinwidth = 1
        self.bins = [[0]]
        self.outofrange = 0
        self.export_threshold = 0.
    # end __init__

    def __str__(self):
        '''Dump the histogram in string format'''
        z = f'# xnbins = {self.xnbins}\n'
        z += f'# xmin = {self.xmin}\n'
        z += f'# xmax = {self.xmax}\n'
        z += f'# ynbins = {self.ynbins}\n'
        z += f'# ymin = {self.ymin}\n'
        z += f'# ymax = {self.ymax}\n'
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

    def fast_fill(self, x, y, w=1):
        '''Add one (or w) counts to the bin, in a fast way'''
        pass
# end class

# EOF
