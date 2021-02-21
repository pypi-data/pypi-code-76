# coding: utf-8

from pricing.option import Opt, Payoff
from toolbox.monte_carlo.monte_carlo import MonteCarlo
from toolbox.func_tools import Comp
from toolbox.black_scholes_functions import get_black_scholes_call_std_price
from toolbox.reduce_var.anti_var import SubAntiVar

class EuPairOpt (Opt):

    #public:

        def __init__ (self, payoff, mat):
            super ().__init__ (payoff, mat)

    #price:

        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            return MonteCarlo (X=Comp (self.payoff.func, mdl.spots), kwargs={'time' : mat}, s=mdl.params.dsc (mat))

class ExchangeCallSpreadOpt (EuPairOpt):

    #public:

        def __init__ (self, mat, strike):
            func = lambda spot1, spot2: max (spot1 - spot2 - strike, 0)
            super ().__init__ (Payoff (func), mat)
            self.strike = strike

    #price:
        
        def black_scholes_price (self, mdl, time=0):
            mat = self.mat - time
            if mat <= 0: return self.payoff.func (mdl.params.spot)
            rate = mdl.params.rate
            vol = mdl.params.vol1 * mdl.params.bar_rho
            spot = lambda brown: mdl.to_spot_like (time) (brown)
            strike = lambda brown: self.strike + mdl.to_spot2 (time) (brown)
            call_black_scholes = lambda brown: get_black_scholes_call_std_price (mat, strike (brown), spot (brown), rate, vol)
            return MonteCarlo (X=SubAntiVar (call_black_scholes, lambda x: -x, mdl.brown), kwargs={'time' : mat})
        