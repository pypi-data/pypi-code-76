# coding: utf-8

import math as mth

from pricing.option import Payoff, Opt
from toolbox.monte_carlo.monte_carlo import MonteCarlo
from toolbox.monte_carlo.batch_monte_carlo import BatchMonteCarlo
from toolbox.func_tools import Join, Comp
from toolbox.black_scholes_functions import get_black_scholes_call_std_price
from toolbox.reduce_var.ctrl_var import SubCtrlVar
from toolbox.diffusion import MultiEulerScheme, ONE_DAY

class AsOptOneDim (Opt):

    #public:

        def __init__ (self, payoff, mat):
            super ().__init__ (payoff, mat)

class AsCallOpt (AsOptOneDim):

    #public:

        def __init__ (self, mat, strike, frame=None):
            func = lambda mean: mean - strike if mean > strike else 0
            payoff = Payoff (func)
            super ().__init__ (payoff, mat)
            self.strike = strike
            self.frame = [0, mat] if frame is None else frame

    #price:
        
        def black_scholes_price (self, mdl):
            mat0, mat1 = self.frame
            if mat1 <= mat0: return 0
            spot_like = mdl.params.spot * mth.exp ((-mdl.params.rate / 2 - mdl.params.vol ** 2 / 12) * mat1)
            vol_like = mdl.params.vol / mth.sqrt (3)
            dsc = mdl.params.dsc (mat1)
            mean = get_black_scholes_call_std_price (mat1, self.strike, spot_like, mdl.params.rate, vol_like) / dsc
            return MonteCarlo (X=SubCtrlVar (mdl.mean2, mean, self.payoff.func, self.payoff.func), kwargs={'frame' : self.frame, 'eps' : 1e-1}, s=dsc) 
        
        def heston_price (self, mdl, scheme=MultiEulerScheme, step=ONE_DAY):
            mat0, mat1 = self.frame
            if mat1 <= mat0: return 0
            dsc1, fwd1 = mdl.params.dsc_fwd (mat1)
            dsc0 = mdl.params.dsc (mat0)
            scaled_fwd1 = fwd1 * (1 - dsc1 / dsc0) / (mdl.params.rate * (mat1 - mat0))
            payoff_like_func = lambda mean: mean - scaled_fwd1
            diffusion = mdl.diffusion (scheme, step)
            return BatchMonteCarlo (join=Comp (Join (self.payoff.func, payoff_like_func), mdl.mean), kwargs={'frame' : self.frame, 'diffusion' : diffusion, 'verbose' : 0}, s=dsc1)