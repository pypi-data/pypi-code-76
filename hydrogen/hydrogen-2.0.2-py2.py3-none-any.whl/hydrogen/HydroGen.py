#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HydroGen methods to generate (stochastic) domestic hot water events.

author: Bruno Hadengue, bruno.hadengue@eawag.ch

Documentation Update: 30th May 2019.
"""

from argparse import ArgumentParser
import hydrogen.tools.tools as tt
from hydrogen.EventClass import event
import hydrogen.tools.methodChoice as mc
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time
from functools import wraps


def timerFunction(orig_func):

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result
    return wrapper

def eventGeneration(nbEvents, eventType, df_freq, totSimTime, startTime, timeDiff):
    """
    Returns a list containing generated events of class ``event``. If an overlap is found, i.e. if ``Tools.tools.is_Overlap`` returns "True", the algorithm tries again until a free spot is found.

    Args:
        * nbEvents (bool): number of events to be generated. Usually the return value of ``HydroGen.nbEventsChoice``
        * eventType (list of dicts): from initialization file.
        * df_freq (DataFrame): frequency distribution. Usually return value of ``HydroGen.readConvert_Distribution``
        * totSimTime (int): from initialization file.

    Returns:
        List of events. See corresponding class ``event``.
        New startTime.
    """
    events = []
    for n in range(nbEvents):
        if n != 0:
            eventTmp = event(eventType, df_freq, totSimTime)
            if eventTmp.startTime == 0:
                eventTmp.startTime = startTime
                startTime += events[n-1].duration + timeDiff
                if eventTmp.startTime+eventTmp.duration > totSimTime:
                    raise ValueError("One event may be overlapping the total simulation time, please avoid this in your initialisation file.")
            else:
                while tt.is_Overlap(n, events, eventTmp):
                    eventTmp = event(eventType, df_freq, totSimTime)  #repeat until non-overlapping event is found
            events.append(eventTmp)
        else:
            events.append(event(eventType, df_freq, totSimTime))
            if events[0].startTime == 0: #if startTime was now defined during event initialization
                events[0].startTime = startTime
                startTime += events[0].duration + timeDiff
                if events[0].startTime+events[0].duration > totSimTime:
                    raise ValueError("One event may be overlapping the total simulation time, please avoid this in your initialisation file.")
    return events, startTime

def readConvert_Distribution(distroFile, totSimTime, verbose):
    """
    Reads and converts the flow distribution provided in the initialization file to a frequency distribution DataFrame.
    """
    print("Reading and converting event distribution...")

    if distroFile.fileName == "None":
        df, df_seconds, df_freq = pd.DataFrame(), pd.DataFrame(), pd.DataFrame() #empty DataFrames.
        try:
            startTime, timeDiff = distroFile.startTime, distroFile.timeDiff
        except AttributeError:
            raise AttributeError("startTime or timeDiff could not be found, please check initFile")
    else:
        try:
            df = tt.distroReader(distroFile.fileName, distroFile.skip_rows, distroFile.use_cols)
        except ValueError:
            raise Exception("distroFile could not be read, please check 'fileName', 'skip_rows', 'skip_cols'.")

        if verbose:
            print(df)

        try:
            df_seconds = tt.convert2Seconds(df, totSimTime)
            df_freq = tt.Flow2Freq(df_seconds)
        except:
            raise Exception("Conversion went bananas. Please check distroFile.")

        startTime, timeDiff = None, None

    return df, df_seconds, df_freq, startTime, timeDiff

def nbEventsChoice(df, eventType, nbInhabitants):
    """
    Samples the number of events based on the information provided in the ``nbEvent`` key of the ``eventType`` list in the initialization file.
    """
    method = getattr(mc, 'method_nb_{}'.format(eventType.nbEvents.method)) #call method from methodChoice.py method repository
    return method(df, eventType, nbInhabitants)

def eventLoop(df, df_freq, d, startTime, timeDiff):
    """
    Generates the events by calling ``HydroGen.eventGeneration`` and returns the resulting hydrograph: ``flowDf``
    """

    def internalLoop(df, df_freq, d, simDay, startTime, timeDiff):
        """
        Internal Loop: Calls nbEventsChoice and eventGeneration for each type (or usage) and
        produces the resulting flow. Summarizes the results in withdrawVolumes dataframe.
        """
        for eventType in d.eventList:
            nbEvents = nbEventsChoice(df, eventType, d.nbInhabitants)
            print("\t{} - {}: {} events...".format(eventType.type, eventType.usage, nbEvents))
            events, startTime = eventGeneration(nbEvents, eventType, df_freq, d.totSimTime, startTime, timeDiff)

            for e in events:
                flowDf.loc[(e.startTime + (simDay - 1) * d.totSimTime):e.startTime + (simDay - 1) * d.totSimTime + e.duration - 1, 'flow'] += e.flow
                flowDf.loc[e.startTime + (simDay - 1) * d.totSimTime:e.startTime + (simDay - 1) * d.totSimTime + e.duration - 1, 'temp'] += e.temperature # -1 because otherwise another second of flow is added, introducing errors in the total withdrawn volume
                withdrawVolumes[eventType.usage].loc[simDay - 1] += e.volume
                try:
                    if d.operationEnergy=="True":
                        flowDf.loc[e.startTime:e.startTime+e.duration-1, 'opEn'] += e.operationEnergy
                except AttributeError:
                    pass #operationEnergy not defined in initFile, do as if nothing happened
                except:
                    raise Exception("Problem occurred when sampling the operation energy. Please check initFile")

        return events, withdrawVolumes, startTime

    print("Generating events...")

    #check if all eventTypes are found in distroFile
    if d.distroFile.fileName != "None":
        if sum([d.eventList[i].type in df.columns for i in range(len(d.eventList))])!=len(d.eventList):
            raise ValueError("among the types {}, one or more could not be found in distroFile".format([d.eventList[i].type for i in range(len(d.eventList))]))
        else:
            pass
    else:
        pass

    flowDf = pd.DataFrame()
    flowDf['flow'] = pd.Series(np.zeros(d.totSimTime*d.simDays))
    flowDf['temp'] = pd.Series(np.zeros(d.totSimTime*d.simDays))
    try:
        if d.operationEnergy=="True":
            flowDf['opEn'] = pd.Series(np.zeros(d.totSimTime))
    except AttributeError:
        pass


    cols = [eventType.usage for eventType in d.eventList] #list made of different event types: 'Shower', 'WC', etc.
    withdrawVolumes = pd.DataFrame(np.zeros((d.simDays, np.size(cols))), columns=cols)

    if d.simDays > 1:
        i = 1
        while i <= d.simDays: #number of simulation days
            print("Day #{}".format(i))
            events, withdrawVolumes, startTime = internalLoop(df, df_freq, d, i, startTime, timeDiff)

            i += 1
    else:
            events, withdrawVolumes, startTime = internalLoop(df, df_freq, d, 1, startTime, timeDiff)

    withdrawVolumes = withdrawVolumes.append(withdrawVolumes.mean(axis=0), ignore_index=True)
    return flowDf, withdrawVolumes
