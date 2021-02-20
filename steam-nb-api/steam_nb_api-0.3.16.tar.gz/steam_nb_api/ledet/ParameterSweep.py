import os
import numpy as np
import csv
from tqdm import trange
import sys
import pandas as pd
import itertools
from copy import deepcopy
from dataclasses import dataclass, asdict
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET

@dataclass
class QuenchSweep:
    VarToQuench: str = ""
    iStartQuench: np.ndarray = np.array([])
    ValToQuench: np.ndarray = np.array([])
    QuenchCopy: np.array = np.array([])

PossibleQuenchVar = ["tStartQuench", "lengthHotSpot_iStartQuench", "vQ_iStartQuench"]

class ParameterSweep(object):
    def __init__(self, ParametersLEDET):
        self.ParametersLEDET = ParametersLEDET
        self.ParametersToSweep = []
        self.ParameterMatrix = np.array([])
        self.SweepMatrix = np.array([])
        self.VoidRatio = np.array([])
        self.QuenchSweep = QuenchSweep()

    def _addToParameterMatrix(self, values):
        if(self.ParameterMatrix.size == 0):
            self.ParameterMatrix = values
            return
        lenNew = values.shape[1]
        lenOld = self.ParameterMatrix.shape[1]
        if(lenNew > lenOld):
            fill = np.zeros((self.ParameterMatrix.shape[0],lenNew-lenOld))
            self.ParameterMatrix = np.hstack((self.ParameterMatrix, fill))
        elif(lenNew < lenOld):
            fill = np.zeros((1, lenOld-lenNew))
            values = np.reshape(np.append(values, fill), (1, lenOld))
        self.ParameterMatrix = np.vstack((self.ParameterMatrix, values))

    def cleanParameterMatrix(self):
        self.ParameterMatrix = np.array([])
        self.__cleanParametersToSweep()

    def __cleanParametersToSweep(self):
        self.ParametersToSweep = []

    def __cleanSweepMatrix(self):
        self.SweepMatrix = np.array([])

    def generatePermutations(self):
        list_iterator = iter(self.ParameterMatrix)
        r = self.ParameterMatrix[0, :][self.ParameterMatrix[0, :] != 0]
        if self.ParameterMatrix[0, :][0] == 0:
            r = np.append([0], r)
        next(list_iterator)
        r = np.reshape(r, (r.size, 1))

        for ro in list_iterator:
            temp_mat = np.array([])
            k = ro[ro !=0]
            if(ro[0]==0):
                k = np.append([0], k)

            for l in itertools.product(r, k):
                tupleSize = np.array(l[0]).size
                if(tupleSize > 1):
                    if(temp_mat.size == 0):
                        temp_mat = np.append(l[0], l[1])
                    else:
                        temp = np.append(l[0], l[1])
                        temp_mat = np.vstack((temp_mat, temp))
                else:
                    if (temp_mat.size == 0):
                        temp_mat = np.array(l)
                    else:
                        temp_mat = np.vstack((temp_mat, np.array(l)))
            r = temp_mat
        self.SweepMatrix = r.astype(float)

    def _checkSetClass(self, Parameter):
        if Parameter in self.ParametersLEDET.Inputs.__annotations__:
            return "Inputs"
        if Parameter in self.ParametersLEDET.Options.__annotations__:
            return "Options"
        if Parameter in self.ParametersLEDET.Plots.__annotations__:
            return "Plots"
        if Parameter in self.ParametersLEDET.Variables.__annotations__:
            return "Variables"

    def _generateImitate(self, classvalue, value):
        if type(classvalue) == np.ndarray:
            v = deepcopy(classvalue)
            v = np.where(self.ParametersLEDET.Inputs.polarities_inGroup != 0, value, v)
        else:
            v = value
        return v

    def _generateImitate_Quench(self, classvalue, value):
        if type(classvalue) == np.ndarray:
            v = deepcopy(self.QuenchSweep.QuenchCopy)
            if len(self.QuenchSweep.iStartQuench.shape) > 1:
                for i in range(self.QuenchSweep.iStartQuench.shape[1]):
                    v[self.QuenchSweep.iStartQuench[int(value) -1, i]-1] = self.QuenchSweep.ValToQuench[int(value) - 1, i]
                    v[self.QuenchSweep.iStartQuench[int(value) -1, i]-1] = self.QuenchSweep.ValToQuench[int(value) - 1, i]
            else:
              v[self.QuenchSweep.iStartQuench[int(value)-1]-1] = self.QuenchSweep.ValToQuench[int(value)-2]
              v[self.QuenchSweep.iStartQuench[int(value)-1]-1] = self.QuenchSweep.ValToQuench[int(value)-2]
        return v

    def loadSweepMatrixFromExcel(self, file):
        self.__cleanSweepMatrix()
        self.__cleanParametersToSweep()
        self.cleanParameterMatrix()
        df = pd.read_excel(file, header=None, engine='openpyxl')
        first = 0
        for column in df:
            if first < 2:
                first = first +1
                continue
            cp = df[column].values
            self.ParametersToSweep = np.append(self.ParametersToSweep, cp[0])
            if first == 2:
                self.SweepMatrix = cp[1:]
                first = 3
                continue
            self.SweepMatrix = np.vstack((self.SweepMatrix, cp[1:]))
        self.SweepMatrix = self.SweepMatrix.transpose()

    def setCurrentLUT(self, currentLvl):
        LUT =  self.ParametersLEDET.Inputs.I_PC_LUT
        LUT[LUT != 0] = currentLvl
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, 'Inputs'), 'I_PC_LUT', LUT)

    def prepareSimulation(self, MagnetName, folder, cleanFolder = False,  OffsetNumber = 0, ROXIE_File = ''):
        Adjust_vQ = 0
        if ROXIE_File:
            Adjust_vQ =1
        #1a. Clean SweepMatrix
        self.__cleanSweepMatrix()
        #1b. Clean Folder
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if cleanFolder:
            filelist = [f for f in os.listdir(folder)]
            for f in filelist:
                if "selfMutualInductanceMatrix" in f: continue
                os.remove(os.path.join(folder, f))
        #2. Generate Permutations
        self.generatePermutations()
        #3. For loop for all Simulations
        toolbar_width = self.SweepMatrix.shape[0]
        file_name_stub = MagnetName
        for i in trange(self.SweepMatrix.shape[0], file=sys.stdout, desc='Excel Files'):
            file_name = folder + file_name_stub + "_" + str(i+OffsetNumber) +".xlsx"
            for j in range(self.SweepMatrix.shape[1]):
                SetClass = self._checkSetClass(self.ParametersToSweep[j])
                if self.ParametersToSweep[j] in PossibleQuenchVar:
                    if self.QuenchSweep.QuenchCopy.size == 0:
                        self.QuenchSweep.QuenchCopy = deepcopy(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]))
                    setValue = self._generateImitate_Quench(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]), self.SweepMatrix[i,j])
                else:
                    setValue = self._generateImitate(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j]), self.SweepMatrix[i,j])
                self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, SetClass), self.ParametersToSweep[j], setValue)
                if self.ParametersToSweep[j] == "I00":
                    self.setCurrentLUT(self.SweepMatrix[i,j])
                if (self.ParametersToSweep[j] == "overwrite_f_internalVoids_inGroup"):
                    setVal = self.VoidRatio - self.SweepMatrix[i, j]
                    if any(sV < 0 for sV in setVal):
                        print("Negative externalVoids calculated. Abort Sweep, please check.")
                        return
                    setVal = np.where(self.ParametersLEDET.Inputs.polarities_inGroup != 0, setVal, 0)
                    self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_externalVoids_inGroup", setVal)
            if Adjust_vQ:
                self.ParametersLEDET.adjust_vQ(ROXIE_File)

            self.ParametersLEDET.Variables.variableToSaveTxt = np.append(self.ParametersLEDET.Variables.variableToSaveTxt, 'I_CoilSections')
            self.ParametersLEDET.Variables.typeVariableToSaveTxt = np.append(self.ParametersLEDET.Variables.typeVariableToSaveTxt, 1)
            self.ParametersLEDET.Options.flag_saveMatFile = 0
            self.ParametersLEDET.Options.flag_generateReport = 0
            self.ParametersLEDET.writeFileLEDET(file_name)

        #4. Write CSV with all Parameters
        SimNumbers = np.linspace(0,self.SweepMatrix.shape[0]-1,self.SweepMatrix.shape[0])
        if SimNumbers.shape[0]>3:
            df = pd.Series(SimNumbers,index=SimNumbers)
            for i in range(self.SweepMatrix.shape[1]):
                par = pd.Series(self.SweepMatrix[:, i], index=SimNumbers)
                df = pd.concat([df, par], axis=1)
            df.columns = np.concatenate((['Simulation'], self.ParametersToSweep))
            writer = pd.ExcelWriter(folder + "SimulationMatrix.xlsx")
            df.to_excel(writer)
            writer.save()

