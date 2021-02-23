# coding: utf-8

import math as mth
import logging as lg
import scipy.stats as sps
import numpy as np

from sample.toolbox.rootfinder import newton, dichotomy
from sample.toolbox.mathbox import square

lg.basicConfig (level=lg.WARNING)

#price:

def black_scholes_call_price (log_fwd_mnn, tot_var):
    tot_vol = np.sqrt (tot_var)
    fwd_mnn = np.exp (log_fwd_mnn)
    d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
    price = sps.norm.cdf (d1) - fwd_mnn * sps.norm.cdf (d2)
    return price

def get_black_scholes_call_price (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
    price = sps.norm.cdf (d1) - fwd_mnn * sps.norm.cdf (d2)
    return dsc_repo * spot * price

def get_black_scholes_call_price_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_call_price (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_put_price (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
    price = fwd_mnn * sps.norm.cdf (-d2) - sps.norm.cdf (-d1)
    return dsc_repo * spot * price    

def get_black_scholes_put_price_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_put_price (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_digicall_price (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    pass

def get_black_scholes_digicall_price_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_digicall_price (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_digiput_price (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    return 1 - get_black_scholes_digicall_price (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo)

def get_black_scholes_digiput_price_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_digiput_price (*to_std (mat, strike, vol, spot, rate, repo))

#delta:

def get_black_scholes_call_delta (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1 = - log_fwd_mnn / tot_vol + 0.5 * tot_vol
    delta = sps.norm.cdf (d1)
    return dsc_repo * delta

def get_black_scholes_call_delta_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_call_delta (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_put_delta (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    return get_black_scholes_call_delta (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo) - 1

def get_black_scholes_put_delta_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_put_delta (*to_std (mat, strike, vol, spot, rate, repo))

#dollargamma:

def get_black_scholes_call_dollargamma (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1 = - log_fwd_mnn / tot_vol + 0.5 * tot_vol
    dollargamma = mth.exp (-0.5 * square (d1)) / mth.sqrt (2 * mth.pi) / tot_vol        
    return dsc_repo * spot * dollargamma

def get_black_scholes_call_dollargamma_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_call_dollargamma (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_put_dollargamma (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    return get_black_scholes_call_dollargamma (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo)

def get_black_scholes_put_dollargamma_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_put_dollargamma (*to_std (mat, strike, vol, spot, rate, repo))

#vega:

def get_black_scholes_call_vega (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1 = - log_fwd_mnn / tot_vol + 0.5 * tot_vol
    return dsc_repo * spot * mth.exp (-0.5 * square (d1)) / mth.sqrt (2 * mth.pi)

def get_black_scholes_call_vega_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_call_vega (*to_std (mat, strike, vol, spot, rate, repo))

def get_black_scholes_put_vega (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    return get_black_scholes_call_vega (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo)

def get_black_scholes_put_vega_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_put_vega (*to_std (mat, strike, vol, spot, rate, repo))

#price_vega:

def get_black_scholes_call_price_vega (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
    price = dsc_repo * sps.norm.cdf (d1) - fwd_mnn * sps.norm.cdf (d2)
    vega = mth.exp (-0.5 * square (d1)) / mth.sqrt (2 * mth.pi)
    dsc_repo_times_spot = dsc_repo * spot
    return dsc_repo_times_spot * price, dsc_repo_times_spot * vega

#price_delta_dollargamma:

def get_black_scholes_call_price_delta_dollargamma (log_fwd_mnn, fwd_mnn, tot_vol, spot=1, dsc_repo=1):
    d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
    delta = sps.norm.cdf (d1)
    price = delta - fwd_mnn * sps.norm.cdf (d2)
    dollargamma = mth.exp (-0.5 * square (d1)) / mth.sqrt (2 * mth.pi) / tot_vol
    dsc_repo_times_spot = dsc_repo * spot
    return dsc_repo_times_spot * price, dsc_repo * delta, dsc_repo_times_spot * dollargamma

def get_black_scholes_call_price_delta_dollargamma_std (mat, strike, vol, spot=1, rate=0, repo=0):
    return get_black_scholes_call_price_delta_dollargamma (*to_std (mat, strike, vol, spot, rate, repo))

#impl_tot_var:

def get_at_the_money_implied_total_variance (price, spot=1):
    return square (2 * sps.norm.ppf (0.5 * (price + 1)) / spot)

def get_implied_total_variance (price, log_fwd_mnn, fwd_mnn, spot=1, dsc_repo=1, verbose=0, max_it=100, tol=1e-4):
    func_der = lambda tot_vol: get_black_scholes_call_price_vega (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo)
    init = mth.sqrt (abs (2 * log_fwd_mnn))
    impl_tot_vol = newton (func_der, price, init, max_it, tol, verbose)
    if impl_tot_vol != None: return square (impl_tot_vol)
    else:
        func = lambda tot_vol: get_black_scholes_call_price (log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo)
        impl_tot_vol = dichotomy (func, 1e-6, 1, price, tol, verbose)
        if impl_tot_vol != None: return square (impl_tot_vol)
        else: return None

#impl_vol:

def get_volatility (impl_tot_var, mat):
    try: return np.sqrt (impl_tot_var / mat)
    except ValueError as err:
        lg.warning ('Square root of negative number occurs: {}'.format (err))
        return 0
    except ZeroDivisionError as err:
        lg.warning ('Division by zero occurs: {}'.format (err))
        return 0
    except TypeError as err:
        lg.warning ('None type encountered: {}'.format (err))
        return 0

def get_impl_skew (impl_tot_var_skew, impl_vol, mat):
    try: 
        return 0.5 * impl_tot_var_skew / impl_vol / mat
    except ValueError as err:
        lg.warning ('Square root of negative number occurs: {}'.format (err))
        return 0
    except ZeroDivisionError as err:
        lg.warning ('Division by zero occurs: {}'.format (err))
        return 0
    except TypeError as err:
        lg.warning ('None type encountered: {}'.format (err))
        return 0

#geobrown:

class GeoBrown:

    #public:

        def __init__ (self, x0, a, b):
            self.x0 = x0
            self.a = a
            self.b = b

        def __call__ (self, time, noise):
            return self.x0 * np.exp (self.a * time + self.b * noise)

#to_std:

def to_std (mat, strike, vol, spot=1, rate=0, repo=0):
    rate = rate - repo
    dsc_repo = mth.exp (-repo * mat)
    fwd = spot * mth.exp (rate * mat)
    fwd_mnn = strike / fwd
    log_fwd_mnn = mth.log (fwd_mnn)
    tot_vol = vol * mth.sqrt (mat)
    return log_fwd_mnn, fwd_mnn, tot_vol, spot, dsc_repo

#d1,d2:

def get_d1_d2 (log_fwd_mnn, tot_vol):
    d1 = - log_fwd_mnn / tot_vol + 0.5 * tot_vol
    d2 = d1 - tot_vol
    return d1, d2
