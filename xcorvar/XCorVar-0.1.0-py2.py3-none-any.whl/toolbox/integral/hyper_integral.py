# coding: utf-8

import copy as cpy
import numpy as np

from toolbox.integral.integral import Int, State
from toolbox.integral.functionnal_integral import FuncInt

class HyperInt:

    #public:

        def __init__ (self, func):
            self.func = func
            self.prog = None
            self.curr = State (0, [], 0)
            self.hist = []

        def __str__ (self):
            return str (self.curr) + ' ' + 'prog: ' + str (self.prog)

        def init (self, eps, batch):
            self.curr.pts = [-batch, batch]
            self.curr.val = FuncInt (self.func, -batch, batch).run (eps).curr.val
            self.hist.append (cpy.copy (self.curr))

        def next (self, eps, batch):
            right = self.curr.pts [-1] + batch
            left = self.curr.pts [0] - batch 
            val_left = FuncInt (self.func, left, self.curr.pts [0])
            val_right = FuncInt (self.func, self.curr.pts [-1], right)
            self.curr.iter += 1
            self.curr.pts.append (right)
            self.curr.pts.insert (0, left)
            prog_left = val_left.run (eps)
            prog_right = val_right.run (eps)
            self.prog = prog_left.curr.val + prog_right.curr.val
            self.curr.val += self.prog
            self.hist.append (cpy.copy (self.curr))
            
        def run (self, eps=1e-3, batch=1, verbose=0):
            self.init (eps, batch)
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

