'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import math as mth
import copy as cpy
import scipy.stats as scy_st

from matplotlib import pyplot as plt


DEF_ALPHA = 0.9544
DEF_QUANT = scy_st.norm.ppf (DEF_ALPHA)

class MeanVar:

    #public:

        def __init__ (self, size=0, trans=0, scale=1):
            self.size = size
            self.trans = trans
            self.scale = scale
            self.sq_scale = scale ** 2

        def mean_core (self):
            NotImplementedError

        def var_core (self):
            NotImplementedError

        @property
        def mean (self):
            return self.trans + self.scale * self.mean_core ()

        @property
        def var (self):
            return self.sq_scale * self.var_core ()

        def ic_size (self, quant=DEF_QUANT):
            return quant * mth.sqrt (self.var / self.size)

        def show (self, quant=DEF_QUANT):
            print ('mean: ', self.mean, 'ic_size: ', self.ic_size (quant), 'size: ', self.size)

class MonteCarloEngine:

    #public:

        def __init__ (self, X, curr, kwargs={}, t=0, s=1):
            self.X = X
            self.kwargs = kwargs
            self.hist = []
            self.curr = curr
                
        def add (self, size, gens=None, verbose=0):
            self.curr += self.monte_carlo (size, gens)
            if verbose > 0: self.curr.show ()
            self.hist.append (cpy.copy (self.curr))
            return self

        def add_until (self, eps, init=10, alpha=DEF_ALPHA, gens=None, verbose=0):
            quant = scy_st.norm.ppf (alpha)
            if self.hist == []: self.add (2 ** init, gens, verbose)
            while self.curr.ic_size (quant) > eps: self.add (self.curr.size, gens, verbose)
            return self

        def show (self, alpha=DEF_ALPHA):
            if self.hist == []: 
                print ('No Monte Carlo historic')
            else: 
                quant = scy_st.norm.ppf (alpha)
                for mean_var in self.hist: mean_var.show (quant)

        def plot (self, alpha=DEF_ALPHA):
            quant = scy_st.norm.ppf (alpha)
            plt.figure ()
            plt.title ('Monte Carlo Inspector')
            plt.xlabel ('Size')
            plt.ylabel ('Confidence Interval')
            for mean_var in self.hist:
                mean = mean_var.mean
                size = mean_var.size
                ic_size = mean_var.ic_size (quant)
                plt.plot ([size, size], [mean - ic_size, mean + ic_size], color='red', linewidth=0.5)
                plt.scatter (size, mean - ic_size, marker='2', color='red')
                plt.scatter (size, mean, marker='x', color='black')
                plt.scatter (size, mean + ic_size, marker='1', color='red')
            plt.show ()

    #private:

        def monte_carlo (self, size, gens=None):
            NotImplementedError

