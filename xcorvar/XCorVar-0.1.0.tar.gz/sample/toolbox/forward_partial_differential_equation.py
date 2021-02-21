'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import math as mth
import numpy as np
import copy as cpy

from scipy.sparse import diags

from matplotlib import pyplot as plt

class State:

    #public

        def __init__ (self, t, x, y):
            self.t = t
            self.x = x
            self.y = y

        def get_attribute (self):
            return self.t, self.x, self.y

        def next_time (self, dt):
            self.t += dt

        def next_values (self, mat, rhs):
            self.y = np.linalg.solve (mat, rhs)

class ForwardPartialDifferentialEquationCore:

    #public:

        def __init__ (self, coeff, payoff, lft, rgt, dt, dx, bds):
            self.dt = dt
            self.sc = get_sc (dt, dx)
            self.lft = lft
            self.rgt = rgt
            self.coeff = coeff
            self.payoff = payoff
            self.spaces = np.arange (*bds, dx)
            self.state = State (0, self.spaces, np.vectorize (payoff) (self.spaces))
            self.hist = [cpy.copy (self.state)]

        @property
        def current (self):
            return self.state

        def next_time (self):
            self.state.next_time (self.dt)

        def next_values (self):
            self.state.next_values (**self.system ())

        def make_matrix (self, a, b, c):
            dt, half_dt_inv_dx, dt_inv_sq_dx, minus_twice_dt_inv_sq_dx = self.sc
            lft = dt_inv_sq_dx * c - half_dt_inv_dx * b
            mid = 1 + dt * a + minus_twice_dt_inv_sq_dx * c
            rgt = dt_inv_sq_dx * c + half_dt_inv_dx * b
            return lft, mid, rgt

        def make_rhs (self, lft, rgt):
            time, _, val = self.state.get_attribute ()
            rhs = val.copy ()
            rhs [0] -= lft [0] * self.lft (time)
            rhs [-1] -= rgt [-1] * self.rgt (time)
            return rhs

        def make_system (self, a, b, c):
            lft, mid, rgt = self.make_matrix (a, b, c)
            rhs = self.make_rhs (lft, rgt)
            return {'mat' : tridiag (lft [1:], mid, rgt [:-1]), 'rhs' : rhs}

        def system (self):
            coeff = [self.coeff (self.state.t, space) for space in self.spaces]
            a = np.array ([val_a for val_a, _, _ in coeff])
            b = np.array ([val_b for _, val_b, _ in coeff])
            c = np.array ([val_c for _, _, val_c in coeff])
            return self.make_system (a, b, c)

        def next (self):
            self.next_time ()
            self.next_values ()

        def not_end (self, mat_max):
            return self.state.t < mat_max
            
        def run (self, mat_max):
            while self.not_end (mat_max): 
                self.next ()
                self.hist.append (cpy.copy (self.state))
            return self

        def plot_slice (self):
            for state in self.hist:
                plt.figure ()
                plt.plot (state.x, state.y)
                plt.show ()
            
#toolkit:

def get_sc (dt, dx):
    dt_inv_dx = dt / dx
    half_dt_inv_dx = 0.5 * dt_inv_dx
    dt_inv_sq_dx = dt_inv_dx / dx
    minus_twice_dt_inv_sq_dx = -2 * dt_inv_sq_dx
    return dt, half_dt_inv_dx, dt_inv_sq_dx, minus_twice_dt_inv_sq_dx

def tridiag (lft, mid, rgt):
    return diags ([lft, mid, rgt], [-1, 0, 1]).toarray ()

class ForwardPartialDifferentialEquation (ForwardPartialDifferentialEquationCore):

    #public:

        def __init__ (self, loc_vol, dt, dx, bds, eps=0):
            l, r = bds
            payoff = lambda log_fwd_mnn: (1 + eps) * max (1 - mth.exp (log_fwd_mnn), 0)
            lft_val = payoff (l)
            rgt_val = payoff (r)
            lft = lambda _: lft_val
            rgt = lambda _: rgt_val
            super ().__init__ (coeff (loc_vol, eps), payoff, lft, rgt, dt, dx, bds)
            self.loc_vol = loc_vol

        def get_prices (self):
            _, log_fwd_mnns, prices = self.state.get_attribute ()
            return log_fwd_mnns, prices

#toolkit:

def coeff (loc_vol, eps=0):
    return lambda time, log_fwd_mnn: coeff_core (0.5 * loc_vol (time, log_fwd_mnn + eps) ** 2)

def coeff_core (half_sq_loc_vol):
    return 0, half_sq_loc_vol, -half_sq_loc_vol
