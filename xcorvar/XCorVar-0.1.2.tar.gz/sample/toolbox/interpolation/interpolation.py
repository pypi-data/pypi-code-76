'''
Copyright (C) 1994-2020 Matthieu Charrier. All rights reserved.
No part of this document may be reproduced or transmitted in any form
or for any purpose without the express permission of Matthieu Charrier.
'''

# !/usr/bin/env/ python3
# coding: utf-8

import math as mth
import numpy as np
import scipy.stats as sps

from matplotlib import pyplot as plt

class Interpolation:

    #public:

        def __init__ (self, grid):
            self.grid = grid
            self.size = len (grid)
            self.fst = self.grid [0]
            self.bf_lst = self.grid [-2]
            self.lst = self.grid [-1]

        def find_idx (self, x):
            return self.find_idx_core (x, 0, self.size-1)

        def find_obj (self, x):
            if self.fst.x > x: obj = self.fst
            elif self.lst.x < x: obj = self.bf_lst
            else: 
                idx, _ = self.find_idx (x)
                obj = self.grid [idx]
            return obj

        def interpoler (self, x):
            raise NotImplementedError

        def plt (self, left, right, size):
            raise NotImplementedError

    #private:

        def find_idx_core (self, x, begin, end):
            if (end - begin == 1): return begin, end
            mid = mth.floor (0.5 * (begin + end))
            x0 = self.grid [mid].x
            if x0 < x: begin = mid 
            else: end = mid
            return self.find_idx_core (x, begin, end)
            