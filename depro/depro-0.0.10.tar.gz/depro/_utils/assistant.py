# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

assistant for coding

@author: tadahaya
"""

import time
import pickle

def chrono(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        res = func(*args,**kwargs)
        end = time.time()
        h,rem = divmod(end - start,3600)
        m,s = divmod(rem,60)
        print("--- {0} h {1} m {2} s ---".format(int(h),int(m),s))
        return res
    return wrapper


def to_pickle(data,url):
    """ to save as pickle """
    with open(url,"wb") as f:
        pickle.dump(data,f)


def read_pickle(url):
    """ to load pickle """
    with open(url,"rb") as f:
        temp = pickle.load(f)
    return temp