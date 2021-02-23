#!/usr/data/env python3
# -*- coding: utf-8 -*-
"""
Tools for the handling of input and output files for the HydroGen module.

author: Bruno Hadengue, bruno.hadengue@eawag.ch

Documentation Update: 4th Feb 2019.
"""

#import random as rd
import pandas as pd
import bisect as bs
import numpy as np
#import configparser as cp
import json
from collections import namedtuple
from matplotlib import pyplot as plt

# def truncDistSampling(dist, args, lower, upper, discretization):
#     """
#     dist is a scipy.stats distribution, for instance stats.lognorm, lower and upper are boundaries. Method seen in https://stackoverflow.com/questions/11491032/truncating-scipy-random-distributions
#     """
#     try:
#         cdfUpper = dist.cdf(upper)
#         cdfLower = dist.cdf(lower)
#         x =


def cfdRandomPick(df, probDistro, pickValues):
    """
    cfdRandomPick applies a Cumulative Frequency Distribution algorithm to a Dataframe containing the 'probDistro' column and the 'pickValues' column. It essentially picks up a value from pickValues according the the probDistro probability distribution. probDistro and pickValues are strings, but pickValues can also be 'index'. 'event' is an object from the EventClass.
    WARNING: probDistro must be normalized s.t. sum(probDistro) = 1 !!
    """
    ri = bs.bisect_left(df[probDistro].cumsum(), np.random.rand())
    if pickValues != 'index':
        return df.loc[ri,pickValues]
    else:
        return ri

def distroReader(xlsFile, skiprowsList, usecolsKey):
    """
    Read an xls file containing flow distributions.

    Returns:
        DataFrame
    """
    if usecolsKey == "":
        return pd.read_excel(xlsFile, sheet_name=0, header=0, skiprows=skiprowsList, index_col=0, converters={0:np.rint})
    else:
        return pd.read_excel(xlsFile, sheet_name=0, header=0, skiprows=skiprowsList, index_col=0, usecols=usecolsKey, converters={0:np.rint})

def convert2Seconds(df, totSimTime):
    """
    requires prior conversion to time index in seconds.

    Returns:
        New dataframe resolved to the second, with flows converted accordingly.
    """
    # df_seconds = pd.DataFrame(columns=df.columns, index=np.arange(totSimTime))

    if df.index.is_monotonic_increasing:
        df_seconds = df.reindex(list(range(np.int(df.index.min()), totSimTime)), fill_value=0, method='ffill')
        #print(df_seconds)
        for i in df.index:  #convert to "per seconds" all flow values
            i = np.int(i)
            if i > totSimTime or i < 0:
                raise Exception("The flow file is out of bounds. Make sure the time column is within [0,%i]" %(totSimTime))
            if i==0:
                i_tmp = i
            else:
                diff = np.rint(abs(i-i_tmp))
                df_seconds.loc[i_tmp:i-1] /= diff
                i_tmp = i

        df_seconds.loc[i_tmp:] /= (totSimTime-i_tmp)

    else:
        raise Exception("Time indices of distroFile is not monotonic increasing. Please check.")

    return df_seconds

def Flow2Freq(df_seconds):
    """
    Returns:
        Dataframe where average flows were converted to frequencies.
    """
    df_freq = df_seconds.copy()
    for column in df_freq.columns:
        df_freq[column] = df_freq[column]/df_freq[column].sum()
    return df_freq


def is_Overlap(n, events, eventTmp):
    """
    Returns:
        True if 'eventTmp' is overlapping with any event in 'events'
    """
    for i in range(n):
        if events[i].startTime <= eventTmp.startTime <= events[i].startTime+events[i].duration:
            return True
        elif eventTmp.startTime <= events[i].startTime <= eventTmp.startTime+eventTmp.duration:
            return True
    return False

def conversion_Modelica(flowTableFile, totSimTime, simdays, numberColumns):
    """
    Used to convert existing csv files `flowTableFile` to a format read by Modelica simulation
    environments. Number of columns = 3 (time index, flow, temperature)
    """
    with open(flowTableFile, "r") as inpf:
        lines = inpf.readlines()
        lines[0] = "#1\nfloat FlowTable({:.0f}, {:.0f})\n".format(totSimTime*simdays, numberColumns+1)

    with open(flowTableFile, "w") as outf:
       outf.writelines(lines)
    print("\nExported successfully to file %s and converted to Modelica format." %flowTableFile)
    return


def initRead(initFile):
    """
    initRead is used to retrieve useful variables from the file `initFile` set
    by the user. Various variables and distribution settings are forwarded to
    the main script using this function.

    Returns:
        object-like version of the `initFile`, and values can be accessed through

            * d.totSimTime
            * d.eventList[0].type
            * d.distroFile.fileName
            * etc.
    """
    with open(initFile, 'r') as f:
        return json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def plot_flowDf(flowDf, df_freq, showBool, freqBool, ax, type):    #showBool is just a bool to show the plot or not Necessary to account for calls from GUI or script.
    """
    called when `-p` option is used in the command line. Plots the generated hydrograph and the corresponding frequency distribution.
    """
    ax.cla()
    plot1=flowDf.reset_index().plot(x='index',y='flow', ax=ax, legend=True, color='blue', label='Flow curve')

    # plot other things on secondary y axis - if `freqBool` is set to True
    df_freq = pd.concat([df_freq] * int(len(flowDf) / (3600 * 24)), ignore_index=True) # Duplicate df_freq repetitively
    if freqBool:
        plot2 = df_freq.reset_index().plot(x='index', y=type, ax=ax, legend=True, secondary_y=True, mark_right=False, alpha=0.5, color='lightgreen', label= 'Frequency curve')
        ax.right_ax.set_ylabel('Frequency')

    ax.set_ylabel("Flow [L/s]")    #ax.right_ax.set_ylim([0,1])
    ax.set_xlabel("Time [hours]")

    ## Seconds to hour conversion in plot ticks
    xticks = []
    xticksLabels = []
    for i in range(0, int(len(flowDf)/3600) + 1, int(len(flowDf)/86400)):
        xticks.append(i * 3600)
        xticksLabels.append(i)

    ax.xaxis.set_ticks(xticks)
    ax.set_xticklabels(xticksLabels)

    if showBool: #useful when working with the same plotting function for GUIs and scripts.
        plt.show()
    return 0
