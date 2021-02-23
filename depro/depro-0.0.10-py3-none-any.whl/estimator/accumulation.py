# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator o-- Accumulation

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.utils.extmath import randomized_svd

class Accumulation():
    def __init__(self):
        self.nfactor = 0
        self.__contr = np.array([]) # for plot

    def get_contr(self):
        return self.__contr,np.array([])

    def get_nfactor(self,X,accumulation=0.8,show_nfactor=True,**kwargs):
        """
        estimate the factor No. from cumulative contribution

        Parameters
        ----------
        X: 2D array
            data x feature (ex. sample x gene) array

        accumulation: float
            indicate threshold of cumulative contribution
        
        """
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]        
        dat = PCAContr()
        dat.fit(X)
        self.__contr = dat.get_contr()
        contr = self.__contr/np.sum(self.__contr)
        acc_ctb = 0.0
        nfactor = 0
        for i in range(ndata):
            nfactor += 1
            acc_ctb += contr[i]
            if acc_ctb > accumulation:
                break
        self.nfactor = nfactor
        return self.nfactor

    
class PCAContr():
    def __init__(self):
        self.X = np.array([[],[]])
        self.n = 0
        self.p = 0
        self.lmd = np.array([])
    
    def fit(self,X,n_components=None):
        """
        X: 2d array
            sample x feature matrix (n x p)
            should be normalized in row (feature)
        
        """
        self.n = X.shape[0]
        self.p = X.shape[1]
        if n_components is None:
            n_components = np.min((self.n,self.p))
        U,S,V = randomized_svd(X,np.min(X.shape),transpose=False)
        lmd = S**2/self.n # the effect of sqrt(n) is reflected on sigma
        self.lmd = lmd[:n_components]

    def get_contr(self):
        return self.lmd