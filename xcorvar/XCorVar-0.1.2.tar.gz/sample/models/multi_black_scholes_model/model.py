# coding: utf-8

import numpy as np
import math as mth

from toolbox.random_variable import MultiNormal

class MultiBlackScholesMdl:

    #public:

        def __init__ (self, params):
            self.params = params
            self.noise = MultiNormal (params.dim, np.zeros (params.dim), params.corr)

        def to_spot (self, time):
            return lambda brown: self.params.func (time, brown)

        def brown (self, time=0):
            return mth.sqrt (time) * self.noise ()

        def spot (self, time=0):
            return self.to_spot (time) (self.brown (time))