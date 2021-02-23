# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer o-- Rotator o-- Promax

@author: maedera and tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats

from .varimax import Varimax

class Promax():
    def __init__(self):
        self.__loading = np.array([[],[]])
        self.__fscore = np.array([[],[]])
        self.__contr = np.array([])
        self.__vmx = Varimax()


    def func(self,data,loading,nfactor,gmma=4,ndata=None,acceptable_err=1.0e-9):
        """
        decompose a given matrix without rotation
        
        Parameters
        ----------
        data: array
            preprocessed data (ex. mirror)
            feature x data (ex. gene x sample) array

        loading: array
            feature x factor (ex. gene x factor) array

        gmma: str
            determine power for indicating target matrix

        nfactor: int
            indicate the No. factors for rotation

        ndata: int
            indicate the No. of samples

        acceptable_err: float
            indicate the acceptable error in varimax rotation

        """
        ### rotation
        if nfactor > ndata:
            raise ValueError("!! nfactor is too large !!")
        L0,F0,C0 = self.__vmx.func(data=data,loading=loading,nfactor=nfactor,ndata=ndata,acceptable_err=acceptable_err)
        Lm = L0[:,:nfactor]
        Ls = L0[:,nfactor:]
        Fm = F0[:nfactor,:].T # transform matrix in general formation (n x p)
        Fs = F0[nfactor:,:]
        L = self.__promax(Lm,Lm.shape[0],Lm.shape[1],gmma) # rotated loading

        ### calculate score
        LtLinv = L.dot(np.linalg.inv(L.T.dot(L)))
        F = Fm.dot(L.T).dot(LtLinv)

        ### summary
        self.loading = np.c_[L,Ls]
        self.fscore = np.c_[F,Fs.T].T
        self.contr = C0/np.sum(C0)
        return self.loading,self.fscore,self.contr


    def __promax(self,V,n_vars,n_comp,gmma):
        """
        promax rotation algorithm
        
        Parameters
        ----------
        V: array
            rotated loading matrix (p x c)

        n_vars: int
            the No. of features

        n_comp: int
            the No. of components

        gmma: int
            indicate power for target matrix preparation

        """
        ua = V.copy()
        for i in range(n_vars):
            ua[i,:] /= np.linalg.norm(ua[i,:]) # normalization, not necessary for principal component method
        abs_ua = np.abs(ua)
        mxu = [np.max(abs_ua[:,i]) for i in range(n_comp)]
        u = ua.copy()
        for i in range(n_comp):
            u[:,i] /= mxu[i] # 最大値で割る理由は？
        C = np.array(np.sign(ua)) * (np.array(np.abs(u))**gmma)
        AtA = V.T.dot(V)
        AtAinv = np.linalg.inv(AtA)
        Q = AtAinv.dot(V.T).dot(C) # rotation matrix
        QtQinv = np.linalg.inv(Q.T.dot(Q))
        D = np.diag(np.diag(np.sqrt(QtQinv)))
        Lmbd = Q.dot(D)
        L = V.dot(Lmbd)
        return L