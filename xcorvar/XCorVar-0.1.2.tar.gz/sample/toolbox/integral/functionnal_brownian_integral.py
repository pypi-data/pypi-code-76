# coding: utf-8

import numpy as np
import math as mth

from sample.toolbox.integral.integral import Int
from sample.toolbox.interpolation.curve_interpolation import Point, brown_mid_interpoler

class RandomIntegral (Int):

    #public:

        def __init__ (self, func, lft, rgt, noise):
            self.noise = noise
            brown_lft = self.noise () * mth.sqrt (lft)
            brown_rgt = brown_lft + self.noise () * mth.sqrt (rgt - lft)
            val_lft = func (lft, brown_lft)
            val_rgt = func (rgt, brown_rgt)
            step = rgt - lft
            super ().__init__ (func, step, [Point (lft, brown_lft), Point (rgt, brown_rgt)], 0.5 * step * (val_lft + val_rgt))

    #private:

        def refine (self):
            lft_idx = 0
            rgt_idx = 1 
            times = []
            browns = []
            while True:
                try:
                    brown_lft = self.curr.pts [lft_idx]
                    brown_rgt = self.curr.pts [rgt_idx]
                    brown_mid = brown_mid_interpoler (brown_lft, brown_rgt, self.noise ())
                    self.curr.pts.insert (rgt_idx, brown_mid)
                    times.append (brown_mid.x)
                    browns.append (brown_mid.y)
                    lft_idx += 2; rgt_idx += 2
                except IndexError: break
            return np.sum (self.func (np.array (times), np.array (browns)))

#mathbox:

#def get_mean_brown (mat, pts, noise):
#    incr = get_incr (pts)
#    nb = len (incr)
#    wghts = [(2 * (nb - idx) - 1) / (2 * nb) for idx in range (nb)]
#    mean = np.dot (wghts, incr)
#    var = mat / (12 * nb ** 2)
#    std = mth.sqrt (var)
#    mean_brown = mean + std * noise
#    return mean_brown

