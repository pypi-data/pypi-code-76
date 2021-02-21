# coding: utf-8

import math as mth
import numpy as np

from pricing.option import Opt, Payoff
from models.multi_black_scholes_model.model import MultiBlackScholesMdl
from toolbox.monte_carlo import MonteCarlo
from toolbox.func_tools import Comp
from toolbox.black_scholes_functions import get_black_scholes_call_std_price
from toolbox.mathbox import prod
from toolbox.reduce_var.ctrl_var import SubCtrlVar

class EuOptMultiDim (Opt):

    #public:

        def __init__ (self, payoff, mat):
            super ().__init__ (payoff, mat)

        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            return MonteCarlo (X=Comp (self.payoff.func, mdl.spot), kwargs={'time' : mat}, s=mdl.params.dsc (mat))

class BestOfCallOpt (EuOptMultiDim):

    #public:

        def __init__ (self, mat, strike, scale):
            func = lambda spots: max (np.max (spots) - strike, 0)
            ctrl_func = lambda spots: max (prod ([spot ** scale for spot in spots]) - strike, 0)
            super ().__init__ (Payoff (func).add_ctrl_func (ctrl_func), mat)
            self.strike = strike
            self.scale = scale

    #price:
        
        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            half_vol = self.scale * mdl.params.vol
            var = half_vol.T @ mdl.params.corr @ half_vol
            sm = self.scale * np.sum (mdl.params.vol ** 2)
            vol = mth.sqrt (var)
            powers = [spot ** self.scale for spot in mdl.params.spot]
            spot = prod (powers) * mth.exp (-0.5 * (sm - var) * mat)
            mean = get_black_scholes_call_std_price (mat, self.strike, spot, mdl.params.rate, vol)
            MonteCarlo (X=SubCtrlVar (mdl.spot, mean, self.payoff.func, self.payoff.ctrl_func), kwargs={'time' : mat}, s=mdl.params.dsc (mat))

class IdxOpt (EuOptMultiDim):

    #public:

        def __init__ (self, mat, strike, wghts):
            func = lambda spot: max (np.dot (wghts, spot) - strike, 0)
            ctrl_func = lambda spots: max (prod ([spot ** wght for spot, wght in zip (spots, wghts)]) - strike, 0)
            super ().__init__ (Payoff (func).add_ctrl_func (ctrl_func), mat)
            self.strike = strike
            self.wghts = wghts
            
    #price:

        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            wghts_vol = self.wghts * mdl.params.vol
            var = wghts_vol.T @ mdl.params.corr @ wghts_vol
            sm = np.dot (wghts_vol, mdl.params.vol)
            vol = mth.sqrt (var)
            powers = [spot ** wght for spot, wght in zip (mdl.params.spot, self.wghts)]
            spot = prod (powers) * mth.exp (-0.5 * (sm - var) * mat)
            mean = get_black_scholes_call_std_price (mat, self.strike, spot, mdl.params.rate, vol)
            return MonteCarlo (X=SubCtrlVar (mdl.spot, mean, self.payoff.func, self.payoff.ctrl_func), kwargs={'time' : mat}, s=mdl.params.dsc (mat))