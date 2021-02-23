# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Decomposer o-- Initializer

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.decomposition import PCA
from scipy import stats

from .principal_component import PC

# abstract class
class Initializer():
    def __init__(self):
        self.__init = PC()
        self.__loading = np.array([[],[]]) # loading matrix (p x q)
        self.__fscore = np.array([[],[]]) # factor score matrix (n x q)
        self.__contr = np.array([]) # contribution


    def to_pc(self):
        """ switch to principal component method """
        self.__init = PC()
    

    def func(self,data,ndata):
        """ extract initial factors """
        self.loading,self.fscore,self.contr = self.__init.func(data,ndata)
        return self.loading,self.fscore,self.contr
    