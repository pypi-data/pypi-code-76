# coding: utf-8

import math as mth

from toolbox.black_scholes_functions import GeoBrown

class BlackScholesParams:

    #public:

    def __init__ (self, vol, spot=1, rate=0, repo=0):
        self.vol = vol
        self.spot = spot
        self.rate = rate
        self.rate_minus_repo = rate - repo
        self.repo = repo

    @property
    def mu (self):
        return self.rate_minus_repo - 0.5 * self.vol ** 2

    def dsc (self, mat, time=0):
        return mth.exp (-self.rate_minus_repo * (mat - time))

    def dsc_2 (self, mat, time=0):
        return mth.exp (-self.rate * (mat - time))

    def fwd (self, mat, time=0):
        return self.spot / self.dsc (mat, time)

    def dsc_fwd (self, mat, time=0):
        dsc = self.dsc (mat, time)
        fwd = self.spot / dsc
        dsc = self.dsc_2 (mat, time)
        return dsc, fwd

    def func (self, time, brown):
        return GeoBrown (self.spot, self.mu, self.vol) (time, brown)
