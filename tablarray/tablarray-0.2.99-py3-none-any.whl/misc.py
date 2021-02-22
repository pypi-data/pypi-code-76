#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities that tend to get used front and back (IO) of tablarray functions

Created on Sun Jan  3 15:34:31 2021

@author: chris
"""


def istablarray(a):
    """returns True/False if argument appears to fulfill TablArray class"""
    return (hasattr(a, 'ts') and hasattr(a, 'view')
            and hasattr(a, 'base') and hasattr(a, 'bcast'))


def istablaset(a):
    """returns True/False if argument appears to fulfill TablaSet class"""
    return (hasattr(a, '_tablarrays') and hasattr(a, '_ts')
            and hasattr(a, 'keys') and hasattr(a, 'bcast'))


def base(a):
    """returns .base if argument is tablarray else pass-through a"""
    return a.base if istablarray(a) else a


def _rval_once_a_ta(rclass, rval, cdim, view):
    """"""
    if rval.ndim == cdim:
        return rval
    return rclass(rval, cdim, view)


def _rval_always_ta(rclass, rval, cdim, view):
    return rclass(rval, cdim, view)
