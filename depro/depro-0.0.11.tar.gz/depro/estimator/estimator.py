# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

DePro o-- Estimator

@author: tadahaya
"""
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from numpy.random import normal
from scipy.stats import bernoulli
import os
import csv
import collections
from tqdm import trange
from sklearn.decomposition import PCA
from sklearn.utils.extmath import randomized_svd

from .accumulation import Accumulation
from .parallel import Parallel
from .smc import SMC
from .mapc import MAPc
from ._est_plot import ScreePlot,AccPlot

EST_METHOD = ["parallel","smc","map","accumulation"]

# organizer
class Estimator():
    """ estimate factor No. """
    def __init__(self,estimation="parallel"):
        self.__emethod = EST_METHOD
        self.__estimator = estimation
        self.__splot = ScreePlot()
        self.__aplot = AccPlot()
        if estimation=="parallel":
            self.__method = Parallel()
        elif estimation=="smc":
            self.__method = SMC()
        elif estimation=="map":
            self.__method = MAPc()
        elif estimation=="accumulation":
            self.__method = Accumulation()
        else:
            self.__method = None

    def get_emethod(self):
        return self.__emethod

    def to_parallel(self):
        self.__method = Parallel()

    def to_smc(self):
        self.__method = SMC()

    def to_map(self):
        self.__method = MAPc()

    def to_accumulation(self):
        self.__method = Accumulation()

    def get_nfactor(self,X,**kwargs):
        """
        estimate the No. of factors
        
        Parameters
        ----------
        X: 2D array
            n x p array
            should be normalized in features

        perm: int
            * for 'parallel' and 'smc'
            indicate permutation times for randomization

        monotonic_check: int
            * for 'map'
            indicate the upper limit of monotonic increase of the difference

        thresh_pcorr: float
            * for 'map'
            indicate partial correlation low enough to end calculation

        fourth: boolean
            * for 'map'
            whether fourth power is employed in difference calculation

        """
        if self.__method is None:
            raise ValueError("!! Set method for estimation !!")
        return self.__method.get_nfactor(X,**kwargs)


    def scree_plot(self,**kwargs):
        """ Scree plot """
        tcont,rcont = self.__method.get_contr()
        if len(tcont)==0:
            raise ValueError("!! run 'get_nfactor' before visualization !!")
        self.__splot.plot(tcont,rcont,**kwargs)


    def accumulation_plot(self,**kwargs):
        """ Plot accumulation """
        tcont,rcont = self.__method.get_contr()
        if len(tcont)==0:
            raise ValueError("!! run 'get_nfactor' before visualization !!")
        self.__aplot.plot(tcont,**kwargs)