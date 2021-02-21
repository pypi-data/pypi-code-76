# coding: utf-8

import math as mth

from toolbox.black_scholes_functions import GeoBrown

class BiBlackScholesParams:

    #public:

        def __init__ (self, spot1, spot2, rate, vol1, vol2, rho):
            self.spot1 = spot1
            self.spot2 = spot2
            self.vol1 = vol1
            self.vol2 = vol2
            self.rate = rate
            self.rho = rho

        @property
        def mu1 (self):
            return self.rate - 0.5 * self.vol1 ** 2

        @property
        def mu2 (self):
            return self.rate - 0.5 * self.vol2 ** 2

        @property
        def bar_rho (self):
            return mth.sqrt (1 - self.rho ** 2)

        def dsc (self, mat, time=0):
            return mth.exp (-self.rate * (mat - time))

        def fwd1 (self, mat, time=0):
            return self.spot1 / self.dsc (mat, time)

        def fwd2 (self, mat, time=0):
            return self.spot2 / self.dsc (mat, time)
        
        def func1 (self, time, brown):
            return GeoBrown (self.spot1, self.mu1, self.vol1) (time, brown)

        def func2 (self, time, brown):
            return GeoBrown (self.spot2, self.mu2, self.vol2) (time, brown)

        def func_like (self, time, brown):
            return GeoBrown (self.spot1, -0.5 * self.rho ** 2 * self.vol1 ** 2, self.vol1 * self.rho) (time, brown)
