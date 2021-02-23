# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Organizer of data preprocessing

DePro o-- PreProcessor o-- PreProcess

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .sphere import Sphere
from .mirror import Mirror
from .deg import DEGIqr,DEGPval

# abstract class
class PreProcess():
    def __init__(self):
        self.__sph = Sphere()
        self.__mirr = Mirror()
        self.__outs = []

    def get_outliers(self):
        return self.__outs

    def get_deg(self):
        """ extract DEG from input data """
        raise NotImplementedError


    def preprocess(self,data,sphere=True,mirror=True,alpha=0.05):
        """
        data preprocessing
            - unit-spherization (normalization of samples with L2 norm)
            - outlier detection with Smirnov-Grubbs test
            - mirror data

        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample) array

        sphere: boolean
            whether normalization of samples with L2 norm

        alpha: float
            indicate SG test criteria

        mirror: boolean
            whether mirror data is considered in decomposition

        """
        temp = data.copy()

        ### Mirror data
        if mirror:
            temp,self.__outs = self.__mirr.func(temp,alpha=alpha)

        ### unit-spherization
        if sphere:
            temp = self.__sph.func(temp)

        return temp


# abstract class
class DEG():
    def __init__(self):
        self.__deg = DEGIqr()

    def to_iqr(self):
        self.__deg = DEGIqr()

    def to_pval(self):
        self.__deg = DEGPval()

    def func(self,data,**kwargs):
        """
        convert dataframe of response profiles into dict of tags

        Parameters
        ----------
        data: dataframe
            feature x sample matrix

        fold: float
            determine threshold of outliers

        method: str
            "std" or "iqr"

        nmin,nmax: int
            indicate the minimum and maximum No. of genes in each tag
        
        raw: boolean
            indicates whether raw data is set or not
            if True, the data will be converted before tag making

        sep: str, default "_"
            separator for sample name
            
        position: int, default 0
            indicates position of sample name such as drug

        control: str
            indicates the control column name

        """
        return self.__deg.func(data,**kwargs)
