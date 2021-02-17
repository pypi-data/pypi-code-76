import os
import numpy as np
import pandas as pd
from dataclasses import dataclass, asdict
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
import steam_nb_api.ledet.ParameterSweep

def RunSimulations(LEDETFolder, LEDETExe, MagnetName, Simulations = 'All', RunSimulations = False):
    ExcelFolder = LEDETFolder + "//LEDET//" + MagnetName + "//Input//"
    StartFile = LEDETFolder + "//startLEDET.xlsx"
    SimNumbers = []

    #1. Prepare everything
    if(Simulations=='All'):
        items = os.listdir(ExcelFolder)
        for item in items:
            if item.startswith(MagnetName) and item.endswith('.xlsx'):
                if ".sys" not in item:
                    num = item.replace('.xlsx', '')
                    num = num.replace(MagnetName+'_', '')
                    num = int(num)
                    SimNumbers.append(num)
    else:
        SimNumbers = Simulations

    df = pd.read_excel(StartFile, header=None)
    df.rename(columns={0: 'a', 1: 'b', 2: 'c'}, inplace=True)
    df.loc[df['b'] == 'currFolder', 'c'] = LEDETFolder + "\\LEDET"
    df.loc[df['b'] == 'nameMagnet', 'c'] = MagnetName
    df.loc[df['b'] == 'simsToRun',  'c'] = str(SimNumbers)
    writer = pd.ExcelWriter(StartFile)
    df.to_excel(writer, index=False, index_label=False, header=False, sheet_name='startLEDET')
    writer.save()

    #2. Run Executable
    if RunSimulations:
        os.chdir(LEDETFolder)  
        os.system(LEDETExe)
