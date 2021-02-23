# coding: utf-8

import math as mth
import numpy as np

import scipy.stats as sps

from sample.toolbox.black_scholes_functions import get_d1_d2
from sample.toolbox.integral.functionnal_integral import Integral

class SpotCalibration:

    def __init__ (self, data):
        '''
        Calibration of spot

        :param {'bid': _, "ask": _, 'mid': _} data: spot data
        '''
        self.data = data 

    def run (self):
        '''
        Calibrate the spot

        :return float: mid spot
        '''
        print ("==> Black Scholes Term Sctructure Model Calibration (spot) processing ...")
        spot = self.data.mid
        print ("==> Spot calibrated.")
        return spot 

class ForwardCalibration:

    def __init__ (self, fwd):
        '''
        Calibration of forward

        :param FwdData fwd: forward data
        '''
        self.fwd = fwd

    def run (self, mat):
        '''
        Calibrate the forward

        :param float mat: maturity
        :return float: mid forward at maturity mat
        '''
        print ("==> Black Scholes Term Sctructure Model Calibration (forward) processing ...")
        fwd = self.fwd (mat)
        print ("==> Forward calibrated.")
        return fwd

class TotalVarianceCalibration:

    def __init__ (self, volatility_surface, dsc_repo=1):
        '''
        Total variance calibration

        :param VolInter vol_inter: interpolated volatility surface
        :param VolInter repo: discounted repo factor
        '''
        self.volatility_surface = volatility_surface
        self.dsc_repo = dsc_repo

    def run (self, mat, prec=1e-4, fwd_mnn_lft=50, fwd_mnn_rgt=150):
        '''
        Calibrate total variance

        :param float mat: maturity
        :param float prec: integral computation accuracy
        :param float fwd_mnn_lft: left bound of integral
        :param float fwd_mnn_rgt: right bound of integral
        :return float: implied total variance of log contract at maturity mat
        '''
        print ("==> Black Scholes Term Sctructure Model Calibration (total variance) processing ...")
        lft_bound = mth.log (fwd_mnn_lft / 100)
        rgt_bound = mth.log (fwd_mnn_rgt / 100)
        def put_like (log_fwd_mnn):
            fwd_mnn = np.exp (log_fwd_mnn)
            tot_var = self.volatility_surface (mat, log_fwd_mnn)
            tot_vol = np.sqrt (tot_var)
            d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
            return self.dsc_repo * (sps.norm.cdf (-d2) - sps.norm.cdf (-d1) / fwd_mnn)
        def call_like (log_fwd_mnn):
            fwd_mnn = np.exp (log_fwd_mnn)
            tot_var = self.volatility_surface (mat, log_fwd_mnn)
            tot_vol = np.sqrt (tot_var)
            d1, d2 = get_d1_d2 (log_fwd_mnn, tot_vol)
            return self.dsc_repo * (sps.norm.cdf (d1) / fwd_mnn - sps.norm.cdf (d2)    )
        put_integral = Integral (func=put_like, lft=lft_bound, rgt=0).run (eps=prec).curr.val
        call_integral = Integral (func=call_like, lft=0, rgt=rgt_bound).run (eps=prec).curr.val
        integral = put_integral + call_integral
        log_ctr_tot_var = 2 * integral
        print ("==> Total variance calibrated.")
        return log_ctr_tot_var