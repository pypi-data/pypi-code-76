'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/local/bin/python3.7
# coding: utf-8

import numpy as np

from matplotlib import pyplot as plt

from toolbox.interpolation.interpolation import Interpolation
from toolbox.mathbox import lin_inter_core
from toolbox.interpolation.curve_interpolation import Point, CubicSplineInterpolation

#box:

def to_grid (data):
    return [Slice (x, [Point (y0, y1) for y0, y1 in zip (*y)]) for x, y in data.items ()]

#core:

class Slice:

    #public:

        def __init__ (self, x, curve):
            self.x = x
            self.curve = curve

        def get_inter_slice (self, CurveInterKind):
            return self.x, CurveInterKind (self.curve)

class SurfInter (Interpolation):

    #public:

        def __init__ (self, surf):
            super ().__init__ (surf)

        def interpoler (self, x, y):
            raise NotImplementedError

        def plt (self, x_lft, x_rgt, x_size, y_lft, y_rgt, y_size):
            x_pts = np.linspace (x_lft, x_rgt, x_size)
            y_pts = np.linspace (y_lft, y_rgt, y_size)
            grid = [[self.interpoler (x, y) for y in y_pts] for x in x_pts]
            fig = plt.figure ()
            axes = plt.axes (projection='3d')
            axes.set_title ('Surface')
            axes.set_xlabel ('X')
            axes.set_ylabel ('Y')
            axes.set_zlabel ('Z')
            surf = axes.plot_surface (*np.meshgrid (x_pts, y_pts), np.array (grid))
            fig.colorbar (surf, shrink=0.5, aspect=10)
            plt.show ()

class StdInter (SurfInter):

    #public:

        def __init__ (self, surf, CurveInterKind=CubicSplineInterpolation):
            super ().__init__ (surf)
            self.slices = [sl.get_inter_slice (CurveInterKind) for sl in surf]

        def interpoler (self, x, y):
            lft, rgt = self.find_idx (x)
            sl1 = self.slices [lft]
            sl2 = self.slices [rgt]
            x1, curve1 = sl1
            x2, curve2 = sl2
            y1 = curve1.interpoler (y)
            y2 = curve2.interpoler (y)
            return lin_inter_core (x, x1, y1, x2, y2)





