'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import math as mth
import functools as ft
import datetime as dt
import os as os
import json as js

import scipy.stats as sps

from sample.constants import Constants

#csts:

INV_PI = 1 / mth.pi
INV_SQRT_TWICE_PI = 1 / mth.sqrt (2 * mth.pi)

#add list
def add_list (lst):
    if len (lst) == 1: return lst [0]
    else: return lst [0] + add_list (lst [1:])

#cleaner

def cleaner (lst):
    return [x for x in lst if x is not None]

#merge_sort

def merge (lst, lsti, begin1, end1, end):
    begin2 = end1 + 1
    end2 = end + 1
    cpt1 = begin1
    cpt2 = begin2
    lfti = lsti [begin1:begin2].copy ()
    for idx in range (begin1, end2):
        if cpt1 == begin2: 
            break
        elif cpt2 > end:
            lsti [idx] = lfti [cpt1-begin1]
            cpt1 += 1
        elif lst [lfti [cpt1-begin1]] < lst [lsti [cpt2]]:
            lsti [idx] = lfti [cpt1-begin1]
            cpt1 += 1
        else:
            lsti [idx] = lsti [cpt2] 
            cpt2 += 1

def merge_sort_core (lst, lsti, begin, end):
    if begin < end:
        mid = mth.floor (0.5 * (begin + end))
        merge_sort_core (lst, lsti, begin, mid)
        merge_sort_core (lst, lsti, mid+1, end)
        merge (lst, lsti, begin, mid, end)

def merge_sort (lst):
    lsti = [idx for idx, _ in enumerate (lst)]
    merge_sort_core (lst, lsti, 0, len (lsti) - 1)
    return lsti

#find_idx

def find_idx_core (lst, lsti, x, begin, end):
    if end - begin == 1: return lsti [begin], lsti [end]
    mid = mth.floor (0.5 * (begin + end))
    if lst [lsti [mid]] < x: begin = mid 
    else: end = mid
    return find_idx_core (lst, lsti, x, begin, end)

def find_index (lst, x=0):
    lsti = merge_sort (lst)
    return find_idx_core (lst, lsti, x, 0, len (lst)-1)

#prod 

def prod (l):
    return ft.reduce (lambda x, y: x * y, l, 1)

#interp:

def lin_inter_core (x, x0, y0, x1, y1):
    slope = (y1 - y0) / (x1 - x0)
    return y0 + slope * (x - x0)

def reg_inter_core (x, coeff):
    return reg_inter_func (x, *coeff.values ())

def get_reg_coeff (x, y):
    slope, intercept, _, _, _ = sps.linregress (x, y)
    return {'slope' : slope, 'intercept' : intercept}

def reg_inter_func (x, slope, intercept):
    return intercept + slope * x

#date:

def get_time_to_expiry (start, end, code=Constants.CODE_DATE):
    date1 = dt.datetime.strptime (start, code)
    date2 = dt.datetime.strptime (end, code)
    time_to_expiry = yrs_btw (date1, date2)
    return time_to_expiry

def yrs_btw (date1, date2, basis=Constants.BASIS):
    delta = date2 - date1
    delta_in_yrs = float (delta.days / basis)
    return delta_in_yrs

#dict:

def union (dict1, dict2):
    return dict (list (dict1.items()) + list (dict2.items()))

#misc:

def cap_and_floor (down, mid, up):
    return min (max (down, mid), up)

def is_in_frame (x, frame):
    left, right = frame
    return x >= left and x <= right        

def switch (a, b):
    return b, a

def square (x):
    return x * x

#file

def get_file_name (ticker, date, path=Constants.DATA_PATH):
    prefix = '_' + ticker + '_' + date + '.json'
    def inner (s): return path + s + prefix
    return inner

def load (file_name):
    if os.path.isfile (file_name):
        file = open (file_name, 'r')
        return js.load (file)
    else: return None

def dump (data, file_name):
    file = open (file_name, 'w')
    js.dump (data, file, indent=2)

def get_mid (bid, ask):
    return 0.5 * (bid + ask)

#protected sqrt 

def protected_sqrt (up, down):
    if down <= 0 or mth.isnan (down): return 0.
    else: 
        if up <= 0: return 0
        else: return mth.sqrt (up / down)

def linear_regression (X, Y):
    b, a, _, _, _ = sps.linregress (X, Y)
    return a, b