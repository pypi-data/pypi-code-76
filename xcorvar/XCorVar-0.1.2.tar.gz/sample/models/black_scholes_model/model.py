# coding: utf-8

import math as mth
import numpy as np

from sample.constants import Constants
from sample.toolbox.random_variable import StandardNormalMarsaglia
from sample.toolbox.diffusion.scheme import BlackScholesScheme
from sample.toolbox.diffusion.diffusion import Diffusion
from sample.toolbox.integral.functionnal_brownian_integral import RandomIntegral

class BlackScholesSample:

    #public:

        def __init__ (self, spot, rate, repo, vol):
            self.spot = spot 
            self.repo = repo
            self.vol = vol
            self.mu = rate - repo - 0.5 * vol * vol
            self.noise = StandardNormalMarsaglia ()

        def get_brownian_sample (self, time, gen):
            return mth.sqrt (time) * self.noise (gen)

        def geometric_brownian_functionnal (self, time, brown):
            return self.spot * np.exp (self.vol * brown + self.mu * time)

        def __call__ (self, time, gen):
            return self.geometric_brownian_functionnal (time, self.get_brownian_sample (time, gen))

        def get_mean_spot_sample (self, frame, eps=1e-1):
            t0, t1 = frame
            return RandomIntegral (self.geometric_brownian_functionnal, t0, t1, self.noise).run (eps).curr.val

class BlackScholesDiffusion:

    #public:

        def __init__ (self, spot, rate, repo, vol, step=Constants.ONE_DAY):
            self.diffusion = Diffusion (BlackScholesScheme (spot, vol, rate - repo - 0.5 * vol * vol, step))

        def get_trajectory_sample (self, mat):
            self.diffusion.restart ().run (mat).plt ()

class BlackScholesModel:

    #public:

        def __init__ (self, spot, rate, repo, vol):
            self.spot = spot
            self.rate = rate
            self.repo = repo
            self.vol = vol
            
'''
def get_mean_spot_and_ctrl_mean_spot_sample (self, frame, eps=1e-1):
    t0, t1 = frame
    func_geo_brown_int = FuncBrownInt (self.func, t0, t1, self.noise).run (eps)
    mean_geo_brown = func_geo_brown_int.curr.val / t1
    mean_brown = get_mean_brown (t1, [pt.y for pt in func_geo_brown_int.curr.pts], func_geo_brown_int.noise ())
    spot_like = self.spot * mth.exp ((-self.rate / 2 - (self.vol ** 2) / 12) * t1)
    vol_like = self.vol / mth.sqrt (3)
    mean_geo_brown_ctrl = GeoBrown (spot_like, self.mu, self.vol) (t1, mean_brown)
    return mean_geo_brown, mean_geo_brown_ctrl
'''

'''
def to_spot (self, time):
    return lambda brown: GeoBrown (self.spot, self.mu, self.vol) (time, brown)

def spot_brown (self, time=0):
    brown = self.brown (time)
    spot = self.to_spot (time) (brown)
    return spot, brown        
'''
