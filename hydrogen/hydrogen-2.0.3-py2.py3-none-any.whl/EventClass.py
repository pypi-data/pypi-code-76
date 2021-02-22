#!/usr/data/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
Event Class. Creates events based on (stochastic) parameters passed from HydroGen methods.

author: Bruno Hadengue, bruno.hadengue@eawag.ch

Documentation Update: 30th May 2019.
"""


import pandas as pd
import numpy as np
import hydrogen.tools.tools as tt
import hydrogen.tools.methodChoice as mc
from scipy.stats import truncnorm, lognorm

class event:
    """
    startTime, flow and volume are picked as soon as the event is initiated using the corresponding methods.
    """
    def __init__(self, eventType, df_freq, totSimTime):
        #check if type is in columns
        self.type = eventType.type
        self.flowDist = eventType.flowDist
        self.volumeDist = eventType.volumeDist
        self.tempDist = eventType.tempDist
        self.df_freq = df_freq
        self.startTime = self.timeChoice()

        self.approxFlow = self.distSample(self.flowDist)
        self.volume = self.distSample(self.volumeDist)
        self.temperature = self.distSample(self.tempDist)
        self.duration, self.flow = self.eventDurationFlowAdapt()

        #test for operationEnergy and sample if present
        try:
            self.opEnDist = eventType.opEnDist
            #opEnDist samples for the energy necessary for 1 event. The energy/second is computed by dividing with the duration
            self.operationEnergy = self.distSample(self.opEnDist)/self.duration
        except:
            pass

    def timeChoice(self):
        """
        Randomly samples for an event starting time using a cumulative frequency distribution method.

        Returns:
            integer
        """
        if self.df_freq.empty:
            return 0
        else:
            return tt.cfdRandomPick(self.df_freq, self.type, 'index')

    def eventDurationFlowAdapt(self):
        """
        Adapts the flow such that the duration*flow = total volume of the event.

        Returns:
            float
        """
        # print("flow adapted from {} to {}".format(self.approxFlow, self.volume/np.round(self.volume/self.approxFlow)))
        return np.round(self.volume/self.approxFlow), self.volume/np.round(self.volume/self.approxFlow)

    def eprint(self):
        """
        Pretty print of event properties
        """
        return print("(%f, %f, %f, %f, %f)" %(self.startTime,self.flow, self.duration, self.volume, self.temperature))

    def distSample(self, dist):
        """
        Samples from distributions as given by the initialization file. Calls method from the MethodChoice module.

        Returns:
            float
        """
        try:
            method = getattr(mc, 'method_dist_{}'.format(dist.dist)) #call method from methodChoice.py method repository
            return method(dist)
        except AttributeError:
            raise AttributeError("Error in initFile for distribution '{}', sampling process went bananas".format(dist))
