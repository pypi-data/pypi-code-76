'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

from toolbox.monte_carlo.monte_carlo_engine import MeanVar, MonteCarloEngine, DEF_ALPHA, DEF_QUANT

from threading import Thread 

class UniMeanVar (MeanVar):

    #public:

        def __init__ (self, sum_x=0, sum_xx=0, size=0, t=0, s=1):
            super ().__init__ (size, t, s)
            self.sum_x = sum_x
            self.sum_xx = sum_xx
    
        def mean_core (self):
            return self.sum_x / self.size

        def var_core (self):
            return (self.sum_xx - self.size * self.mean_core () ** 2) / (self.size - 1)
        
        def __add__ (self, rhs):
            return UniMeanVar (self.sum_x + rhs.sum_x, self.sum_xx + rhs.sum_xx, self.size + rhs.size, self.trans, self.scale)

class MonteCarlo (MonteCarloEngine):

    #public:

        def __init__ (self, X, kwargs={}, t=0, s=1):
            super ().__init__ (X, UniMeanVar (), kwargs, t, s)

    #private:

        def monte_carlo (self, size, gens=None):
            if gens is None : return monte_carlo_core (self.X, size, self.kwargs)
            else: return multithd_monte_carlo (self.X, size, gens)

#toolkit:

def monte_carlo_core (X, size, kwargs={}):
    sample = [X (*kwargs.values ()) for _ in range (size)]
    sq_sample = [x ** 2 for x in sample]
    return UniMeanVar (sum (sample), sum (sq_sample), size)

def multithd_monte_carlo_aux (X, size, i, mean_vars, gens):
    mean_vars [i] = monte_carlo_core (X, size, gens [i])

def multithd_monte_carlo (X, size, gens):
    tot_mean_var = UniMeanVar ()
    sub_size = int (size / len (gens))
    mean_vars = [UniMeanVar () for gen in gens]
    thds = [Thread (target=multithd_monte_carlo_aux, args=(X, sub_size, idx, mean_vars, gens)) for idx, gen in enumerate (gens)]
    for thd in thds: thd.start ()
    for thd in thds: thd.join ()
    for mean_var in mean_vars: tot_mean_var += mean_var
    return tot_mean_var