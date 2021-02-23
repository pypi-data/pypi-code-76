# coding: utf-8

import copy as cpy
import math as mth
import numpy as np

from matplotlib import pyplot as plt

class State:

    #public:

        def __init__ (self, it, pts, val):
            self.iter = it
            self.pts = pts
            self.val = val

        def __str__ (self):
            return 'iter: ' + str (self.iter) + ' ' + 'val: ' + str (self.val)

class Int:

    #public:

        def __init__ (self, func, step, pts_init, val_init):
            self.func = func
            self.prog = None
            self.step = step
            self.curr = State (0, pts_init, val_init)
            self.hist = [cpy.copy (self.curr)]

        def __str__ (self):
            return str (self.curr) + ' ' + 'prog: ' + str (self.prog)

        def run (self, eps=1e-4, verbose=0):
            while self.prog is None or np.max (np.absolute (self.prog)) > eps: 
                self.next ()
                if verbose > 0: print (self)
            return self

        def show (self):
            for state in self.hist: 
                print (state)
                
        def plot (self):
            plt.figure ()
            plt.xlabel ('Iter')
            plt.ylabel ('Val')
            for state in self.hist:
                plt.scatter (state.iter, state.val, marker='+', color='black')
            plt.show ()

    #private:

        def next (self):
            self.step *= 0.5
            self.prog = -0.5 * self.curr.val + self.step * self.refine ()
            self.curr.iter += 1
            self.curr.val += self.prog
            self.hist.append (cpy.copy (self.curr))

        def refine (self):
            NotImplementedError


