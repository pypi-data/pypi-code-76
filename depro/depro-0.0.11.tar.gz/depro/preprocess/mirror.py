# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- PreProcessor o-- Mirror

@author: tadahaya
"""
import pandas as pd
import numpy as np

from .smir_grub import SG

# abstract class
class Mirror():
    def __init__(self):
        self.__sg = SG()

    def func(self,data,alpha=0.05):
        """
        convert data into mirror data
        
        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample)

        alpha: float
            the threshold for outlier detection with SG test

        """
        ts = np.linalg.norm(data,axis=0)
        remain,outs = self.__sg.get_index(ts,alpha=alpha)
        mirr = data[:,remain]
#        temp = np.c_[data,mirr*-1]
        temp = np.c_[mirr,mirr*-1]
        return temp,outs