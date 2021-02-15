import numpy as np
from collections import Counter
from peakutils import peak
from struct import unpack
import math
import os

import pyhrv.time_domain as td
from pyhrv import tools
from scipy import stats
from VSRstats.frequency_domain import frequency_domain

class time_domain:
    
    def __init__(self, data):

        if type(data) == list:
            data = np.array(data)
        if type(data) == np.ndarray:
            self.stats = (self._computeSignal(data) if
                           data.ndim == 1 else self._computeSignals(data))
        else:
            raise TypeError('Signal should be an np.ndarray')

    def _computeSignals(self, signals):
        return np.array([self.computeSignal(s) for s in signals])

    def _cv(self, sdnn, hr_mean):
        return (sdnn / hr_mean) * 100

    def _cc1(self, sdnn, hr_mean):
        return (sdnn / hr_mean) * 100
    
    def _computeSignal(self, signal):
        obj = {}

        # Best min_dist & thres for sphygmogram signal
        peaks = peak.indexes(signal, min_dist=56, thres=0.16)
        
        # Ignore un normal signls (with no peaks)
        if(len(peaks) == 0): return obj
            
        nn = tools.nn_intervals(peaks)
        
        # Ignore un normal signls (with no NN)
        if(len(nn) == 0): return

        # Standard
        obj = dict(td.nni_parameters(nn, peaks), **obj)
        obj = dict(td.nni_differences_parameters(nn, peaks), **obj)
        obj = dict(td.sdnn(nn, peaks), **obj)
        obj = dict(td.sdnn_index(nn, peaks), **obj)
        obj = dict(td.sdann(nn, peaks), **obj)
        obj = dict(td.rmssd(nn, peaks), **obj)
        obj = dict(td.sdsd(nn, peaks), **obj)
        obj = dict(td.nn50(nn, peaks), **obj)
        obj = dict(td.nn20(nn, peaks), **obj)
        obj = dict(td.geometrical_parameters(nn, peaks, plot=False), **obj)
        del obj['nni_histogram']
        
        # Additional
        obj = dict({'cv': self._cv(obj['sdnn'], obj['nni_mean'])}, **obj)

        peaks_diff = tools.nni_diff(peaks)
        obj = dict({'MxDMn': max(peaks_diff) - min(peaks_diff)}, **obj)
        obj = dict({'MxRMn': max(peaks_diff) / min(peaks_diff)}, **obj)
        obj = dict({'Mo': stats.mode(peaks_diff)[0][0]}, **obj)

        counter = Counter(peaks_diff)
        idx = list(counter.keys()).index(obj["Mo"])
        obj = dict({'AMo': list(counter.values())[idx]}, **obj)
        obj = dict({'SI': obj['AMo']/(2*obj['Mo']*obj['MxDMn'])}, **obj)

        # Autocorrelation function

        # Frequency stats
        welch = frequency_domain(signal).stats['welch']['params']
        bands = list(welch['fft_bands'].keys())

        obj = dict({'TP': welch['fft_total']}, **obj)
        
        obj = dict({'HF': welch['fft_rel'][bands.index('hf')]}, **obj)
        obj = dict({'LF': welch['fft_rel'][bands.index('lf')]}, **obj)
        obj = dict({'VLF': welch['fft_rel'][bands.index('vlf')]}, **obj)
        obj = dict({'ULF': welch['fft_rel'][bands.index('ulf')]}, **obj)
        
        obj = dict({'HFav': welch['fft_abs'][bands.index('hf')]}, **obj)
        obj = dict({'LFav': welch['fft_abs'][bands.index('lf')]}, **obj)
        obj = dict({'VLFav': welch['fft_abs'][bands.index('vlf')]}, **obj)
        obj = dict({'ULFav': welch['fft_abs'][bands.index('ulf')]}, **obj)
        
        obj = dict({'(LF/HF)av': obj['LFav'] / obj['HFav']}, **obj)
        obj = dict({'IC': obj['LF'] / obj['VLF']}, **obj)

        for k in obj:
            if(math.isnan(obj[k])):
                obj[k] = 0;
        
        return obj
