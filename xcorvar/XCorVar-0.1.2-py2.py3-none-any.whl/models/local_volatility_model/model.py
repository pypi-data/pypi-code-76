# coding: utf-8

import math as mth

from matplotlib import pyplot as plt
import numpy as np

from sample.constants import Constants
from sample.toolbox.diffusion.utilities import State
from sample.toolbox.diffusion.scheme import LocalVolatilityScheme
from sample.toolbox.diffusion.diffusion import Diffusion
from sample.toolbox.black_scholes_functions import get_volatility, get_implied_total_variance, get_at_the_money_implied_total_variance
from sample.toolbox.forward_partial_differential_equation import ForwardPartialDifferentialEquation
from sample.toolbox.mathbox import is_in_frame, find_index

class LocalVolatilityDiffusion:

    def __init__ (self, fwd, loc_vol, step=Constants.ONE_DAY):
        self.fwd = fwd 
        self.diffusion = Diffusion (LocalVolatilityScheme (loc_vol, step))

    def get_log_forward_spot_sample (self, time):
        return self.diffusion.restart ().run (time).scheme.state.space

    def get_spot_sample (self, time):
        return self.fwd (time) * mth.exp (self.get_log_forward_spot_sample (time))

    def get_trajectory_sample (self, mat):
        diffusion = self.diffusion.restart ().run (mat)
        diffusion.map (func=lambda state: State (state.time, self.fwd (state.time) * mth.exp (state.space)))
        diffusion.plt ()
            
class LocalVolatilityModel:

        def __init__ (self, spot, fwd, loc_vol):
            self.spot = spot
            self.fwd = fwd
            self.loc_vol = loc_vol
        
        def plot_calibration_accuracy (self, vol_surf, mat, frame=[30, 200]):
            lft = mth.log (Constants.ONE_PERCENT)
            rgt = mth.log (10)
            dt = 2 * Constants.ONE_WEEK
            dx = Constants.ONE_PERCENT
            pde = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt))
            log_fwd_mnns, prices = pde.run (mat).get_prices ()  
            plt.figure ()
            fwd_mnns = np.exp (log_fwd_mnns)
            for fwd_mnn, price in zip (fwd_mnns, prices): 
                if is_in_frame (100*fwd_mnn, frame):
                    vol = get_volatility (get_implied_total_variance (price, mth.log (fwd_mnn), fwd_mnn), mat)
                    if vol < 1: plt.scatter (100*fwd_mnn, 100*vol, marker='+', color='black')   
            fwd_mnns = np.array ([fwd_mnn for fwd_mnn in fwd_mnns if is_in_frame (100*fwd_mnn, frame)])
            log_fwd_mnns = np.log (fwd_mnns)
            plt.plot (100*fwd_mnns, 100*get_volatility (vol_surf (mat, log_fwd_mnns), mat), color='green')
            plt.show ()
                    
        def plot_volatility_dynamic (self, mat, spd=5):
            eps = spd * Constants.ONE_PERCENT
            lft = mth.log (Constants.ONE_PERCENT)
            rgt = mth.log (10)
            dt = 2 * Constants.ONE_WEEK
            dx = Constants.ONE_PERCENT
            log_fwd_mnn_down, prices_down = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt), eps=-eps).run (mat).get_prices ()
            log_fwd_mnn, prices = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt), eps=0).run (mat).get_prices ()
            log_fwd_mnn_up, prices_up = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt), eps=+eps).run (mat).get_prices ()
            tot_var_down = [get_implied_total_variance (price=p, log_fwd_mnn=k, fwd_mnn=mth.exp (k), spot=1-eps) for p, k in zip (prices_down, log_fwd_mnn_down)]
            tot_var = [get_implied_total_variance (price=p, log_fwd_mnn=k, fwd_mnn=mth.exp (k), spot=1) for p, k in zip (prices, log_fwd_mnn)]
            tot_var_up = [get_implied_total_variance (price=p, log_fwd_mnn=k, fwd_mnn=mth.exp (k), spot=1+eps) for p, k in zip (prices_up, log_fwd_mnn_up)]
            vol_down = [100 * get_volatility (w, mat) for w in tot_var_down]
            vol = [100 * get_volatility (w, mat) for w in tot_var]
            vol_up = [100 * get_volatility (w, mat) for w in tot_var_up]
            atm_down = vol_down [find_index (log_fwd_mnn_down) [0]]
            atm = vol [find_index (log_fwd_mnn) [0]]
            atm_up = vol_up [find_index (log_fwd_mnn_up) [0]]
            plt.figure ()
            plt.plot (np.exp (log_fwd_mnn_down) * 100, vol_down, label=str(int ((1-eps) * 100)) + '%' + ' spot', color='blue')
            plt.plot (np.exp (log_fwd_mnn) * 100, vol, label=str(100) + '%' + ' spot', color='black')
            plt.plot (np.exp (log_fwd_mnn_up) * 100, vol_up, label=str(int ((1+eps) * 100)) + '%' + ' spot', color='red')
            plt.scatter (100, atm_down, color='blue')
            plt.scatter (100, atm, color='black')
            plt.scatter (100, atm_up, color='red')
            plt.xlabel ('Forward moneyness (in %)')
            plt.ylabel ('Implied Volatility (in %)')
            plt.title ('Local Volatility Model - Implied Volatility Dynamic')
            plt.legend (loc='best')
            plt.axis ([50, 150, 0, 100])
            plt.show ()

        def plot_skew_stickiness_ratio (self, mat=1):
            plt.figure ()
            plt.xlabel ('Maturity (in years)')
            plt.ylabel ('Skew Stickiness Ratio')
            plt.title ('Local Volatility Model - Skew Stickiness Ratio')
            eps = Constants.ONE_PERCENT
            lft = mth.log (Constants.ONE_PERCENT)
            rgt = mth.log (10)
            dt = 2 * Constants.ONE_WEEK
            dx = Constants.ONE_PERCENT
            twice_dx = 2 * dx 
            pde_lft = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt), eps=-eps).run (mat)
            pde_rgt = ForwardPartialDifferentialEquation (self.loc_vol, dt, dx, (lft, rgt), eps=+eps).run (mat)
            for state_lft, state_rgt in zip (pde_lft.hist, pde_rgt.hist):
                mat, log_fwd_mnn_lft, prices_lft = state_lft.get_attribute ()
                mat, log_fwd_mnn_rgt, prices_rgt = state_rgt.get_attribute ()
                if mat > Constants.MINIMUM_MATURITY:
                    idx_lft, idx_rgt = find_index (log_fwd_mnn_lft)
                    price_lft = 0.5 * (prices_lft [idx_lft] + prices_lft [idx_rgt])
                    idx_lft, idx_rgt = find_index (log_fwd_mnn_rgt)
                    price_rgt = 0.5 * (prices_rgt [idx_lft] + prices_rgt [idx_rgt])
                    tot_var_lft = get_at_the_money_implied_total_variance (price=price_lft, spot=1-eps)
                    tot_var_rgt = get_at_the_money_implied_total_variance (price=price_rgt, spot=1+eps)
                    vol_lft = get_volatility (tot_var_lft, mat)
                    vol_rgt = get_volatility (tot_var_rgt, mat)
                    ssr = (vol_rgt - vol_lft) / twice_dx
                    plt.scatter (mat, ssr, color='black', marker='+')
            plt.show ()

        

        
        
        