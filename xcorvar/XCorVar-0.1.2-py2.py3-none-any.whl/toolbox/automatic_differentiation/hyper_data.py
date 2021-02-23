# coding: utf-8

import math as mth
import logging as lg
import scipy.stats as sps
import numpy as np

from sample.toolbox.mathbox import INV_SQRT_TWICE_PI
from sample.toolbox.automatic_differentiation.super_data import SuperFloat

lg.basicConfig (level=lg.WARNING)

class HyperFloat (SuperFloat):

    #public:

        def __init__ (self, val, grad, hess):
            super ().__init__ (val, grad)
            self.hess = hess

        def __str__ (self):
            return super ().__str__ () + '\n' + 'hess: ' + str (self.hess)

        def __add__ (self, rhs):
            super_attr = super ().__add__ (rhs).get_attr ()
            try: hess = self.hess + rhs.hess
            except AttributeError: hess = self.hess
            return HyperFloat (*super_attr, hess)

        def __sub__ (self, rhs):
            super_attr = super ().__sub__ (rhs).get_attr ()
            try: hess = self.hess - rhs.hess
            except AttributeError: hess = self.hess
            return HyperFloat (*super_attr, hess)

        def __rsub__ (self, lhs):
            super_attr = super ().__rsub__ (lhs).get_attr ()
            try: hess = lhs.hess - self.hess
            except AttributeError: hess = -self.hess
            return HyperFloat (*super_attr, hess)

        def __neg__ (self):
            super_attr = super ().__neg__ ().get_attr ()
            hess = -self.hess
            return HyperFloat (*super_attr, hess)

        def __mul__ (self, rhs):
            super_attr = super ().__mul__ (rhs).get_attr ()
            try:
                fst_der = rhs.val, self.val
                snd_der = 0, 1, 0
                hess = self.hessian2 (rhs, *fst_der, *snd_der)
            except AttributeError:
                hess = rhs * self.hess
            return HyperFloat (*super_attr, hess)

        def __rmul__ (self, lhs):
            return self * lhs

        def __truediv__ (self, rhs):
            try:
                try:
                    inv_rhs_val = 1 / rhs.val
                    sq_inv_rhs_val = inv_rhs_val ** 2
                    cb_inv_rhs_val = inv_rhs_val * sq_inv_rhs_val
                    fst_der = inv_rhs_val, -self.val * sq_inv_rhs_val
                    snd_der = 0, -sq_inv_rhs_val, 2 * self.val * cb_inv_rhs_val
                    val = self.val / rhs.val
                    grad = (rhs.val * self.grad - self.val * rhs.grad) * sq_inv_rhs_val
                    hess = self.hessian2 (rhs, *fst_der, *snd_der)
                except AttributeError:
                    val = self.val / rhs
                    grad = self.grad / rhs
                    hess = self.hess / rhs
            except ZeroDivisionError:
                lg.warning ('Zero division occurs')
            return HyperFloat (val, grad, hess)

        def __pow__ (self, n):
            val2 = self.val ** (n-2)
            val1 = self.val * val2
            val0 = self.val * val1
            fst_der = n * val1
            snd_der = n * (n-1) * val2
            val = val0
            grad = fst_der * self.grad 
            hess = self.hessian1 (fst_der, snd_der)
            return HyperFloat (val, grad, hess)

    #private:

        def hessian1 (self, du, duu):
            fst = du * self.hess
            snd = duu * self.grad.T @ self.grad
            return fst + snd
        
        def fst_hessian2 (self, rhs, du, dv):
            return du * self.hess + dv * rhs.hess

        def snd_hessian2 (self, rhs, duu, dvv, duv):
            self_t_self = self.grad.T @ self.grad
            rhs_t_rhs = rhs.grad.T @ rhs.grad
            rhs_t_self = rhs.grad.T @ self.grad
            self_t_rhs = self.grad.T @ rhs.grad
            return duu * self_t_self + dvv * rhs_t_rhs + duv * (rhs_t_self + self_t_rhs)

        def hessian2 (self, rhs, du, dv, duu, duv, dvv):
            fst = self.fst_hessian2 (rhs, du, dv)
            snd = self.snd_hessian2 (rhs, duu, dvv, duv)
            return fst + snd

class HyperFunction:

    #public:

        def __init__ (self, func):
            self.func = func
        
        def __call__ (self, *args):
            if not hasattr (self, 'I') or not hasattr (self, 'O'):
                n = len (args)
                self.I = np.eye (n)
                self.O = np.zeros ((n, n))
            X = [HyperFloat (x, np.array ([self.I [i]]), self.O) for i, x in enumerate (args)]
            return self.func (*X)

#toolkit:

def exp (x):
    try:
        exp_val = mth.exp (x.val)
        fst_der = exp_val
        snd_der = exp_val
        hess = x.hessian1 (fst_der, snd_der) 
        grad = fst_der * x.grad 
        val = exp_val
        return HyperFloat (val, grad, hess)
    except AttributeError:
        return np.exp (x)

def sqrt (x):
    try:
        sqrt_val = mth.sqrt (x.val)
        fst_der = 0.5 / sqrt_val
        snd_der = -0.5 * fst_der / x.val
        hess = x.hessian1 (fst_der, snd_der)
        grad = fst_der * x.grad 
        val = sqrt_val
        return HyperFloat (val, grad, hess)
    except AttributeError:
        return np.sqrt (x)    

def cdf (x):
    try:
        cdf_val = sps.norm.cdf (x.val)
        fst_der = INV_SQRT_TWICE_PI * mth.exp (-0.5 * x.val * x.val)
        snd_der = -x.val * fst_der 
        hess = x.hessian1 (fst_der, snd_der)
        grad = fst_der * x.grad 
        val = cdf_val
        return HyperFloat (val, grad, hess)
    except AttributeError:
        return sps.norm.cdf (x)    