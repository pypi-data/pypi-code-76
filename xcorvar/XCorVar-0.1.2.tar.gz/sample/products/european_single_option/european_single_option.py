# coding: utf-8

import math as mth

from sample.pricing.option import Payoff, Option
from sample.toolbox.monte_carlo.monte_carlo import MonteCarlo
from sample.toolbox.func_tools import Comp, Join
from sample.toolbox.monte_carlo.batch_monte_carlo import BatchMonteCarlo
from sample.toolbox.reduce_var.anti_var import SubAntiVar
from sample.toolbox.diffusion import EulerScheme, MultiEulerScheme, ONEDAY
from sample.toolbox.black_scholes_functions import *

class EuropeanOptionOneDim (Option):

    #public:

        def __init__ (self, payoff, mat):
            super ().__init__ (payoff, mat)

    #price:
        
        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            return MonteCarlo (X=SubAntiVar (Comp (self.payoff.func, mdl.to_spot (mat)), lambda x: -x, mdl.brown), kwargs={'time' : mat}, s=mdl.params.dsc (mat))

        def heston_price (self, mdl, time=0, scheme=MultiEulerScheme, step=ONEDAY):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            diffusion = mdl.diffusion (scheme, step)
            return MonteCarlo (X=Comp (self.payoff.func, mdl.spot), kwargs={'time' : mat, 'diffusion' : diffusion, 'verbose' : 0}, s=mdl.params.dsc (mat))

    #delta:

        def black_scholes_delta (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return 1
            fwd = mdl.params.fwd (mat)
            vol = mdl.params.vol
            if self.payoff.grad is None: return MonteCarlo (Comp (lambda X, W: self.payoff.func (X) * W, mdl.spot_brown), s=1/(fwd * vol * mat), kwargs={'time' : mat})
            else: return MonteCarlo (Comp (lambda X: (self.payoff.grad (X) - self.payoff.grad (fwd)) * X, mdl.spot), s=1/(fwd * vol * mat), kwargs={'time' : mat})

    #dollargamma:

        def black_scholes_dollargamma (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return None
            vol_mat = mdl.params.vol * mat
            if self.payoff.grad is None: return MonteCarlo (Comp (lambda X, W: self.payoff.func (X) * (W ** 2 / vol_mat - W - 1 / mdl.params.vol), mdl.spot_brown), s=mdl.params.dsc (mat)/vol_mat, kwargs={'time' : mat})
            else: return MonteCarlo (Comp (lambda X, W: (self.payoff.grad (X) * X - self.payoff.func (X)) * W, mdl.spot_brown), s=mdl.params.dsc (mat)/vol_mat, kwargs={'time' : mat})

    #vega:

        def black_scholes_vega (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return None
            dsc = mth.exp (-mdl.params.rate * mat)
            vol = mdl.params.vol
            vol_mat = vol * mat
            sample = lambda gen: mdl.spot_brown (mat, gen)
            if self.payoff.grad is None: func = lambda X, W: self.payoff.func (X) * (W ** 2 / vol_mat - W - 1 / vol)
            else: func = lambda X, W: self.payoff.grad (X) * X * (W - vol_mat)
            return MonteCarlo (Comp (func, sample), k=dsc, c=0)
            
class EuropeanCallOption (EuropeanOptionOneDim):

    #public:

        def __init__ (self, mat, strike):
            func = lambda spot: spot - strike if spot > strike else 0
            grad = lambda spot: 1 if spot > strike else 0
            payoff = Payoff (func, grad)
            super ().__init__ (payoff, mat)
            self.strike = strike

    #price:
        
        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            return get_black_scholes_call_price_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

        def heston_price (self, mdl, time=0, scheme=MultiEulerScheme, step=ONEDAY):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            dsc, fwd = mdl.params.dsc_fwd (mat)
            payoff_like_func = lambda spot, var: spot - fwd
            diffusion = mdl.diffusion (scheme, step)
            return BatchMonteCarlo (join=Comp (Join (self.payoff.func, payoff_like_func), mdl.spot), kwargs={'time' : mat, 'diffusion' : diffusion, 'verbose' : 0}, s=dsc)

    #delta:
        
        def black_scholes_delta (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return 1
            return get_black_scholes_call_delta_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

    #dollargamma:

        def black_scholes_dollargamma (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return None
            return get_black_scholes_call_dollargamma_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

    #vega

        def black_scholes_vega (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return None
            return get_black_scholes_call_vega_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

    #pricer:

        def black_scholes_pricer (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot), 1, None
            return get_black_scholes_call_price_delta_dollargamma_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

class EuropeanPutOption (EuropeanOptionOneDim):

    #public:

        def __init__ (self, mat, strike):
            func = lambda spot: strike - spot if strike > spot else 0
            grad = lambda spot: -1 if strike > spot else 0
            payoff = Payoff (func, grad)
            super ().__init__ (payoff, mat)
            self.strike = strike

    #price:
        
        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            return get_black_scholes_put_price_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

    #delta:
        
        def black_scholes_delta (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return 0
            return get_black_scholes_put_delta_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

    #dollargamma:

        def black_scholes_dollargamma (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return None
            return get_black_scholes_put_dollargamma_std (mat, self.strike, mdl.params.vol, mdl.params.spot, mdl.params.rate, mdl.params.repo)

class EuropeanCallSpreadOption (EuropeanOptionOneDim):
    
    def __call__ (self, mat, strike1, strike2):
        return EuropeanCallOption (mat, strike1) - EuropeanCallOption (mat, strike2)

class EuropeanCalendarCallSpreadOption (EuropeanOptionOneDim):
    
    def __call__ (self, mat1, mat2, strike):
        return EuropeanCallOption (mat1, strike) - EuropeanCallOption (mat2, strike)

class EuropeanButterflyCallOption (EuropeanOptionOneDim):

    def __call__ (self, mat, strike_lft, strike_mid, strike_rgt):
        return EuropeanOptionOneDim (mat, strike_rgt) - 2 * EuropeanOptionOneDim (mat, strike_mid) + EuropeanOptionOneDim (mat, strike_lft)
    
