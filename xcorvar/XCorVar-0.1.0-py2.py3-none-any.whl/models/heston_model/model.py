# coding: utf-8

import numpy as np
import math as mth

from toolbox.diffusion import ONE_DAY
from toolbox.diffusion import State, SuperState, Step, StoDifEq, MultiEulerScheme, Diffusion 

class HestonMdl:

    #public:

        def __init__ (self, params):
            self.params = params

        def drift (self, time, space):
            spot, var = space 
            return np.array ([self.params.rate * spot, self.params.var.kappa * (self.params.var.theta - var)])

        def vol (self, time, space):
            spot, var = space
            vol = mth.sqrt (abs (var))
            return np.array ([[vol * spot, 0], [0, self.params.var.eta * vol]])

        @property
        def state (self):
            return State (0, np.array ([self.params.spot, self.params.var.v0]))

        @property
        def super_state (self):
            return SuperState (0, np.array ([self.params.spot, self.params.var.v0]))

        @property
        def corr (self):
            return np.array ([[1, self.params.rho], [self.params.rho, 1]])

        @property
        def sto_dif_eq (self):
            return StoDifEq (self.drift, self.vol, self.corr)

        def diffusion (self, scheme=MultiEulerScheme, step=ONE_DAY):
            return Diffusion (scheme (self.state, self.sto_dif_eq, Step (step)))

        def super_diffusion (self, scheme=MultiEulerScheme, step=ONE_DAY):
            return Diffusion (scheme (self.super_state, self.sto_dif_eq, Step (step)))

        def spot (self, time=0, diffusion=None, verbose=0):
            if diffusion is None: diffusion = self.diffusion ()
            return diffusion.restart ().run (time, verbose).scheme.state.space

        def mean (self, frame=[0,1], diffusion=None, verbose=0):
            _, mat1 = frame
            if diffusion is None: diffusion = self.diffusion ()
            return diffusion.restart ().run (mat1, verbose).mean (frame, 0)

        def trj_spot (self, mat, scheme=MultiEulerScheme, step=ONE_DAY, verbose=0):
            self.diffusion (scheme, step).run (mat, verbose).plt_dim (0)

        def trj_var (self, mat, scheme=MultiEulerScheme, step=ONE_DAY, verbose=0):
            self.diffusion (scheme, step).run (mat, verbose).plt_dim (1)