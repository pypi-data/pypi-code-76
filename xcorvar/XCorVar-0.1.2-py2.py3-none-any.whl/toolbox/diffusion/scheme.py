# coding: utf-8

import copy as cpy
import numpy as np
import math as mth

from sample.toolbox.diffusion.utilities import Step, State, SuperState, StoDifEq 

class Scheme:

    #public:

        def __init__ (self, init, sto_dif_eq, step):
            self.state = cpy.copy (init)
            self.sto_dif_eq = sto_dif_eq
            self.step = step

        @property
        def curr (self):
            return self.state

        def next_time (self):
            self.state.time += self.step.time

        def next_space (self, noise):
            self.state.space = self.get_next_space (self.state.time, self.state.space, noise)
            if isinstance (self.state, SuperState): self.state.bar_space = self.get_next_space (self.state.time, self.state.bar_space, -noise)

        def next (self, noise):
            self.next_space (noise)
            self.next_time ()

        def get_coeff (self, time, space):
            raise NotImplementedError

        def get_next_space (self, time, space, noise):
            raise NotImplementedError

class EulerScheme (Scheme):

    #public:

        def __init__  (self, init, sto_dif_eq, step):
            super ().__init__ (init, sto_dif_eq, step)

        def get_coeff (self, time, space):
            return self.sto_dif_eq.coeff (time, space)

        def get_next_space (self, time, space, noise=None):
            drift, vol = self.get_coeff (time, space)
            return space + self.step.time * drift + self.step.brown * vol * noise

class MultiEulerScheme (Scheme):

    #public:

        def __init__  (self, init, multi_sto_dif_eq, step):
            super ().__init__ (init, multi_sto_dif_eq, step)
            if hasattr (multi_sto_dif_eq, 'corr'): self.sqr_corr = np.linalg.cholesky (multi_sto_dif_eq.corr)

        def get_coeff (self, time, space):
            return self.sto_dif_eq.coeff (time, space)

        def get_next_space (self, time, space, noise=None):
            drift, vol = self.get_coeff (time, space)
            normal = self.sqr_corr @ noise if hasattr (self, 'sqr_corr') else noise
            return space + self.step.time * drift + self.step.brown * vol @ normal

class MultiCorrDepEulerScheme (Scheme):

    #public:

        def __init__  (self, init, multi_corr_dep_sto_dif_eq, step):
            super ().__init__ (init, multi_corr_dep_sto_dif_eq, step)

        def get_coeff (self, time, space):
            return self.sto_dif_eq.coeff (time, space)

        def get_next_space (self, time, space, noise=None):
            drift, vol, corr = self.get_coeff (time, space)
            sqr_corr = np.linalg.cholesky (corr)
            return space + self.step.time * drift + self.step.brown * vol @ sqr_corr @ noise

class BlackScholesScheme (Scheme):
    
    #public:

        def __init__  (self, spot, vol, mu, step):
            step = Step (step)
            init = State (0, spot)
            sto_diff_eq = StoDifEq (lambda time, space: (mu, vol))
            super ().__init__ (init, sto_diff_eq, step)

        def get_coeff (self, time, space):
            return self.sto_dif_eq.coeff (time, space)

        def get_next_space (self, time, space, noise=None):
            drift, vol = self.get_coeff (time, space)
            return space * mth.exp (drift * self.step.time + vol * self.step.brown * noise)

class LocalVolatilityScheme (EulerScheme):

    #public:

        def __init__ (self, loc_vol, step):
            init = State (0, 0)
            step = Step (step)
            def get_coeff (time, space):
                sig = loc_vol (time, space)
                return (-0.5 * sig * sig, sig)
            sto_diff_eq = StoDifEq (get_coeff)
            super ().__init__ (init, sto_diff_eq, step)
        