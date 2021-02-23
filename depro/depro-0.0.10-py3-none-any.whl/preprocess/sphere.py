# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- PreProcessor o-- PreProcess o-- Sphere

@author: tadahaya
"""
import numpy as np

# abstract class
class Sphere():
    def __init__(self):
        pass

    def func(self,data):
        """
        unit-spherization (normalization of samples with L2 norm)

        Parameters
        ----------
        data: array
            feature x data (ex. gene x sample) array

        """
        return data/np.linalg.norm(data,axis=0)
