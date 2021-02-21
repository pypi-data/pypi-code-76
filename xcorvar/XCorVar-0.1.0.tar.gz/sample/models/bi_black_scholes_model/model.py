# coding: utf-8

import numpy as np
import math as mth

from toolbox.random_variable import StandardNormalMarsaglia

class BiBlackScholesMdl:

    #public:

        def __init__ (self, params):
            self.params = params
            self.noise1 = StandardNormalMarsaglia ()
            self.noise2 = StandardNormalMarsaglia ()

        def to_spot1 (self, time):
            return lambda brown: self.params.func1 (time, brown)

        def to_spot2 (self, time):
            return lambda brown: self.params.func2 (time, brown)

        def to_spot_like (self, time):
            return lambda brown: self.params.func_like (time, brown)

        def noises (self):
            noise1 = self.noise1 ()
            noise2 = self.noise2 ()
            return np.array ([self.params.rho * noise2 + self.params.bar_rho * noise1, noise2])

        def brown (self, time):
            return self.noise1 () * mth.sqrt (time)

        def browns (self, time=0):
            return mth.sqrt (time) * self.noises ()

        def spots (self, time=0):
            brown1, brown2 = self.browns (time)
            return self.to_spot1 (time) (brown1), self.to_spot2 (time) (brown2)
