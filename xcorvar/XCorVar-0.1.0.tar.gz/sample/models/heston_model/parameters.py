# coding: utf-8

import math as mth

class VarParams:

    #public:

        def __init__ (self, v0, kappa, theta, eta, verbose=0):
            self.v0 = v0
            self.kappa = kappa
            self.theta = theta
            self.eta = eta
            if verbose > 0:
                threshold = self.eta ** 2 / (2 * self.kappa * self.theta)
                if threshold > 1: print ('variance might be negative')
                else: print ('variance cannot be negative')

class HestonParams:

    #public:

        def __init__ (self, rate, spot, var, rho):
            self.rate = rate
            self.spot = spot
            self.var = var
            self.rho = rho

        def dsc (self, mat, time=0):
            return mth.exp (-self.rate * (mat - time))

        def fwd (self, mat, time=0):
            return self.spot / self.dsc (mat, time)

        def dsc_fwd (self, mat, time=0):
            dsc = self.dsc (mat, time)
            fwd = self.spot / dsc
            return dsc, fwd