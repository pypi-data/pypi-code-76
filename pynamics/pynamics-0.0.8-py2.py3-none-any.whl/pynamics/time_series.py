# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:49:31 2020

@author: danaukes
"""

import scipy.signal
import scipy.interpolate
import numpy
import sympy
import matplotlib.pyplot as plt

def build_smoothed_time_signal(t_given,y_given,time_series,symbol_name, window_time_width = .1,kind = 'quadratic'):
    t_step = time_series[1]-time_series[0]
    window_width = int(window_time_width/t_step)
    
    
    ft = scipy.interpolate.interp1d(t_given,y_given,'linear',fill_value='extrapolate')
    win = scipy.signal.hann(window_width)
    filtered = scipy.signal.convolve(ft(time_series), win, mode='same') / sum(win)
    ft2 = scipy.interpolate.interp1d(time_series,filtered,kind=kind,fill_value='extrapolate')
    my_signal = sympy.Symbol(symbol_name)
    return my_signal, ft2


if __name__=='__main__':
    x = [0,2,2,5,5,6,6,10]
    y = [0,0,1,1,-1,-1,0,0]
    t = numpy.r_[0:10:.01]
    my_signal, ft2 = build_smoothed_time_signal(x,y,t,window_time_width = 1)
    plt.figure()
    plt.plot(x,y)
    # plt.plot(time_series,ft(time_series))
    # plt.plot(t,filtered)
    plt.plot(t,ft2(t))