class MinMaxSweep(ParameterSweep):
    def __init__(self, ParametersLEDET, basePoints):
        super(MinMaxSweep, self).__init__(ParametersLEDET)
        self.basePoints = basePoints

    def change_basePoints(self,basePoints):
        self.basePoints = basePoints

    def __generate_points(self, minimum, maximum, basePoints, type = 'linear'):
        if type=='linear':
            return np.array([np.linspace(minimum, maximum, basePoints)])
        if type == 'logarithmic':
            return np.array([np.logspace(minimum, maximum, num=basePoints)])

    def addParameterToSweep(self, parameter, minimum, maximum, basePoints = 0, type = 'linear'):
        if basePoints == 0:
            basePoints = self.basePoints
        self.ParametersToSweep.append(parameter)
        self.ParametersLEDET.Variables.variableToSaveTxt = np.append(self.ParametersLEDET.Variables.variableToSaveTxt,
                                                                     parameter)
        self.ParametersLEDET.Variables.typeVariableToSaveTxt = np.append(self.ParametersLEDET.Variables.typeVariableToSaveTxt,
                                                                         2)
        sweep_points = self.__generate_points(minimum, maximum, basePoints, type = type)
        self._addToParameterMatrix(sweep_points)

    def addParameterToSweep_Vector(self, parameter, vector):
        self.ParametersToSweep.append(parameter)
        self._addToParameterMatrix(np.array([vector]))

    def _activateHelium(self):
        setValue = self._generateImitate(self.ParametersLEDET.getAttribute(getattr(self.ParametersLEDET, "Inputs"),
                                                                           "polarities_inGroup"), 0)
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_internalVoids_inGroup", setValue)
        self.ParametersLEDET.setAttribute(getattr(self.ParametersLEDET, "Inputs"), "overwrite_f_externalVoids_inGroup", setValue)

    def addHeliumCrossSection(self, minHe, maxHe, basePoints = 0):
        self._activateHelium()
        cs_bare = self.ParametersLEDET.Inputs.wBare_inGroup*self.ParametersLEDET.Inputs.hBare_inGroup
        cs_ins = (self.ParametersLEDET.Inputs.wBare_inGroup +2*self.ParametersLEDET.Inputs.wIns_inGroup)* \
                (self.ParametersLEDET.Inputs.hBare_inGroup +2*self.ParametersLEDET.Inputs.hIns_inGroup)
        cs_strand = self.ParametersLEDET.Inputs.nStrands_inGroup*np.pi*(self.ParametersLEDET.Inputs.ds_inGroup**2)/4

        strand_total = cs_strand/cs_ins
        ins_total = (cs_ins - cs_bare)/cs_ins
        self.VoidRatio = (cs_bare - cs_strand)/cs_ins
        self.addParameterToSweep("overwrite_f_internalVoids_inGroup", minHe/100.0, maxHe/100.0, basePoints = basePoints)

    def addQuenchSweep(self, VarToQuench, iStartQuench, ValToQuench):
        iStartQuench = np.array(iStartQuench)
        ValToQuench = np.array(ValToQuench)
        if not iStartQuench.shape == ValToQuench.shape:
            print("Variable To Sweep and provided Values do not have same shape. Abort.")
        self.QuenchSweep.VarToQuench = np.array(VarToQuench)
        self.QuenchSweep.iStartQuench = np.array(iStartQuench)
        self.QuenchSweep.ValToQuench = np.array(ValToQuench)
        self.ParametersToSweep.append(VarToQuench)
        try:
            imitate = np.linspace(1, len(ValToQuench), len(ValToQuench))
        except:
            imitate = np.array([0])
        self._addToParameterMatrix(np.array([imitate]))

    def addCurrentSweep(self, ultimateCurrent, basePoints, current_vector = np.array([])):
        print('Warning: Current Sweep only works for FPA \n')
        if len(current_vector) == 0:
            if basePoints <= 2:
                print('Less than 3 current level provided. Set first current as level.')
                current_vector = np.array([ultimateCurrent])
            else:
                nomCurrent = self.ParametersLEDET.Options.Iref
                current_vector = np.linspace(10, ultimateCurrent, basePoints-1)
                current_vector = np.append(current_vector, nomCurrent)
        self.addParameterToSweep_Vector('I00', current_vector)

