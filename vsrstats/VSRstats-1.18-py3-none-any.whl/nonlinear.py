import numpy as np
import matplotlib.pyplot as plt
from peakutils import peak
from struct import unpack
import biosppy
import math
import os

from pyhrv import tools
from pyhrv.nonlinear import poincare
from statsmodels.tsa import stattools
import matplotlib as mpl

class nonlinear:
    
    def __init__(self, data):

        if type(data) == list:
            data = np.array(data)
            
        if type(data) == np.ndarray:

            self.stats = (self._computeSignal(data) if
                           data.ndim == 1 else self._computeSignals(data))
            
        else:
            raise TypeError('Signal should be an np.ndarray')

    def _poincare(self, nn, peaks):
        res = poincare(nni = nn, rpeaks = peaks, show=False)
        nn_mean = np.mean(nn)
        sd1, sd2 = res['sd1'], res['sd2']
        ellipse = mpl.patches.Ellipse((nn_mean, nn_mean), sd1 * 2, sd2 * 2, angle=-45, fc='k', zorder=1)
        ellipse = ellipse.get_verts()
        ellipse = {'x': ellipse[:,0], 'y': ellipse[:,1]}
        obj = {'sd1': res['sd1'], 'sd2': res['sd2'], 'ellipse': ellipse}
        return obj

    def _ACF(self, signal, lags):
        nlags = lags;
        lags = np.arange(nlags)
        
        acf_x, conflict = stattools.acf(signal, nlags=nlags,
                                        alpha=0.005, fft=False, 
                                        adjusted=False, missing = "none")
        
        return {'lags': lags, 'acf_x': acf_x[lags]}

    def _walk_over(self, obj, key):
        
        keys = []

        if(type(obj[key]) == biosppy.utils.ReturnTuple
           or type(obj[key]) == dict):
            keys = obj[key].keys()
            
        if len(keys) == 0:
            if(type(obj[key]) == biosppy.utils.ReturnTuple):
                return obj[key].as_dict()
            
            elif(type(obj[key]) == np.ndarray):
                return list([i.item() for i in obj[key]])

            else:
                return obj[key]

        res = {}
        for k in keys:
            res[k] = self._walk_over(obj[key], k)
        return res
    
    def _computeSignals(self, signals):
        return np.array([self.computeSignal(s) for s in signals])    

    def _computeSignal(self, signal):
        obj = {}

        # Best min_dist & thres for sphygmogram signal
        peaks = peak.indexes(signal, min_dist=56, thres=0.16)
        
        # Ignore un normal signls (with no peaks)
        if(len(peaks) == 0): return obj
            
        nn = tools.nn_intervals(peaks)
        
        # Ignore un normal signls (with no NN)
        if(len(nn) == 0): return

        # Poincare method
        poincare = {'poincare': self._poincare(nn, peaks)}
        obj['poincare'] = self._walk_over(poincare, 'poincare')

        # ACF
        acf = {'ACF': self._ACF(signal, int(len(signal)/2))}
        obj['ACF'] = self._walk_over(acf, 'ACF')
        
        return obj

        
