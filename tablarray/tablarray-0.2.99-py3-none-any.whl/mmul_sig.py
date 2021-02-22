#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 17:33:57 2020

@author: chris
"""

import numpy as np

from . import ta


def mmul_ta_signature(arg):
    """Given a TablArray or np.ndarray, return a TablArray"""
    if hasattr(arg, 'ts') and hasattr(arg, 'base'):
        # arg is TablArray type
        array = arg
    # elif (type(arg) is tuple and len(arg) == 2
    #          and isinstance(arg[0], np.ndarray)):
    #        # arg is (array, cdim)
    #        cdim = arg[1]
    #        array = arg[0]
    elif isinstance(arg, np.ndarray):
        # assume either cdim = 2 or ndim
        cdim = max(2, arg.ndim)
        array = ta.TablArraylib.TablArray(arg, cdim)
    elif np.isscalar(arg):
        array = ta.TablArray(np.array(arg), 0)
    else:
        raise ValueError
    return array
