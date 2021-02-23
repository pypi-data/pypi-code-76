# coding: utf-8

import numpy as np
import math as mth
import copy as cpy

from matplotlib import pyplot as plt

from sample.toolbox.random_variable import StandardMultiNormal, StandardNormalMarsaglia
from sample.toolbox.integral.discrete_integral import DiscInt
from sample.toolbox.interpolation.curve_interpolation import Point

#box:

def area (path, step, frame, dim=None):
    if dim is None: curve = [Point (*state.get_attr ()) for state in path if test (state.time, frame)]
    else: curve = [Point (state.time, state.space [dim]) for state in path if test (state.time, frame)]
    return DiscInt (curve, step) ()

def mean (path, step, frame, dim=None):
    return area (path, step, frame, dim) / length (frame)

def test (time, frame):
    mat0, mat1 = frame
    return time >= mat0 and time <= mat1

def length (frame):
    mat0, mat1 = frame
    return mat1 - mat0

#core:

class Diffusion:

    #public:

        def __init__ (self, scheme):
            self.stage = 0
            self.init = cpy.copy (scheme.state)
            self.scheme = scheme
            self.path = [cpy.copy (self.scheme.state)]
            self.anti_path = [cpy.copy (self.scheme.state)]
            try: self.noise = StandardMultiNormal (len (scheme.state.space))
            except TypeError: self.noise = StandardNormalMarsaglia ()

        def restart (self):
            self.stage = 0
            self.scheme.state = cpy.copy (self.init)
            self.path = [cpy.copy (self.scheme.state)]
            return self

        def not_end (self, stage_max):
            return self.stage < stage_max

        def n_stage (self, mat):
            return int (mat / self.scheme.step.time)

        def next (self, noise):
            self.scheme.next (noise)
            self.stage += 1
            self.path.append (cpy.copy (self.scheme.state))
            return self

        def run (self, mat):
            stage_max = self.n_stage (mat)
            while self.not_end (stage_max): self.next (self.noise ())
            return self

        def map (self, func):
            self.path = list (map (func, self.path))

        def show (self):
            if self.path == []: print ('No path')
            for state in self.path: print (state)

        def plt_dim (self, dim):
            plt.figure ()
            times = [state.time for state in self.path]
            spaces = [state.space [dim] for state in self.path]
            plt.plot (times, spaces)
            plt.show ()

        def plt (self):
            plt.figure ()
            plt.plot ([state.time for state in self.path], [state.space for state in self.path])
            plt.show ()

