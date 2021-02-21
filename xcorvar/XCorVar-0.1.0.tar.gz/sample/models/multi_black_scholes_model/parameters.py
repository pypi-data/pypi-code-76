# coding: utf-8

import math as mth

from toolbox.black_scholes_functions import GeoBrown

class MultiBlackScholesParams:

    #public:

        def __init__ (self, spot, rate, vol, corr):
            self.spot = spot
            self.rate = rate
            self.vol = vol
            self.corr = corr

        @property
        def mu (self):
            return self.rate - 0.5 * self.vol ** 2

        @property
        def dim (self):
            return len (self.spot)

        def dsc (self, mat, time=0):
            return mth.exp (-self.rate * (mat - time))

        def fwd (self, mat, time=0):
            return self.spot / self.dsc (mat, time)

        def dsc_fwd (self, mat, time=0):
            dsc = self.dsc (mat, time)
            fwd = self.spot / dsc
            return dsc, fwd
        
        def func (self, time, brown):
            return GeoBrown (self.spot, self.mu, self.vol) (time, brown)
