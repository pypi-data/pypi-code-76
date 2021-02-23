# coding: utf-8

import math as mth

from sample.toolbox.random_variable import Normal

class BlackScholesTermStructureSample:

    #public:

        def __init__ (self, spot, fwd, tot_var):
            '''
            Simulate market values from Black Scholes term structure model

            :param float spot: mid spot value
            :param float fwd: mid forward value at maturity
            :param float tot_var: Total variance at maturity
            '''
            self.spot = spot 
            self.fwd = fwd
            self.tot_var = tot_var
            self.noise = Normal (-0.5 * tot_var, mth.sqrt (tot_var))

        def func (self, noise):
            return self.fwd * mth.exp (noise)

        def __call__ (self, gen):
            return self.func (self.noise (gen))

class BlackScholesTermStructureModel:

    #public:

        def __init__ (self, spot, fwd, tot_var, dsc_repo):
            '''
            Black Scholes Term Structure Model

            :param float spot: mid spot value
            :param float fwd: mid forward value at maturity
            :param float tot_var: Total variance at maturity
            :param float dsc_repo: Discount repo factor at maturity
            '''
            self.spot = spot
            self.fwd = fwd
            self.tot_var = tot_var
            self.dsc_repo = dsc_repo
