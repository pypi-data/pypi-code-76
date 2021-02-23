# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer o-- Rotator o-- Varimax

@author: maedera and tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats
from math import cos,sin

class Varimax():
    def __init__(self):
        self.__loading = np.array([[],[]])
        self.__fscore = np.array([[],[]])
        self.__contr = np.array([])


    def func(self,data,loading,nfactor,ndata=None,acceptable_err=1.0e-9):
        """
        decompose a given matrix without rotation
        
        Parameters
        ----------
        data: array
            preprocessed data (ex. mirror)
            feature x data (ex. gene x sample) array

        loading: array
            feature x factor (ex. gene x factor) array

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
        print("{} factors are subjected to Varimax rotation".format(nfactor))
        f = loading[:,:nfactor]
        rotated = self.__varimax(f,acceptable_err)
        
        ### sort factors based on variance of factor scores
        temp_score = rotated.T.dot(data)
        temp_vars = np.var(temp_score,axis=1)
        temp = dict(zip(temp_vars,rotated.T))
        s_temp = sorted(temp.items(),reverse=True)
        s_contr = np.array([v[0] for v in s_temp])
        s_rotated = np.array([v[1] for v in s_temp]).T
        self.__loading = np.c_[s_rotated,loading[:,nfactor:]]

        ### calculate factor scores
        centroid = np.c_[np.mean(data,axis=1)]
        self.__fscore = self.__loading.T.dot(data - centroid)

        ### calculate contribution
        self.__contr = s_contr/np.sum(s_contr)
        return self.__loading,self.__fscore,self.__contr # shape: feature x contracted, contracted x data, contracted


    def __varimax(self,X,acceptable_err=1.0e-7):
        """
        varimax rotation algorithm
        
        Parameters
        ----------
        X: array
            loading matrix
        
        """
        vn = X.shape[0]
        vp = X.shape[1]
        A = X.copy()
        h = [np.linalg.norm(A[i,:]) for i in range(vn)] # normalization, not necessary in principal component method
        for i in range(vn):
            A[i,:] /= h[i]
        if vp < 2:
            return A
        while True:
            ckA = A.copy()
            for i in range(vp):
                for j in range(i+1,vp):
                    x = A.T[i]
                    y = A.T[j]
                    u = x**2 - y**2
                    v = 2.0 * x * y
                    cA = np.sum(u)
                    cB = np.sum(v)
                    cC = np.sum(u**2) - np.sum(v**2)
                    cD = 2.0 * u.dot(np.c_[v])[0]
                    num = cD - 2 * cA * cB / vn
                    den = cC - (cA**2 - cB**2) / vn
                    theta4 = np.arctan2(num,den)   
                    theta = theta4/4
                    theta = theta4 / 4.0
                    tx = A.T[i] * cos(theta) + A.T[j] * sin(theta)
                    ty = -A.T[i] * sin(theta) + A.T[j] * cos(theta)
                    A.T[i] = tx
                    A.T[j] = ty
            dif = np.sum((ckA - A)**2)
            print("\r" + str(dif),end="")
            if dif < acceptable_err:
                for i in range(vn):
                    A[i,:] *= h[i]
                break
        print("")
        return A # rotated loading matrix