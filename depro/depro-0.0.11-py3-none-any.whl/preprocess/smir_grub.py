# -*- coding: utf-8 -*-
"""

Created on Sat Mar  9 19:25:25 2019

@author: tadahaya
"""
import numpy as np
from scipy import stats

class SG():
    def __init__(self):
        pass

    def do_sg(self,data,alpha=0.05):
        """
        conduct Smirnov-Grubbs test on data (dataframe)
        return a dict containing:
            name: list of remaining data and outliers
            index: indices of remaining data and outliers
            data: arrays of remaining data and outliers
    
        Parameters
        ----------
        data: dataframe
            data

        alpha: float, default 0.05
            significance level

        """
        ind = list(data.index)
        val = data.values.flatten()
        res_ind = get_index(val,alpha=alpha)
        res_data = get_data(val,alpha=alpha)
        name_r = [ind[i] for i in res_ind[0]]
        name_o = [ind[i] for i in res_ind[1]]
        res_name = (name_r,name_o)
        key = ["name","index","data"]
        return dict(zip(key,[res_name,res_ind,res_data]))

    def get_data(self,data,alpha=0.05):
        """
        conducts Smirnov-Grubbs test on data (array)
        returns arrays of remaining data and outliers
        
        Parameters
        ----------
        data: numpy array
            data

        alpha: float, default 0.05
            significance level

        """
        x, o = list(data), []
        ap = o.append
        while True:
            n = len(x)
            if n < 3:
                break
            t = stats.t.isf(q=(alpha / n) / 2, df=n - 2)
            tau = (n - 1) * t / np.sqrt(n * (n - 2) + n * t * t)
            i_min, i_max = np.argmin(x), np.argmax(x)
            myu, std = np.mean(x), np.std(x, ddof=1)
            i_far = i_max if np.abs(x[i_max] - myu) > np.abs(x[i_min] - myu) else i_min
            tau_far = np.abs((x[i_far] - myu) / std)
            if tau_far < tau: break
            ap(x.pop(i_far))
        return (np.array(x), np.array(o))


    def get_index(self,data,alpha=0.05):
        """
        conducts Smirnov-Grubbs test on data (array)
        returns indices of remaining data and outlier ones
        
        Parameters
        ----------
        data: numpy array
            data

        alpha: float, default 0.05
            significance level

        Returns
        ----------
        rem: remained
        o: outliers

        """
        x, o = list(data), []
        y = list(data)
        ap = o.append
        while True:
            n = len(x)
            if n < 3:
                break
            t = stats.t.isf(q=(alpha / n) / 2, df=n - 2)
            tau = (n - 1) * t / np.sqrt(n * (n - 2) + n * t * t)
            i_min, i_max = np.argmin(x), np.argmax(x)
            myu, std = np.mean(x), np.std(x, ddof=1)
            i_far = i_max if np.abs(x[i_max] - myu) > np.abs(x[i_min] - myu) else i_min
            tau_far = np.abs((x[i_far] - myu) / std)
            if tau_far < tau: break
            ap(np.where(y==x[i_far])[0][0])
            del x[i_far]
        rem = [v for v in list(range(len(data))) if v not in o]
        return (rem,o)