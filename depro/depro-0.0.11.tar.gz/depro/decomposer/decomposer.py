# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats

from .initializer.initializer import Initializer
from .rotator.rotator import Rotator

class Decomposer():
    def __init__(self):
        self.__init = Initializer()
        self.__rot = Rotator()
        self.__loading = np.array([[],[]])
        self.__fscore = np.array([[],[]])
        self.__contr = np.array([])

    ### data control
    def set_decomposed(self,loading=None,fscore=None,contribution=None):
        """ set external decomposed data """
        if loading is not None:
            self.__loading = loading
        if fscore is not None:
            self.__fscore = fscore
        if contribution is not None:
            self.__contr = contribution

    def get_decomposed(self):
        return {"loading":self.__loading,"fscore":self.__fscore,"contribution":self.__contr}

    ### initilizer control
    def to_pc(self):
        """ switch to principal component method """
        self.__init.to_pc()

    ### rotator control
    def to_varimax(self):
        """ switch to Varimax rotation """
        self.__rot.to_varimax()

    def to_promax(self):
        """ switch to Promax rotation """
        self.__rot.to_promax()

    ### decomposition
    def decompose(self,data,nfactor=None,ndata=None,rotate=True,acceptable_err=1.0e-7):
        """
        decompose a given matrix
        
        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample) array

        nfactor: int
            indicate the No. factors for rotation

        nsample: int
            indicate the No. of samples

        """
        ### initialize
        X = data.copy()
        if ndata is None:
            ndata = data.shape[1]
        L,F,C = self.__init.func(data=X,ndata=ndata)

        ### rotation
        if rotate:
            if (nfactor is None) or (nfactor==0):
                raise ValueError("!! Indicate the No. of factors (nfactor) !!")
            elif nfactor > len(C):
                raise ValueError("!! Inappropriate nfactor: nfactor should be less than the No. of components in initial factor prep!!")
            else:
                L,F,C = self.__rot.func(data=X,
                loading=L,nfactor=nfactor,ndata=ndata,acceptable_err=acceptable_err)

        self.__loading = L
        self.__fscore = F
        self.__contr = C
        return self.__loading,self.__fscore,self.__contr # shape: feature x contracted, contracted x data, contracted