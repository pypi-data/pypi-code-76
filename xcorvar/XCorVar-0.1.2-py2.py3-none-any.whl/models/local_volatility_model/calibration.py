# coding: utf-8

import numpy as np

from matplotlib import pyplot as plt

from sample.toolbox.automatic_differentiation.hyper_data import HyperFunction
from sample.toolbox.mathbox import protected_sqrt

class SpotCalibration:

    def __init__ (self, data):
        self.data = data 

    def run (self):
        print ("==> Local Volatility Model Calibration (spot) processing ...")
        spot = self.data.mid
        print ("==> Spot calibrated.")
        return spot 

class ForwardCalibration:

    def __init__ (self, fwd):
        self.fwd = fwd

    def run (self):
        print ("==> Local Volatility Model Calibration (forward) processing ...")
        fwd = self.fwd
        print ("==> Forward calibrated.")
        return fwd

class LeverageSurfaceCalibration:

    def __init__ (self, volatility_surface):
        self.hyper_total_variance_function = HyperFunction (volatility_surface)
        #self.volatility_surface = volatility_surface

    def run (self):
        print ("==> Local Volatility Model Calibration (Leverage Surface) processing ...")

        def local_volatility_function (mat, log_fwd_mnn):
            w = self.hyper_total_variance_function (mat, log_fwd_mnn)
            t = mat
            k = log_fwd_mnn
            f_k = w.val
            df_k = w.grad [0] [1]
            df_kk = w.hess [1] [1]
            df_t = w.grad [0] [0]
            up = df_t
            down = (0.5 * k / f_k * df_k - 1) ** 2 + 0.5 * df_kk - 0.25 * (0.25 + 1 / f_k) * df_k ** 2
            return protected_sqrt (up, down)
        
        #from toolbox.black_scholes_functions import black_scholes_call_price
        #from constants import Const
        #dt = Const.ONE_DAY
        #dk = Const.ONE_BP
        #sq_dk = dk * dk
        #twice_dk = 2 * dk
        #def loc_vol_func (t, k):
        #    rk = k+dk
        #    lk = k-dk
        #    rt = t+dt
        #    ptk = black_scholes_call_price (k, self.volatility_surface (t, k))
        #    prtk = black_scholes_call_price (k, self.volatility_surface (rt, k))
        #    ptrk = black_scholes_call_price (rk, self.volatility_surface (t, rk))
        #    ptlk = black_scholes_call_price (lk, self.volatility_surface (t, lk))
        #    df_t = (prtk - ptk) / dt
        #    df_k = (ptrk - ptlk) / twice_dk
        #    df_kk = (ptrk - 2 * ptk + ptlk) / sq_dk
        #    up = 2 * df_t
        #    down = df_kk - df_k
        #    return protected_sqrt (up, down)
        
        print ("==> Leverage surface calibrated.")
        return LeverageSurface (local_volatility_function)

class LeverageSurface:

    def __init__ (self, loc_vol_func):
        self.loc_vol_func = loc_vol_func

    def __call__ (self, mat, log_fwd_mnn):
        return self.loc_vol_func (mat, log_fwd_mnn)

    def plot (self, mat_min=0.1, mat_max=1, size_mat=100, log_fwd_mnn_min=-0.5, log_fwd_mnn_max=0.5, size_log_fwd_mnn=100):
        fig = plt.figure ()
        axes = plt.axes (projection='3d')
        mats = np.linspace (mat_min, mat_max, size_mat)
        log_fwd_mnns = np.linspace (log_fwd_mnn_min, log_fwd_mnn_max, size_log_fwd_mnn)
        grid = np.array ([[self (mat, log_fwd_mnn) for log_fwd_mnn in log_fwd_mnns] for mat in mats])
        surf = axes.plot_surface (*np.meshgrid (log_fwd_mnns, mats), grid)
        fig.colorbar (surf, shrink=0.5, aspect=10)
        plt.show ()





            
            
