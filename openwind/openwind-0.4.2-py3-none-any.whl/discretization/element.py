#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"
"""One individual element of a finite elements Mesh."""

from openwind.discretization import GLQuad
import numpy as np


__quads = dict()
def _get_quad(order):
    """Memorized version of GLQuad, to not recompute each time.

    Maybe useless, or maybe move it to GLQuad itself ?
    """
    if order not in __quads:
        __quads[order] = GLQuad(order)
    return __quads[order]


class Element:

    def __init__(self, x0, x1, order):
        self._x_start = x0
        self._length = x1 - x0
        self.order = int(order)

    def get_length(self):
        return self._length

    def get_nodes(self):
        return self._x_start + _get_quad(self.order).pts*self._length

    def get_weights(self):
        return self._length * _get_quad(self.order).weight

    def get_Bh_coeff(self):
        return _get_quad(self.order).BK

    def get_lagrange(self, x):
        assert all(x >= 0) and all(x <= 1)
        if x.size > 0:
            lagrange = _get_quad(self.order).lagranPolys()
            return np.vstack([lag(x) for lag in lagrange]).T
        else:
            return np.zeros((0, self.order + 1))

    def get_diff_lagrange(self, x):
        assert all(x >= 0) and all(x <= 1)
        if x.size > 0:
            lagrange = _get_quad(self.order).lagran_polys_derivate()
            return np.vstack([lag(x)/self._length for lag in lagrange]).T
        else:
            return np.zeros((0, self.order + 1))
