import numpy as np
import matplotlib.pyplot as plt
from peakutils import peak
from struct import unpack
import math
import os
from pyhrv import tools
import biosppy

import pyhrv.frequency_domain as fd

class frequency_domain:
    
    def __init__(self, data):

        self.bands = {'ulf': (0.0, 0.015),
                     'vlf':(0.015, 0.04),
                     'lf':(0.04, 0.15),
                     'hf':(0.15, 0.4) }

        if type(data) == list:
            data = np.array(data)
            
        if type(data) == np.ndarray:

            self.stats = (self._computeSignal(data) if
                           data.ndim == 1 else self._computeSignals(data))
            
        else:
            raise TypeError('Signal should be an np.ndarray')

    def _welch_psd(self, nni, peaks):
        params, freq, power = fd.welch_psd(nni=nni, fbands=self.bands,
                                  rpeaks=peaks, show=False, mode='dev')
        
        _, freq_i = fd._compute_parameters('fft', freq, power, self.bands)
        
        return {'params': dict(params.as_dict()), 'freq': freq,
                'power': power / 10**6, 'freq_i': freq_i}
    
    def _lomb_psd(self, nni, peaks):
        params, freq, power = fd.lomb_psd(nni=nni, fbands=self.bands,
                                  rpeaks=peaks, show=False, mode='dev')
        
        _, freq_i = fd._compute_parameters('lomb', freq, power, self.bands)
        
        return {'params': dict(params.as_dict()), 'freq': freq,
                'power': power / 10**6, 'freq_i': freq_i}
    
    def _ar_psd(self, nni, peaks):
        params, freq, power = fd.ar_psd(nni=nni, fbands=self.bands,
                                  rpeaks=peaks, show=False, mode='dev')
        
        _, freq_i = fd._compute_parameters('ar', freq, power, self.bands)
        
        return {'params': dict(params.as_dict()), 'freq': freq,
                'power': power / 10**6, 'freq_i': freq_i}

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

        welch = {'welch': self._welch_psd(nn, peaks)}
        lomb = {'lomb': self._lomb_psd(nn, peaks)}
        ar = {'ar': self._ar_psd(nn, peaks)}
        
        obj['welch'] = self._walk_over(welch, 'welch')
        obj['lomb'] = self._walk_over(lomb, 'lomb')
        obj['ar'] = self._walk_over(ar, 'ar')
        
        return obj

        
