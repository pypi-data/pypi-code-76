# coding: utf-8

import numpy as np
import copy as cpy
import math as mth

from toolbox.interpolation.curve_interpolation import Point, CubicSplineInterpolation
from toolbox.interpolation.surface_interpolation import Slice
from toolbox.integral.functionnal_integral import FuncInt
from toolbox.mathbox import INV_SQRT_TWICE_PI
from matplotlib import pyplot as plt

class Params:

    #public:

        def __init__ (self, min, max, nb):
            self.min = min
            self.max = max
            self.nb = nb

        @property
        def step (self):
            return (self.max - self.min) / self.nb

        def __call__ (self, rev=False):
            rg = list (np.linspace (self.min, self.max, self.nb))
            if rev: rg.reverse ()
            return rg

class AmOptBlackScholesPricing:

    #public:

        def __init__ (self, am_opt, mdl_params, x_params, y_params):
            self.am_opt = am_opt
            self.spots = x_params (rev=False)
            self.dates = y_params (rev=True)
            self.cond_dens = black_scholes_trans (mdl_params.vol, mdl_params.mu, y_params.step)
            
        def start (self, mat):
            self.curr_curve = Slice (mat, [Point (spot, self.am_opt.payoff.func (mat, spot)) for spot in self.spots])
            self.grid = [cpy.copy (self.curr_curve)]

        def next (self, mat):
            val = CubicSplineInterpolation (self.curr_curve.curve)
            spots = np.array ([pt.x for pt in self.curr_curve.curve])
            payoff = np.array ([self.am_opt.payoff.func (mat, spot) for spot in spots])
            cond_exp = FuncInt (lambda y: self.cond_dens (spots, y) * val.interpoler (y), self.spots [0], self.spots [-1]).run ().curr.val
            values = np.maximum (payoff, cond_exp)
            self.curr_curve = Slice (mat, [Point (spot, val) for spot, val in zip (spots, values)])

        def run (self):
            for mat in self.dates:
                self.curr_mat = mat
                if mat == self.am_opt.mat: self.start (mat)
                else: self.next (mat)
                self.grid.append (cpy.copy (self.curr_curve))
            return self

        def plt (self):
            for sl in self.grid:
                plt.figure ()
                for pt in sl.curve:
                    plt.scatter (pt.x, pt.y, color='black', marker='x')
                plt.show ()

#mathkit:

def black_scholes_trans (vol, mu, dt):
    vol_sqrt_dt = vol * mth.sqrt (dt)
    return lambda x, y: INV_SQRT_TWICE_PI * np.exp (-0.5 * ((np.log (y / x) - mu * dt) / vol_sqrt_dt) ** 2) / (y * vol_sqrt_dt)






        

        