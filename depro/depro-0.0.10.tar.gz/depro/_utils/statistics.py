# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

utilities: statistics

@author: tadahaya
"""
import numpy as np

def outlier_std(mtx,fold,axis=0):
    """ calculate upper and lower values for outlier detection """
    loc = np.mean(mtx.values,axis=axis)
    scale = np.std(mtx.values,axis=axis)        
    upper = loc + fold*scale
    lower = loc - fold*scale
    return upper,lower    
    
    
def outlier_iqr(mtx,fold,axis=0):
    """ calculate upper and lower values for outlier detection """
    q3 = np.percentile(mtx.values,75,axis=axis)
    q1 = np.percentile(mtx.values,25,axis=axis) 
    scale = q3 - q1        
    upper = q3 + fold*scale
    lower = q1 - fold*scale
    return upper,lower
