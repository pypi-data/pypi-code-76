#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 11:26:17 2020

@author: chr
"""

import numpy as np

from .mmul_sig import mmul_ta_signature


def _matmul_MV(a, b):
    """matrix-vector multiplication a, b supporting tabular super-structure
    and/or broadcasting

    Parameters
    ----------
    a : array 2 dim or higher
        Where higher dim implies it is an array of 2 dim matrices. Matrix
        multiplication is always aligned to the last 2 dim.
    b : array 1 dim or higher
        Where higher dim implies it is an array of 1 dim vectors. Matrix
        multiplication is always aligned to the last 1 dim.
    """
    # matmul 2d matrix by vector
    subscripts = '...ij,...j->...i'
    # do einsum of a,b using the subscripts
    return np.einsum(subscripts, a, b)


def _matmul_MM(a, b):
    """matrix-matrix multiplication a, b supporting tabular super-structure
    and/or broadcasting

    Parameters
    ----------
    a : array 2 dim or higher
        Where higher dim implies it is an array of 2 dim matrices. Matrix
        multiplication is always aligned to the last 2 dim.
    b : array 2 dim or higher
        Where higher dim implies it is an array of 2 dim vectors. Matrix
        multiplication is always aligned to the last 2 dim.
    """
    # matmul 2d matrix by 2d matrix
    subscripts = '...ij,...jk->...ik'
    # do einsum of a,b using the subscripts
    return np.einsum(subscripts, a, b)


def matmul(a, b):
    """Fast Matrix Multiplication with ATC compatibility.

    Signatures::

        c = atc_matmul(a: ATC, b: ATC)
        c = atc_matmul(a: ndarray, b: ndarray)
        c = atc_matmul(a: ndarray, b: ATC)
    """
    a = mmul_ta_signature(a)
    b = mmul_ta_signature(b)
    rclass = a.__class__
    # setup the subscripts to achieve matmul
    if a.ts.cdim == 2 and b.ts.cdim == 1:
        # matmul 2d matrix by vector
        rarray = _matmul_MV(a.base, b.base)
        return rclass(rarray, 1, a.view)
    elif a.ts.cdim == 2 and b.ts.cdim == 2:
        # matmul 2d matrix by 2d matrix
        rarray = _matmul_MM(a.base, b.base)
        return rclass(rarray, 2, a.view)
    else:
        raise ValueError
