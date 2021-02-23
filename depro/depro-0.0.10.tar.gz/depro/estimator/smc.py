# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator o-- SMC

@author: tadahaya
"""
import pandas as pd
import numpy as np
from numpy.random import normal
import collections
from tqdm import trange
from sklearn.utils.extmath import randomized_svd


# concrete method
class SMC():
    def __init__(self):
        self.nfactor = 0
        self.__true_contr = np.array([]) # for plot
        self.__rand_contr = np.array([]) # for plot


    def get_contr(self):
        """
        get eigen values for contribution calculation and plot
        
        Return
        ------
        true_eigen_values: eigen values derived from the actual data
        random_eigen_values: eigen values derived from the representative random data
        
        """
        return self.__true_contr,self.__rand_contr


    def get_nfactor(self,X,perm=3,**kwargs):
        """
        estimate the factor No. with diagonal SMC parallel analysis
        randomization with Normal distribution

        Parameters
        ----------
        X: 2D array
            data x feature matrix

        perm: int
            indicate permutation No. for parallel analysis
        
        """
        ### preparation
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]        
        dat = SMCContr()
        dat.fit(X)
        self.__true_contr = dat.get_contr()

        ### contribution of randomized data
        Xshape = X.shape
        myu = np.mean(X)
        uvar = np.var(X,ddof=1)
        rand_contr = []
        ap = rand_contr.append
        for i in trange(perm):
            Xrand = normal(myu,uvar,Xshape)
            
            ### get contribution
            dat = SMCContr()
            dat.fit(Xrand)
            temp_contr = dat.get_contr()
            ap(temp_contr)
        rand_contr = np.array(rand_contr)

        ### determine the threshold
        checker = self.__true_contr - rand_contr
        high = np.sum(checker > 0,axis=1)
        self.nfactor = _mode_higher(high)
        high_idx = [i for i,v in enumerate(high) if v==self.nfactor]
        self.__rand_contr = rand_contr[np.min(high_idx)]
        return self.nfactor


    def _get_nfactor_random(self,X,perm=5,**kwargs):
        """
        estimate the factor No. with parallel analysis

        Parameters
        ----------
        X: 2D array
            data x feature matrix

        perm: int
            indicate permutation No. for parallel analysis
        
        """
        ### preparation
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]        
        dat = SMCContr()
        dat.fit(X)
        self.__true_contr = dat.get_contr()

        ### contribution of randomized data
        X_c = X.copy()
        rand_contr = []
        ap = rand_contr.append
        for i in trange(perm):
            rand_data = []
            ap2 = rand_data.append
            for v in X_c:
                temp = v.copy()
                np.random.shuffle(temp)
                ap2(temp)
            Xrand = np.array(rand_data)
            
            ### get contribution
            dat = SMCContr()
            dat.fit(Xrand)
            temp_contr = dat.get_contr()
            ap(temp_contr)
        rand_contr = np.array(rand_contr)

        ### determine the threshold
        checker = self.__true_contr - rand_contr
        high = np.sum(checker > 0,axis=1)
        self.nfactor = _mode_higher(high)
        high_idx = [i for i,v in enumerate(high) if v==self.nfactor]
        self.__rand_contr = rand_contr[np.min(high_idx)]
        return self.nfactor


class SMCContr():
    def __init__(self):
        self.n = 0
        self.p = 0
        self.d2 = np.array([])
        self.smc = np.array([])
        self.lmd = np.array([])
        self.sum = 0.0

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
        U,S,V = randomized_svd(self._calc_smc(X),np.min(X.shape),transpose=False) # considering natures of symmetric matrix
        del U,V
        self.lmd = S[:n_components]

    def _calc_smc(self,X):
        R = X.T.dot(X)/X.shape[0]
        Rinv = np.linalg.inv(R)
        self.d2 = 1/np.diag(Rinv)
        del Rinv
        self.smc = 1 - self.d2 # squared multiple correlation is equivalent to communalities
        return R - np.diag(self.d2)

    def get_contr(self):
        return self.lmd

def _mode_higher(array):
    """ return mode which is highest when multiple hits """
    res = collections.Counter(array).most_common()
    mod = res[0]
    res = [v[0] for v in res if v[1]==mod[1]]
    return np.max(res)