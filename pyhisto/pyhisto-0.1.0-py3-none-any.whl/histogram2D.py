#!/usr/env python
# -*- coding: utf-8 -*-
# -*- format: python -*-
# -*- author: G. Henning -*-
# -*- created: Fri Aug 11 10:22:50 CEST 2017 -*-
# -*- copyright: GH/IPHC 2017 -*-
# -*- file: histogram2D.py -*-
# -*- purpose: -*-

'''
The module contain the Histogram2D class.
'''


from math import floor

from typing import Union, Optional

# importing 1D histogram to export projections
from pyhisto.histogram import Histogram


class Histo2DError(Exception):
    '''2D Histogram error '''


class Histogram2D:
    ''' Implement 2D hisotgram'''
    def __init__(self,
                 xnbins: int = 1,
                 xmin: Optional[float] = None,
                 xmax: Optional[float] = None,
                 ynbins: int = 1,
                 ymin: Optional[float] = None,
                 ymax: Optional[float] = None,
                 fromstring: Optional[str] = None,
                 fromarray: Optional[Union[list, tuple]] = None,
                 fromdict: Optional[dict] = None):
        '''Initilize the Hisotgram2D

        - Using a string, as exported from str(histo2d) using
        ``Histogram2D(fromstring=z)``

        - Using a dictionnary, as obtained from repr, using
        ``Histogram2D(fromdict=d)`` (not implemented yet)

        - Using an array of values, which will be indexed naturally,
        ``Histogram2D(fromarray=a)`` (not implemented yet)

        - From 'nothing', using
        ``Histogram2D(nxbins, xmin, xmax, nybins, ymin, ymax)``
        '''
        if fromstring:
            self._fromstring(fromstring)
        elif fromarray:
            raise NotImplementedError
        elif fromdict:
            raise NotImplementedError
        else:
            self.xnbins: int = xnbins
            self.ynbins: int = ynbins
            self.xmin: float = -0.5 if xmin is None else xmin
            self.xmax: float = self.xmin + self.xnbins if xmax is None else xmax
            self.ymin: float = -0.5 if ymin is None else ymin
            self.ymax: float = self.ymin + self.ynbins if ymax is None else ymax
            if self.xmin == self.xmax:
                raise Histo2DError("X Bounds values in histogram should be different")
            if self.ymin == self.ymax:
                raise Histo2DError("Y Bounds values in histogram should be different")
            self.xmin, self.xmax = min(self.xmax, self.xmin), max(self.xmax, self.xmin)
            self.ymin, self.ymax = min(self.ymax, self.ymin), max(self.ymax, self.ymin)
            self.xbinwidth: float = (self.xmax - self.xmin) / float(self.xnbins)
            self.ybinwidth: float = (self.ymax - self.ymin) / float(self.ynbins)
            self.bins: list = [[0 for j in range(self.ynbins)]
                               for i in range(self.xnbins)]
            self.outofrange: float = 0
            self.export_threshold: float = 0.
        # end if
    # end __init__

    def _fromstring(self, instr: str):
        '''This function imports an histogram from a string,
        formatted as the output of __str__'''
        lines = instr.split('\n')
        self.outofrange = 0
        for l in lines:
            if l.startswith("# xnbins"):
                self.xnbins = int(l.split('=')[1])
            elif l.startswith("# xmin"):
                self.xmin = float(l.split('=')[1])
            elif l.startswith("# xmax"):
                self.xmax = float(l.split('=')[1])
            elif l.startswith("# ynbins"):
                self.ynbins = int(l.split('=')[1])
                self.bins = [[0 for j in range(self.ynbins)]
                             for i in range(self.xnbins)]
            elif l.startswith("# ymin"):
                self.ymin = float(l.split('=')[1])
            elif l.startswith("# ymax"):
                self.ymax = float(l.split('=')[1])
            elif l.startswith("# out of range"):
                self.outofrange = float(l.split('=')[1])
            else:
                if len(l.split()) == 3:
                    try:
                        i, j, c = l.split()
                        self.bins[int(i)][int(j)] = float(c)
                    except Exception:
                        pass
            # end if
        # end for lines
        self.xbinwidth = (self.xmax - self.xmin) / float(self.xnbins)
        self.ybinwidth = (self.ymax - self.ymin) / float(self.ynbins)
        self.export_threshold = 0.

    def __str__(self):
        '''Dump the histogram in string format'''
        z = ''
        z += '# xnbins = {0}\n'.format(self.xnbins)
        z += '# xmin = {0}\n'.format(self.xmin)
        z += '# xmax = {0}\n'.format(self.xmax)
        z += '# ynbins = {0}\n'.format(self.ynbins)
        z += '# ymin = {0}\n'.format(self.ymin)
        z += '# ymax = {0}\n'.format(self.ymax)
        if self.export_threshold > 0:
            z += '# Exporting bins with more than {0} counts\n'.format(self.export_threshold)
        for i in range(0, self.xnbins):
            for j in range(0, self.ynbins):
                if self.bins[i][j] > self.export_threshold:
                    z += "{0} {1} {2} \n".format(i, j, self.bins[i][j])
        z += '# out of range = {0}\n'.format(self.outofrange)
        return z
    # end __str__

    def __repr__(self):
        '''Writting the histogram2D as a dictionnary'''
        z = "{"
        z += "   'xnbins':{0},\n".format(self.xnbins)
        z += "   'xmin':{0},\n".format(self.xmin)
        z += "   'xmax':{0},\n".format(self.xmax)
        z += "   'ynbins':{0},\n".format(self.ynbins)
        z += "   'ymin':{0},\n".format(self.ymin)
        z += "   'ymax':{0},\n".format(self.ymax)
        z += "   'outofrange':{0},\n".format(self.outofrange)
        z += "   'bins':{0},\n".format(str(self.bins))
        z += "}"
        return z
    # end __repr__

    def todict(self) -> dict:
        '''Return the histogram as a dict'''
        return eval(repr(self))

    def copy(self) -> 'Histogram2D':
        '''Return a copy of the histogram'''
        return Histogram2D(fromstring=str(self))

    def empty(self):
        '''Sets all bin content to 0'''
        self.outofrange = 0
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                self.bins[i][j] = 0

    def empty_copy(self) -> 'Histogram2D':
        '''Returns an empty copy (i.e. preserved just the axis)'''
        return self.copy().empty()

    def rescale(self,
                newxmin: Optional[float] = None,
                newxmax: Optional[float] = None,
                newymin: Optional[float] = None,
                newymax: Optional[float] = None):
        '''Change the scale, compute new bin width, ....'''
        if newxmin is not None:
            self.xmin = newxmin
        if newxmax is not None:
            self.xmax = newxmax
        if newymin is not None:
            self.ymin = newymin
        if newymax is not None:
            self.ymax = newymax
        self.xbinwidth = (self.xmax - self.xmin) / float(self.xnbins)
        self.ybinwidth = (self.ymax - self.ymin) / float(self.ynbins)

    def dim(self) -> tuple:
        '''Alternative to len, for 2D'''
        return self.xnbins, self.ynbins

    def sum(self) -> float:
        '''compute the sum, because sum() does not work on 2D'''
        S = 0.0
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                S += self.bins[i][j]
        return S

    def max(self) -> dict:
        '''returns position and value of maximum'''
        the_i, the_j, the_max = 0, 0, 0.0
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                if self.bins[i][j] > the_max:
                    the_i, the_j, the_max = i, j, self.bins[i][j]
                 # end if
             # end for j
         # end for i
        return {'i': the_i, 'j': the_j, 'max': the_max}

    def scale(self, S: float = 1.):
        '''Mutliply the content by S'''
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                self.bins[i][j] *= S
            # end for j
        # end for i

    def getbin(self, x: float, y: float) -> dict:
        '''return a bin information'''
        i, j = self.findbin(x, y)
        return {'i': i, 'j': j,
                'x': x, 'y': y,
                'lowedge': self.getbinlowedge(i, j),
                'updedge': self.getbinupedge(i, j),
                'count': self.bins[i][j]}

    def findbin(self, x: float, y: float) -> tuple:
        '''find a bin and returns the indices'''
        i, j = -1, -1
        if x >= self.xmin and x < self.xmax:
            i = int(floor((x - self.xmin) / self.xbinwidth))
        if y >= self.ymin and y < self.ymax:
            j = int(floor((y - self.ymin) / self.ybinwidth))
        return i, j
    # end FindBin

    def fill(self,
             x: float, y: float,
             w: float = 1.):
        '''Add one (or w) counts to bin corresponding to x

        Keyword Arguments:
        x,y -- (float)
        w -- (float) default =1'''
        i, j = self.findbin(x, y)
        if i >= 0 and j >= 0:
            try:
                self.bins[i][j] += w
            except IndexError:
                self.outofrange += w
        else:
            self.outofrange += w
    # End Fill

    def fast_fill(self,
                  x: float, y: float,
                  w: float = 1):
        '''Add one (or w) counts to the bin, in a fast way'''
        try:
            self.bins[int((x - self.xmin) / self.xbinwidth)][int((y - self.ymin) / self.ybinwidth)] += w
        except IndexError:
            self.outofrange += w

    def very_fast_fill(self,
                       i: int, j: int,
                       w: float = 1):
        ''' add one (or w) counts to the bin identified with i,j'''
        try:
            self.bins[i][j] += w
        except IndexError:
            self.outofrange += w

    def getbincenter(self, i: int, j: int) -> tuple:
        'Returns bin center'
        return self.xmin + (i + 0.5) * self.xbinwidth, self.ymin + (j + 0.5) * self.ybinwidth

    def getbinlowedge(self, i: int, j: int) -> tuple:
        'Returns bin lowedge'
        return self.xmin + i * self.xbinwidth, self.ymin + j * self.ybinwidth

    def getbinupedge(self, i: int, j: int) -> tuple:
        'Returns bin upedge'
        return self.xmin + (i + 1.) * self.xbinwidth, self.ymin + (j + 1.) * self.ybinwidth

    def xyz(self, mode: str = 'lowedge') ->tuple:
        'Returns XYZ data map for plotting'
        X = tuple((self.getbinlowedge(i, 0)[0] for i in range(self.xnbins + 1)))
        Y = tuple((self.getbinlowedge(0, j)[1] for j in range(self.ynbins + 1)))
        Z = tuple(zip(*self.bins))
        return X, Y, Z

    def project_x(self,
                  ymin: float = -1,
                  ymax: float = -1) -> Histogram:
        '''project the histogram content on the X axis'''
        jmin = self.findbin(self.xmin, ymin)[1]
        jmax = self.findbin(self.xmin, ymax)[1]
        if ymin == -1:
            jmin = 0
        if ymax == -1:
            jmax = self.ynbins
        d = [sum([self.bins[i][j] for j in range(jmin, jmax)]) for i in range(self.xnbins)]
        h = Histogram(self.xnbins, self.xmin, self.xmax)
        for i in range(self.xnbins):
            h.bins[i].count += d[i]
        return h

    def project_y(self,
                  xmin: float = -1,
                  xmax: float = -1) -> Histogram:
        '''project the histogram content on the X axis'''
        imin = self.findbin(xmin, self.ymin)[0]
        imax = self.findbin(xmax, self.ymin)[0]
        if xmin == -1:
            imin = 0
        if xmax == -1:
            imax = self.xnbins
        d = [sum([self.bins[i][j] for i in range(imin, imax)]) for j in range(self.ynbins)]
        h = Histogram(self.ynbins, self.ymin, self.ymax)
        for j in range(self.ynbins):
            h.bins[j].count += d[j]
        return h

    def rebin(self,
              newbinx: int = -1,
              newbiny: int = -1) -> 'Histogram2D':
        '''Return a new histogram with same limits but different number of bins'''
        if newbinx == -1:
            newbinx = self.xnbins
        if newbiny == -1:
            newbiny = self.ynbins
        rh = Histogram2D(newbinx,
                         self.xmin, self.xmax,
                         newbiny,
                         self.ymin, self.ymax)
        # Now filling the new histogram!
        for i in range(self.xnbins):
            for j in range(self.ynbins):
                x, y = self.getbincenter(i, j)
                rh.fill(x, y, self.bins[i][j])
        return rh

    def subhisto(self,
                 xmin: float = -1, xmax: float = -1,
                 ymin: float = -1, ymax: float = -1) -> 'Histogram2D':
        '''Return a new 2D histogram, with only the selected range'''
        # First, select
        jmin = self.findbin(self.xmin, ymin)[1]
        jmax = self.findbin(self.xmin, ymax)[1]
        imin = self.findbin(xmin, self.ymin)[0]
        imax = self.findbin(xmax, self.ymin)[0]
        if xmin == -1:
            imin = 0
        if xmax == -1:
            imax = self.xnbins
        if ymin == -1:
            jmin = 0
        if ymax == -1:
            jmax = self.ynbins
        jmin, jmax = min(jmin, jmax), max(jmin, jmax)
        imin, imax = min(imin, imax), max(imin, imax)
        subh = Histogram2D(imax-imin,
                           self.getbinlowedge(imin, jmin)[0],
                           self.getbinlowedge(imax, jmin)[0],
                           jmax - jmin,
                           self.getbinlowedge(imin, jmin)[1],
                           self.getbinlowedge(imin, jmax)[1])
        subh.bins = [[self.bins[i][j] for j in range(jmin, jmax)]
                     for i in range(imin, imax)]
        return subh

    def autocrop(self, threshold: float = 0):
        '''Cut the bins that are 'empty' '''
        # Find the first i,j that is above threshold

        # use specialized function:
        def _ifromthetop():
            for i in range(self.xnbins):
                for j in range(self.ynbins):
                    if self.bins[i][j] > threshold:
                        return i
            return -1

        def _jfromthetop():
            for j in range(self.ynbins):
                for i in range(self.xnbins):
                    if self.bins[i][j] > threshold:
                        return j
            return -1

        def _ifromthebottom():
            for i in range(self.xnbins - 1, 0, -1):
                for j in range(self.ynbins - 1, 0, -1):
                    if self.bins[i][j] > threshold:
                        return i
            return 0

        def _jfromthebottom():
            for j in range(self.ynbins - 1, 0, -1):
                for i in range(self.xnbins - 1, 0, -1):
                    if self.bins[i][j] > threshold:
                        return j
            return 0

        i_top, j_top = _ifromthetop(), _jfromthetop()
        i_bot, j_bot = _ifromthebottom(), _jfromthebottom()
        i_top, i_bot = max(i_top, i_bot), min(i_top, i_bot)
        j_top, j_bot = max(j_top, j_bot), min(j_top, j_bot)
        xmin, ymin = self.getbinlowedge(i_bot, j_bot)
        xmax, ymax = self.getbinupedge(i_top, j_top)
        return self.subhisto(xmin, xmax, ymin, ymax)
# end of class

# EOF
