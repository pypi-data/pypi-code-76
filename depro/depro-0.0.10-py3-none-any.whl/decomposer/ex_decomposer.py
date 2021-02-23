# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- ExDecomposer

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from scipy import stats

from enan.connect import Connect

class ExDecomposer():
    def __init__(self):
        self.__analyzer = Connect()
        self.__loading = np.array([[],[]]) # feature x contracted
        self.__deg = dict() # {term:tuples of up/down tags}
        self.__res = pd.DataFrame()
        

    def set_loading(self,data,trim=True,key="V"):
        """
        load rotated loading
        
        Parameters
        ----------
        data: dataframe
            feature x contracted dataframe derived from rotation

        trim: boolean
            whether loading is trimmed based on the indicated key

        key: str
            indicates the keyword for trimming

        """
        if trim:
            data = data.loc[:,data.columns.str.contains(key)]
        self.__loading = data


    def set_deg(self,data):
        """
        load DEG of chemicals of interest
        
        Parameters
        ----------
        data: dict
            a dictionary like {term:tuples of up/down tags}
            the terms correspond to chemicals of interest
        
        """
        self.__deg = data


    def get_res(self):
        """ result getter """
        return self.__res


    ### decomposition
    def decompose(self):
        """
        decompose a given matrix
        
        Parameters
        ----------
        species: str
            indicates the species to be analyzed

        """
        if len(self.__deg)==0:
            raise ValueError("!! set_deg() before this process !!")
        self.__analyzer.fit(self.__deg)
        temp = self.__loading
        self.__res = self.__analyzer.calc(temp).T
        return self.__res