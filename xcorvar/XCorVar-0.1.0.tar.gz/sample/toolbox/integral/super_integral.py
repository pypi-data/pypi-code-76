# coding: utf-8

import copy as cpy
import numpy as np
from matplotlib import pyplot as plt

from toolbox.integral.integral import Int, State
from toolbox.integral.functionnal_integral import FuncInt

class SuperInt (Int):

    #public:

        def __init__ (self, func):
            self.func = func
            self.prog = None
            self.curr = State (0, [0], 0)
            self.hist = [cpy.copy (self.curr)]

        def __str__ (self):
            return str (self.curr) + ' ' + 'prog: ' + str (self.prog)

        def next (self, eps=1e-3, batch=1):
            pt = self.curr.pts [-1] + batch
            val = FuncInt (self.func, self.curr.pts [-1], pt)
            self.curr.iter += 1
            self.curr.pts.append (pt)
            self.prog = val.run (eps).curr.val
            self.curr.val += self.prog
            self.hist.append (cpy.copy (self.curr))

        def run (self, eps=1e-3, batch=1, verbose=0):
            while self.prog is None or np.max (np.absolute (self.prog)) > eps:
                self.next (eps, batch)
                if verbose > 0: print (self)
            return self

        def show (self):
            for state in self.hist: 
                print (state)

        def plot (self):
            plt.figure ()
            plt.xlabel ('iter')
            plt.ylabel ('val')
            for state in self.hist:
                plt.scatter (state.iter, state.val, marker='+', color='black')
            plt.show ()
