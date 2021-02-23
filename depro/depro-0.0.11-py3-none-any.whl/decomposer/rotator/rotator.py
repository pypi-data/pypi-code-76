# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer o-- Rotator

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats

from .varimax import Varimax
from .promax import Promax

# abstract class
class Rotator():
    def __init__(self):
        self.__rot = Varimax()
        self.__loading = np.array([[],[]])
        self.__fscore = np.array([[],[]])
        self.__contr = np.array([])

    def to_varimax(self):
        """ switch to varimax rotation """
        self.__rot = Varimax()

    def to_promax(self):
        """ switch to promax rotation """
        self.__rot = Promax()

    def func(self,data,loading,nfactor,ndata=None,acceptable_err=1.0e-7):
        """ rotate loading """
        L,F,C = self.__rot.func(data=data,loading=loading,nfactor=nfactor,ndata=ndata,acceptable_err=acceptable_err)
        self.__loading = L
        self.__fscore = F
        self.__contr = C
        return self.__loading,self.__fscore,self.__contr # shape: feature x contracted, contracted x data, contracted