# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator o-- Parallel

@author: tadahaya
"""
import pandas as pd
import numpy as np
from numpy.random import normal
from scipy.stats import bernoulli
import collections
from tqdm import trange
from sklearn.utils.extmath import randomized_svd


# concrete method
class Parallel():
    def __init__(self):
        self.nfactor = 0
        self.__true_contr = np.array([]) # for plot
        self.__rand_contr = np.array([]) # for plot
        self.__randomize = RandomFlip()


    def to_normal(self):
        """ change randomization strategy to that based on normal distribution """
        self.__randomize = RandomNormal()


    def to_shuffle(self):
        """ change randomization strategy to that based on shuffling data """
        self.__randomize = RandomShuffle()


    def to_flip(self):
        """ change randomization strategy to that based on flipping data """
        self.__randomize = RandomFlip()


    def get_contr(self):
        """
        get eigen values for contribution calculation and plot
        
        Return
        ------
        true_eigen_values: eigen values derived from the actual data
        random_eigen_values: eigen values derived from the representative random data
        
        """
        return self.__true_contr,self.__rand_contr


    def get_nfactor(self,X,perm:int=5,randomize:str="flip",**kwargs):
        """
        estimate the factor No. with parallel analysis
        randomization with Normal distribution

        Parameters
        ----------
        X: 2D array
            data x feature matrix

        perm: int
            indicate permutation No. for parallel analysis
        
        randomize: str
            indicate how to prepare randomized data for null contribution

        """
        ### preparation
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]        
        dat = PCAContr()
        dat.fit(X)
        self.__true_contr = dat.get_contr()

        ### contribution of randomized data
        if randomize=="flip":
            self.to_flip()
        elif randomize=="shuffle":
            self.to_shuffle()
        elif randomize=="normal":
            self.to_normal()
        else:
            raise KeyError("!! Wrong randomize: choose 'flip', 'shuffle', or 'normal' !!")
        rand_contr = self.__randomize.calc_random(X,perm)

        ### determine the threshold
        checker = self.__true_contr - rand_contr
        high = np.sum(checker > 0,axis=1)
        self.nfactor = _mode_higher(high)
        high_idx = [i for i,v in enumerate(high) if v==self.nfactor]
        self.__rand_contr = rand_contr[np.min(high_idx)]
        return self.nfactor


class RandomNormal():
    """ randomization based on normal distribution """
    def calc_random(self,X,perm:int):
        """ calculate the contribution of randomized data """
        X_c = X.copy()
        Xshape = X_c.shape
        myu = np.mean(np.mean(X_c,axis=0))
        scale = np.mean(np.std(X_c,ddof=1,axis=0))
        rand_contr = []
        ap = rand_contr.append
        for i in trange(perm):
            Xrand = normal(myu,scale,Xshape)
            
            ### get contribution
            dat = PCAContr()
            dat.fit(Xrand)
            temp_contr = dat.get_contr()
            ap(temp_contr)
        return np.array(rand_contr)


class RandomShuffle():
    """ randomization based on shuffling data """
    def calc_random(self,X,perm:int):
        """ calculate the contribution of randomized data """
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
            dat = PCAContr()
            dat.fit(Xrand)
            temp_contr = dat.get_contr()
            ap(temp_contr)
        return np.array(rand_contr)


class RandomFlip():
    """ randomization based on flipping data """
    def calc_random(self,X,perm:int):
        """ calculate the contribution of randomized data """
        X_c = X.copy()
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]        
        rand_contr = []
        ap = rand_contr.append
        for i in trange(perm):
            be_rand = np.array([bernoulli.rvs(p=0.5,size=ndata) for j in range(nfeat)]).T*2 - 1
            Xrand = X_c*be_rand

            ### get contribution
            dat = PCAContr()
            dat.fit(Xrand)
            temp_contr = dat.get_contr()
            ap(temp_contr)
        return np.array(rand_contr)


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


def _mode_higher(array):
    """ return mode which is highest when multiple hits """
    res = collections.Counter(array).most_common()
    mod = res[0]
    res = [v[0] for v in res if v[1]==mod[1]]
    return np.max(res)