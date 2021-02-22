#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line script for the generation of domestic hot water hydrographs.

author: Bruno Hadengue, bruno.hadengue@eawag.ch

Documentation Update: 30th May 2019.
"""

from argparse import ArgumentParser
from hydrogen.HydroGen import readConvert_Distribution, eventLoop
import hydrogen.tools.tools as tt
import pandas as pd
from matplotlib import pyplot as plt

def main():
    #parsers and co.
    parser = ArgumentParser(description="Stochastic Process for the generation of Domestic Hot Water hydrographs.")
    parser.add_argument("initFile", type=str, help="Only mandatory argument, the path to the initialisation file, that contains all user-given information. See documentation for file format")
    parser.add_argument("-v", "--verbose",action="store_true", dest="verbose", default=False,
                      help="prints the content of input files as tables")
    parser.add_argument("-p", "--plot", action="store_true", dest="plot", default=False,
                     help="plots the resulting flow graph")
    parser.add_argument("-o", "--outputFile", dest="outputFile", help="Output Filename (.csv)")
    args = parser.parse_args()

    #Read init file and set variables
    d = tt.initRead(args.initFile)

    #Reading and converting the file given as input by user
    df, df_seconds, df_freq, startTime, timeDiff = readConvert_Distribution(d.distroFile, d.totSimTime, args.verbose)

    #event creation using eventLoop
    flowDf, withdrawVolumes = eventLoop(df, df_freq, d, startTime, timeDiff)
    if args.verbose:
        print(flowDf)

    #Printing events summary
    print("\n\nSummary of generated events: daily withdrawn volumes [L] (Last entry is daily average flows)")
    print(withdrawVolumes)

    #%% Plotting if required
    if args.plot:
        fig=plt.figure(figsize=(10, 4))
        ax = fig.add_subplot(111)
        try:
            tt.plot_flowDf(flowDf, df_freq, True, True, ax, d.eventList[0].type)
        except:
            tt.plot_flowDf(flowDf, df_freq, True, False, ax, d.eventList[0].type)

    # Printing to output file if present
    if args.outputFile:
        try:
            if d.operationEnergy == "True":
                flowDf.to_csv(args.outputFile, columns=['flow', 'temp', 'opEn'])
            else:
                flowDf.to_csv(args.outputFile, columns=['flow', 'temp'])
        except AttributeError: #do as if nothing happened
            flowDf.to_csv(args.outputFile, columns=['flow', 'temp'])
        tt.conversion_Modelica(args.outputFile, d.totSimTime, d.simDays, len(flowDf.columns))

if __name__=='__main__':
    main()
