# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Data

@author: tadahaya
"""
import pandas as pd
import numpy as np


# abstract class
class Data():
    def __init__(self):
        self.data = {"X":None,"ts":None,"index":None,"columns":None}
        self.processed = {"X":None,"outlier":None}
        self.nfactor = 0
        self.decomposed = {"loading":None,"fscore":None,"contribution":None,"ts":None}
        self.state = {"mirror":True,"sphere":True,"estimator":"parallel",
        "initializer":"principal_component","rotator":"varimax"}

    ### data loading ###
    def set_data(self,data):
        """ load data """
        if type(data)==pd.core.frame.DataFrame:
            X = data.values
            ts = np.linalg.norm(X,axis=0)
            index = list(data.index)
            columns = list(data.columns)
            self.data = {"X":X,"ts":ts,"index":index,"columns":columns}
            self.decomposed["ts"] = ts
        else:
            raise TypeError("!! data should be a dataframe !!")

    def get_data(self):
        return self.data.copy()

    def update_state(self,key,value):
        """ update state """
        if key not in list(self.state.keys()):
            raise KeyError("!! Wrong key: 'mirror', 'sphere', 'estimator', 'initializer', or 'rotator' !!")
        self.state[key] = value

    def get_state(self):
        return self.state.copy()

    ### preprocessing ###
    def set_processed(self,key,value):
        """ set preprocessed data """
        if key not in list(self.processed.keys()):
            raise KeyError("!! Wrong key: 'X' or 'outlier' !!")
        self.processed[key] = value

    def get_processed(self):
        return self.processed.copy()

    ### estimate ###
    def set_nfactor(self,n):
        """ set the No. of factors """
        self.nfactor = n

    def get_nfactor(self):
        return self.nfactor

    ### decomposition ###
    def set_decomposed(self,key,value):
        """ set loading, fscore, or contribution """
        if key not in list(self.decomposed.keys()):
            raise KeyError("!! Wrong key: 'loading', 'fscore', 'contribution', or 'ts' !!")
        self.decomposed[key] = value

    def get_decomposed(self):
        return self.decomposed

        


