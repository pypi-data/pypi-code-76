# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator o-- MAPc

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from tqdm import trange

# concrete method
class MAPc():
    def __init__(self):
        self.nfactor = 0


    def get_contr(self):
        raise NotImplementedError("!! MAP estimation does not calculate contribution !!")


    def get_nfactor(self,X,monotonic_check=5,thresh_pcorr=0.0001,fourth=False,**kwargs):
        """
        estimate the factor No. based on minimal average partial correlation (MAP)

        Parameters
        ----------
        X: 2D array
            data x feature matrix
            should be normalized

        monotonic_check: int
            indicate the upper limit of monotonic increase of the difference

        thresh_pcorr: float
            indicate partial correlation low enough to end calculation

        fourth: boolean
            whether fourth power is employed in difference calculation
            the fourth option returns more precise estimation in general but takes long time

        """
        ### preparation
        nfeat = X.shape[1] # assume that data size > No. of features
        ndata = X.shape[0]
        R = X.T.dot(X)/ndata

        ### calculate loading
        U,S,V = np.linalg.svd(X/np.sqrt(ndata),full_matrices=False)
        loading = V.T.dot(np.diag(S)) # V is normalized, thus multiply singular values

        ### calculate average partial correlation
        num = 2
        if fourth:
            num = 4
        apcs = [1.0]
        ap = apcs.append
        count = 0
        for i in trange(loading.shape[1] - 1):
            temp = loading[:,:i + 1]
            pcorr = R - temp.dot(temp.T) # partial correlation
            if np.max(pcorr) > thresh_pcorr:
                d = 1/np.sqrt(np.diag(pcorr))
#                pcorr = np.diag(d).dot(pcorr.dot(np.diag(d))) # slower than __dX
                pcorr = self.__dX(d,pcorr)
                apc = (np.sum(pcorr**num) - nfeat)/(nfeat*(nfeat - 1))
                if apc > apcs[-1]: # check monotonic increase
                    count += 1
                    if count >= monotonic_check:
                        break
                else:
                    count = 0
                ap(apc)
            else:
                break
        minpc = np.min(apcs)
        minidx = apcs.index(minpc)
        return minidx
    

    def __dX(self,d,X):
        return d*X*np.c_[d]