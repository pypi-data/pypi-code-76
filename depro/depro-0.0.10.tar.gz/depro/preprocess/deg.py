# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- PreProcessor o-- PreProcess o-- DEG

@author: tadahaya
"""
import numpy as np
import pandas as pd

from .._utils import statistics as st
from .._utils import normalizer as nor


class DEGIqr():
    def __init__(self):
        pass

    def __vec2tpl(self,mtx,fold=2.0,method="iqr",nmin=None,nmax=None):
        """ convert dataframe into tuple of tags """
        sample_name = list(mtx.columns)
        n_sample = len(sample_name)
        n_feature = len(mtx.index)
        if nmin is None:
            nmin = 15
        if nmax is None:
            nmax = int(0.01*n_feature)
        if method=="std":
            upper,lower = st.outlier_std(mtx=mtx,fold=fold,axis=0)
        else:
            upper,lower = st.outlier_iqr(mtx=mtx,fold=fold,axis=0)
        res = []
        ap = res.append
        for i in range(n_sample):
            temp = mtx.iloc[:,i].sort_values(ascending=False)
            up_val = upper[i]
            low_val = lower[i]
            temp_l = list(temp.index)
            upper_tag = set(temp[temp > up_val].index)
            lower_tag = set(temp[temp < low_val].index)
            n_up = len(upper_tag)
            n_low = len(lower_tag)
            if n_up > nmax:
                upper_tag = set(temp_l[:nmax])
            elif n_up < nmin:
                upper_tag = set(temp_l[:nmin])
            if n_low > nmax:
                lower_tag = set(temp_l[-nmax:])
            elif n_low < nmin:
                lower_tag = set(temp_l[-nmin:])
            ap((upper_tag,lower_tag))
        return res


    def func(self,data,fold=3.0,method="iqr",nmin=None,nmax=None,
             raw=True,sep="_",position=0,control=""):
        """
        convert dataframe of response profiles into dict of tags

        Parameters
        ----------
        data: dataframe
            feature x sample matrix
            Groups of samples should be indicated like "treatment_1", "treatment_2", etc.

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
        if raw:
            check = [c for c in list(data.columns) if control not in c]
            check = [c for c in check if sep not in c]
            if len(check)==0: # check whether consensus signature can be applied
                data = nor.consensus_sig(data,sep=sep,position=position)
                data = nor.madz(data,control=control)
                data = nor.consensus_sig(data,sep=sep,position=position)
                col = [v.split(sep)[0] for v in list(data.columns)]
                data.columns = col
                data = data.T.groupby(level=0,axis=0).mean().T
            else:
                raise ValueError("!! Sample names should include a separator like '_' to indicate groups !!")
        temp = self.__vec2tpl(data,fold,method,nmin,nmax)
        dic = dict(zip(list(data.columns),temp))
        return dic


class DEGPval():
    def __init__(self):
        raise NotImplementedError

    def func(self,data):
        """
        get differentially expressed genes

        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample) array

        """
        raise NotImplementedError

