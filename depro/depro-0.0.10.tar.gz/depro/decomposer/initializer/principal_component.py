# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer o-- Initializer o-- PC

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats

class PC():
    def __init__(self):
        self.__loading = np.array([[],[]]) # loading matrix (p x q)
        self.__fscore = np.array([[],[]]) # factor score matrix (n x q)
        self.__contr = np.array([]) # contribution


    def func(self,data,ndata=None):
        """
        decompose a given matrix without rotation
        
        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample) array
            probably preprocessed data

        ndata: int
            indicate the No. of data

        Returns
        ----------
        loading: loading matrix (novel axes)
        fscore: factor score matrix (principal components)
        contribution
        ncomp: the No. of principal components

        """
        X = data.T
        pca = PCA(svd_solver="full")
        pca.fit(X)
        self.__loading = pca.components_.T[:,:ndata]
        self.__contr = pca.explained_variance_ratio_[:ndata]
        centroid = np.c_[np.mean(data,axis=1)]
        self.__fscore = self.__loading.T.dot(data - centroid)
        return self.__loading,self.__fscore,self.__contr

