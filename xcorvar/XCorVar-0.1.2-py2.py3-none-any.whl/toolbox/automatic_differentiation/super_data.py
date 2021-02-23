# coding: utf-8

import logging as lg
import numpy as np
import math as mth
import scipy.stats as sps

from sample.toolbox.mathbox import INV_SQRT_TWICE_PI

lg.basicConfig (level=lg.WARNING)

class SuperFloat:

    #public:

        def __init__ (self, val, grad):
            self.val = val
            self.grad = grad

        def get_attr (self):
            return self.val, self.grad
            
        def __str__ (self):
            return 'val: ' + str (self.val) + '\n' + 'grad: ' + str (self.grad)

        def __lt__ (self, other):
            try: return self.val < other.val
            except AttributeError: return self.val < other

        def __le__ (self, other):
            try: return self.val <= other.val
            except AttributeError: return self.val <= other

        def __gt__ (self, other):
            try: return self.val > other.val
            except AttributeError: return self.val > other

        def __ge__ (self, other):
            try: return self.val >= other.val
            except AttributeError: return self.val >= other

        def __eq__ (self, other):
            try: return self.val == other.val
            except AttributeError: return self.val == other

        def __ne__ (self, other):
            try: return self.val != other.val
            except AttributeError: return self.val != other

        def __add__ (self, rhs):
            try:
                grad = self.grad + rhs.grad
                val = self.val + rhs.val
            except AttributeError:
                grad = self.grad
                val = self.val + rhs
            return SuperFloat (val, grad)

        def __radd__ (self, lhs):
            return self + lhs

        def __sub__ (self, rhs):
            try:
                grad = self.grad - rhs.grad
                val = self.val - rhs.val
            except AttributeError:
                grad = self.grad
                val = self.val - rhs
            return SuperFloat (val, grad)

        def __rsub__ (self, lhs):
            return - (self - lhs)

        def __neg__ (self):
            grad = -self.grad
            val = -self.val
            return SuperFloat (val, grad)
        
        def __pos__ (self):
            return self

        def __mul__ (self, rhs):
            try:
                grad = self.val * rhs.grad + rhs.val * self.grad
                val = self.val * rhs.val    
            except AttributeError:
                grad = rhs * self.grad
                val = rhs * self.val
            return SuperFloat (val, grad)

        def __rmul__ (self, lhs):
            return self * lhs

        def __truediv__ (self, rhs):
            try:
                try:
                    inv_rhs_val = 1 / rhs.val
                    sq_inv_rhs_val = inv_rhs_val ** 2
                    grad = (rhs.val * self.grad - self.val * rhs.grad) * sq_inv_rhs_val
                    val = self.val / rhs.val
                except AttributeError:
                    grad = self.grad / rhs
                    val = self.val / rhs
            except ZeroDivisionError:
                lg.warning ('Zero division occured')
            return SuperFloat (val, grad)

        def __pow__ (self, n):
            val1 = self.val ** (n-1)
            val0 = self.val * val1
            grad = n * val1 * self.grad 
            val = val0
            return SuperFloat (val, grad)

class SuperFunc:

    #public:

        def __init__ (self, func):
            self.func = func
        
        def __call__ (self, *args, wghts=None):
            if wghts is None: wghts = np.eye (len (args))
            X = [SuperFloat (x, w) for w, x in zip (wghts, args)]
            return self.func (*X)

#toolkit:

def exp (x):
    try:
        exp_val = mth.exp (x.val)
        grad = exp_val * x.grad 
        val = exp_val
        return SuperFloat (val, grad)
    except AttributeError:
        return mth.exp (x)

def sqrt (x):
    try:
        sqrt_val = mth.sqrt (x.val)
        grad = 0.5 / sqrt_val * x.grad 
        val = sqrt_val
        return SuperFloat (val, grad)
    except AttributeError:
        return mth.sqrt (x)    

def cdf (x):
    try:
        val = sps.norm.cdf (x.val)
        grad = INV_SQRT_TWICE_PI * mth.exp (-0.5 * x.val * x.val) * x.grad 
        return SuperFloat (val, grad)
    except AttributeError:
        return sps.norm.cdf (x)    