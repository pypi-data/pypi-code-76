# coding: utf-8

import json as js
import math as mth
import cmath as cmth
import numpy as np
import scipy.optimize as sci_opt

from matplotlib import pyplot as plt

from models.heston_model.parameters import HestonParams

'''
from toolbox.integral.super_integral import SuperInt
from toolbox.mathbox import find_idx, INV_PI
from toolbox.black_scholes_functions import get_black_scholes_call_price_vega_core, get_black_scholes_call_price_core
from extraction import mat_wise_mkt_data
'''

class HestonCalibratedParams (HestonParams):

    #public:

        def __init__ (self, ticker, kind='mid', guess=None, npts=1):
            if guess is None: guess = np.array ([0.5, 5, 0.5, 0.5, -0.5])
            data = mat_wise_mkt_data (js.load (open (file='data/impl_tot_var_data_' + ticker + '.json', mode='r')), kind)
            super ().__init__ (*calibrate (data, npts, guess))

        def plt_slices (self):
            for mat, (log_fwd_mnn, mkt_impl_tot_var) in self.data.items ():
                log_fwd_mnn = np.array (log_fwd_mnn)
                fwd_mnn = np.exp (log_fwd_mnn)
                mdl_prices = lew_form (lambda z: heston_char_func (mat, log_fwd_mnn, self.params, z))
                mkt_prices = np.vectorize (get_black_scholes_call_price_core) (log_fwd_mnn, fwd_mnn, np.sqrt (mkt_impl_tot_var))
                plt.figure ()
                plt.title ('Heston model price vs market price slice at time to expiry ' + str (mat) + 'y')
                plt.xlabel ('Log forward moneyness')
                plt.ylabel ('Price')
                plt.scatter (log_fwd_mnn, mkt_prices, color='black', label='Market', marker='x')
                plt.scatter (log_fwd_mnn, mdl_prices, color='blue', label='Model', marker='x')
                plt.show ()

#toolkit:

def calibrate (data, npts=1, guess=None):
    mat = []
    log_fwd_mnn = []
    mkt_impl_tot_var = []
    for t, (k, w) in data.items ():
        lft, rgt = find_idx (k)
        for _ in range (npts):
            log_fwd_mnn.append (k [lft])
            log_fwd_mnn.append (k [rgt])
            mkt_impl_tot_var.append (w [lft])
            mkt_impl_tot_var.append (w [rgt])
            mat.extend (2 * [t])
            lft -= 1
            rgt += 1
    mat = np.array (mat)
    log_fwd_mnn = np.array (log_fwd_mnn)
    fwd_mnn = np.exp (log_fwd_mnn)
    mkt_impl_tot_vol = np.sqrt (mkt_impl_tot_var)
    mkt_prices, mkt_vegas = np.vectorize (get_black_scholes_call_price_vega_core) (log_fwd_mnn, fwd_mnn, mkt_impl_tot_vol)
    down = np.array ([0, 0, 0, 0, -1])
    up = np.array ([1, 10, 1, 1, 1])
    bds = np.array ([down, up])
    args = mat, log_fwd_mnn, mkt_prices, mkt_vegas
    optim_alg = sci_opt.least_squares (fun=lst_sq_func, x0=guess, args=args, bounds=bds)
    return optim_alg.x

#mathkit:

def lst_sq_func (params, mat, log_fwd_mnn, mkt_prices, mkt_vegas):
    mdl_prices = lew_form (lambda z: heston_char_func (mat, log_fwd_mnn, params, z))
    return np.log (np.absolute (mdl_prices / mkt_prices)) / mkt_vegas

def heston_char_func (mat, log_fwd_mnn, params, z):
    v0, a, b, eta, rho = params
    c = a - eta * rho * z
    sq_eta = eta ** 2
    f = a * b / sq_eta
    gamma = cmth.sqrt (sq_eta * z * (1 - z) + c ** 2)
    half_gamma_mat = 0.5 * gamma * mat
    csh = np.cosh (half_gamma_mat)
    snh = np.sinh (half_gamma_mat)
    return np.exp (log_fwd_mnn * z.conjugate () - v0 / (gamma * csh / snh + c) * z * (1 - z) + f * c * mat) / (csh + c / gamma * snh) ** (2 * f)

def black_scholes_char_func (mat, log_fwd_mnn, sigma, z):
    half_var = 0.5 * sigma ** 2 * mat
    return np.exp (half_var * z * (z - 1) + log_fwd_mnn * z.conjugate ())

def lew_form (char_func):
    func = lambda u: char_func (0.5 + u * 1j) / (0.25 + u ** 2)
    cpx_price = 1 - INV_PI * SuperInt (func).run (eps=1e-4, batch=1).curr.val 
    return np.real (cpx_price)
