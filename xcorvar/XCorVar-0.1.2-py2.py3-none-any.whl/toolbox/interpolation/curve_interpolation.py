# coding: utf-8

import math as mth
import numpy as np
import scipy as sp

from matplotlib import pyplot as plt

from sample.toolbox.interpolation.interpolation import Interpolation
from sample.toolbox.random_variable import DEFAULT_RANDOM_NUMBER_GENERATOR

class Point:

    #public:

        def __init__ (self, x, y, fst_der=None, snd_der=None, thd_der=None):
            self.x = x
            self.y = y
            self.fst_der = fst_der
            self.snd_der = snd_der
            self.thd_der = thd_der

        def get_attr (self):
            return self.x, self.y

#toolkit:

def brown_mid_interpoler (pt_lft, pt_rgt, noise):
    return Point (0.5 * (pt_lft.x + pt_rgt.x), 0.5 * (pt_lft.y + pt_rgt.y) + mth.sqrt (0.25 * (pt_rgt.x - pt_lft.x)) * noise)  

class CurveInter (Interpolation):

    #public:

        def plt (self, lft, rgt, size):
            plt.figure ()
            X = np.linspace (lft, rgt, size)
            Y = [self.interpoler (x) for x in X]
            plt.plot (X, Y, linestyle='--', color='black')
            for pt in self.grid: plt.scatter (*pt.get_attr (), marker='+', color='blue')
            plt.show ()

        def interpoler (self, x):
            raise NotImplementedError

class FlatInter (CurveInter):

    #public:

        def __init__ (self, grid):
            super ().__init__ (grid)

        def interpoler (self, x):
            return self.find_obj (x).y

class LinearInterpolation (CurveInter):

    #public:

        def __init__ (self, grid):
            super ().__init__ (grid)
            self.get_slopes ()

        def get_slopes (self):
            it0 = iter (self.grid); it1 = iter (self.grid)
            next (it1)
            while True:
                try:
                    pt0 = next (it0); pt1 = next (it1)     
                    pt0.fst_der = (pt1.y - pt0.y) / (pt1.x - pt0.x)
                except StopIteration: 
                    break

        def interpoler (self, x):
            pt = self.find_obj (x)
            return pt.y + pt.fst_der * (x - pt.x)

class CubicSplineInterpolation (CurveInter):

    #public:

        def __init__ (self, grid):
            super ().__init__ (grid)
            self.get_der ()

        def interpoler (self, x, extrapolation_kind='linear'):
            if self.fst.x > x:
                if extrapolation_kind is 'linear': return self.fst.y + self.fst.fst_der * (x - self.fst.x)
                elif extrapolation_kind is 'flat': return self.fst.y
                else: raise ValueError ('Cannot find extrapolation kind')
            elif self.lst.x < x:
                if extrapolation_kind is 'linear': return self.lst.y + self.lst.fst_der * (x - self.lst.x)
                elif extrapolation_kind is 'flat': return self.lst.y
                else: raise ValueError ('Cannot find extrapolation kind')
            else:
                pt = self.find_obj (x)
                shift = x - pt.x
                sq_shift = shift * shift
                cb_shift = sq_shift * shift
                return pt.y + pt.fst_der * shift + pt.snd_der * sq_shift + pt.thd_der * cb_shift

    #private

        def get_der (self):
            self.slopes = self.get_slopes ()
            its0 = iter (self.slopes); its1 = iter (self.slopes); next (its1)
            itg0 = iter (self.grid); itg1 = iter (self.grid); next (itg1)
            while True:
                try:
                    pt0 = next (itg0); pt1 = next (itg1)
                    slope0 = next (its0); slope1 = next (its1)
                    pt0.fst_der = slope0
                    pt0.snd_der = 3 * (pt1.y - pt0.y) / (pt1.x - pt0.x) ** 2 - (2 * slope0 + slope1) / (pt1.x - pt0.x)
                    pt0.thd_der = (slope1 + slope0) / (pt1.x - pt0.x) ** 2 - 2 * (pt1.y - pt0.y) / (pt1.x - pt0.x) ** 3
                except StopIteration: 
                    pt0.fst_der = slope0
                    break

        def get_slopes (self):
            fst_slope = self.left_boundary_slope ()
            lst_slope = self.right_boundary_slope ()
            slopes = list (np.linalg.solve (*self.build (fst_slope, lst_slope)))
            slopes.insert (0, fst_slope)
            slopes.insert (self.size, lst_slope)
            return slopes

        def build (self, fst_slope, lst_slope):
            left_diag = []; mid_diag = []; right_diag = []
            vec = []
            it_left = iter (self.grid); it_mid = iter (self.grid); it_right = iter (self.grid)
            next (it_mid); next (it_right); next (it_right)
            while True:
                try:
                    right = next (it_right); left = next (it_left); mid = next (it_mid)
                    assert (vec != [])
                    l = 1 / (mid.x - left.x)
                    m = 2 * (1 / (mid.x - left.x) + 1 / (right.x - mid.x))
                    r = 1 / (right.x - mid.x)
                    rhs = 3 * (right.y - mid.y) / (right.x - mid.x) ** 2 + 3 * (mid.y - left.y) / (mid.x - left.x) ** 2
                    left_diag.append (l); mid_diag.append (m); right_diag.append (r); vec.append (rhs)
                except AssertionError:
                    m = 2 * (1 / (mid.x - left.x) + 1 / (right.x - mid.x))
                    r = 1 / (right.x - mid.x)
                    rhs = 3 * (right.y - mid.y) / (right.x - mid.x) ** 2 + 3 * (mid.y - left.y) / (mid.x - left.x) ** 2 - fst_slope / (mid.x - left.x)
                    right_diag.append (r); mid_diag.append (m); vec.append (rhs)
                except StopIteration:
                    l = 1 / (mid.x - left.x)
                    m = 2 * (1 / (mid.x - left.x) + 1 / (right.x - mid.x))
                    rhs = 3 * (right.y - mid.y) / (right.x - mid.x) ** 2 + 3 * (mid.y - left.y) / (mid.x - left.x) ** 2 - lst_slope / (mid.x - left.x)
                    left_diag.append (l); mid_diag.append (m); vec.append (rhs)
                    break
            mat = sp.sparse.diags ([left_diag, mid_diag, right_diag], [-1, 0, 1]).toarray ()
            return mat, vec
                        
        def left_boundary_slope (self):
            fst_pt = self.grid [0]
            snd_pt = self.grid [1]
            return (snd_pt.y - fst_pt.y) / (snd_pt.x - fst_pt.x)

        def right_boundary_slope (self):
            fst_pt = self.grid [self.size-2]
            snd_pt = self.grid [self.size-1]
            return (snd_pt.y - fst_pt.y) / (snd_pt.x - fst_pt.x)