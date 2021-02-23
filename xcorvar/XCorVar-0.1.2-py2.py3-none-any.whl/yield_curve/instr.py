# coding: utf-8

import math as mth
import json as js
import numpy as np

from toolbox.mathbox import find_idx
from toolbox.rootfinder import dichotomy

class Instr:

    #public:

        def __init__ (self, mat, val):
            self.mat = mat
            self.val = val

        def get_val (self, disc):            
            raise NotImplementedError

        def get_impl_disc (self):
            raise NotImplementedError

class Deposit (Instr):

    #public:

        def __init__ (self, mat, val):
            super ().__init__ (mat, val)

        def get_val (self, disc):
            return (1 / disc (self.mat) - 1) / self.mat

        def get_impl_disc (self, disc):
            return 1 / (1 + self.mat * self.val)

class Swap (Instr):

    #public:

        def __init__ (self, mat, period, val):
            super ().__init__ (mat, val)
            self.period = period
            self.dates = np.arange (period, mat, period)

        def get_val (self, disc):
            return (1 - disc (self.mat)) / (self.period * sum ([disc (date) for date in self.dates]))

        def get_impl_disc (self, disc):
            return (1 - self.period * self.val * sum ([disc (date) for date in self.dates [:-1]])) / (1 + self.period * self.val)

class Disc (Instr):

    #public:

        def __init__ (self, fwd):
            self.fwd = fwd
            
        def __call__ (self, mat):
            return mth.exp (-self.fwd.integral (mat))

class Fwd:

    #public:

        def __init__ (self):
            self.pts = [Point (0, 1)]

        def integral (self, mat):
            return DiscInt (self.pts) ()

        def get_pt (self, mat, integral):
            param = (integral - sum ([self.pts [idx].y * (self.pts [idx].x - self.pts [idx-1].x) for idx in range ()]) / (mat - )
            return Point (mat, params)
            
        def __call__ (self, mat):
            lft, _ = find_idx (self.dates, mat)
            return self.params [lft]

class YieldCurve:

    #public:

        def __init__ (self):
            self.data = js.load (open (file='instr.json', mode='r'))
            self.disc = Disc (Fwd ())

        def build_instr (self, kind, params):
            return Deposit (**params) if kind is 'deposit' else Swap (**params) if kind is 'swap' else Instr (**params)

        def calibrate (self):
            for line in self.data:
                instr = build_instr (*line.values ())
                impl_disc = instr.get_impl_disc (self.disc)
                impl_int = -mth.log (impl_disc)
                
                self.disc.fwd.params.append (param)
                self.disc.fwd.dates.append (date)