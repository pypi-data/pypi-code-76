import numpy as np
import matplotlib.pyplot as plt
from peakutils import peak
from struct import unpack
import math
import os

import pyhrv.tools as tools
from pyhrv.time_domain import time_domain

# Util for display peaks on signal
def showPeaks(signal):
    peaks = getPeaks(signal);
    fig = plt.figure(figsize=(30, 3))
    plt.scatter(x=peaks, y=[signal[j] for j in peaks],
                            color='red', marker = '*')
    plt.plot(signal)
    plt.show()

# func to get peaks of signal
def getPeaks(signal):
    return peak.indexes(signal, min_dist=56, thres=0.16)

# Read signal from file
def loadSignal(filepath):
    
    file = open(filepath, "rb").read()
    ufile = unpack('10000H', file)
    arr = np.array(ufile)
    
    return arr

#
    
class VSR:
    
    def __init__(self, data):

        if type(data) == list:
            self.data = data = np.array(data)
            
        if type(data) == np.ndarray:
            buffer = {}
            self.stats = (self.computeSignal(data) if
                           data.ndim == 1 else self.computeSignals(data))
            for k in self.stats:
                if(math.isnan(self.stats[k])):
                    continue
                else:
                    buffer[k] = self.stats[k];
            self.stats = buffer
        else:
            raise TypeError('Signal should be an np.ndarray')

    def computeSignals(self, signals):
        return np.array([self.computeSignal(s) for s in signals])

    def computeSignal(self, signal):
        obj = {}

        # Best min_dist & thres for sphygmogram signal
        peaks = peak.indexes(signal, min_dist=56, thres=0.16)
        
        # Ignore un normal signls (with no peaks)
        if(len(peaks) == 0): return obj
            
        self.nn = tools.nn_intervals(peaks)
        
        # Ignore un normal signls (with no NN)
        if(len(self.nn) == 0): return obj
            
        stats = time_domain(nni=self.nn, rpeaks=peaks, # Compute VSR stats
                                        plot=False, show=False)
        for k in stats.keys():
            if k == 'nni_histogram': continue 
            obj[k] = stats[k]

        return obj
        
