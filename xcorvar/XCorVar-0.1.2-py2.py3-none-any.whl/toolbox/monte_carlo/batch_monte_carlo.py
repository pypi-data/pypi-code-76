'''
Copyright (C) 2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import numpy as np

from toolbox.monte_carlo.monte_carlo_engine import MeanVar, MonteCarloEngine, DEF_ALPHA, DEF_QUANT

class BiMeanVar (MeanVar):

    #public:

        def __init__ (self, sum_x=0, sum_xx=0, sum_y=0, sum_yy=0, sum_xy=0, size=0, t=0, s=1):
            super ().__init__ (size, t, s)
            self.sum_x = sum_x
            self.sum_y = sum_y
            self.sum_xx = sum_xx
            self.sum_yy = sum_yy
            self.sum_xy = sum_xy

        def x_mean (self):
            return self.sum_x / self.size

        def y_mean (self):
            return self.sum_y / self.size

        def xx_mean (self):
            return self.sum_xx / self.size

        def yy_mean (self):
            return self.sum_yy / self.size

        def beta (self):
            return self.sum_xy / self.sum_yy 

        def x_var (self):   
            return self.xx_mean () - self.x_mean () ** 2
        
        def y_var (self):
            return self.yy_mean ()

        def var_core (self):
            return self.x_var () - self.beta () ** 2 * self.y_var ()

        def mean_core (self):
            return self.x_mean () - self.beta () * self.y_mean ()

        def __add__ (self, rhs):
            return BiMeanVar (self.sum_x + rhs.sum_x, self.sum_xx + rhs.sum_xx, self.sum_y + rhs.sum_y, self.sum_yy + rhs.sum_yy, self.sum_xy + rhs.sum_xy, self.size + rhs.size, self.trans, self.scale)

class BatchMonteCarlo (MonteCarloEngine):

    #public:

        def __init__ (self, join, kwargs={}, t=0, s=1):
            super ().__init__ (join, BiMeanVar (), kwargs, t, s)

    #private:

        def monte_carlo (self, size, gens=None):
            if gens is None : return batch_monte_carlo_core (self.X, size, self.kwargs)
            else: NotImplementedError

#toolkit:

def trans (x, y):
    return np.array ([x, x * x, y, y * y, x * y])

def batch_monte_carlo_core (join, size, kwargs):
    sample = [join (*kwargs.values ()) for _ in range (size)]
    args_sum = sum ([trans (*args) for args in sample])
    return BiMeanVar (*args_sum, size)