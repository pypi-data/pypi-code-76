# coding: utf-8

import copy as cpy
import numpy as np

from toolbox.interpolation.surface_interpolation import Slice
from toolbox.interpolation.curve_interpolation import Point, CubicSplineInterpolation
from toolbox.diffusion import State, Step, StoDifEq, EulerScheme
from toolbox.monte_carlo import MonteCarlo
from toolbox.random_variable import StandardNormalMarsaglia
from toolbox.compose import comp
from matplotlib import pyplot as plt

class AmOptEulerSchemePricing:

    #public:

        def __init__ (self, am_opt, sto_dif_eq, x_params, y_params):
            self.am_opt = am_opt
            self.noise = StandardNormalMarsaglia ()
            self.step = Step (y_params.step)
            self.sto_dif_eq = sto_dif_eq
            self.spots = x_params (rev=False)
            self.dates = y_params (rev=True)
        
        def start (self, mat):
            self.curr_curve = Slice (mat, [Point (spot, self.am_opt.payoff.func (mat, spot)) for spot in self.spots])
            self.grid = [cpy.copy (self.curr_curve)]

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

    #private:

        def next (self, mat):
            val = CubicSplineInterpolation (self.curr_curve.curve)
            spots = np.array ([pt.x for pt in self.curr_curve.curve])
            payoff = np.array ([self.am_opt.payoff.func (mat, spot) for spot in spots])
            cond_exp = [MonteCarlo (comp (val.interpoler, EulerScheme (State (self.curr_mat, spot), self.sto_dif_eq, self.step).next, self.noise)).add_until (0.1).current.mean for spot in spots]
            values = np.maximum (payoff, cond_exp)
            self.curr_curve = Slice (mat, [Point (spot, val) for spot, val in zip (spots, values)])