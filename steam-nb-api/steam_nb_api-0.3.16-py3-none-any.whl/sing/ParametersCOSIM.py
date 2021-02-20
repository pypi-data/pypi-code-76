import os
import json
import pandas as pd
import numpy as np
import shutil
import datetime

from steam_nb_api.resources.ResourceReader import ResourceReader
from steam_nb_api.utils.misc import makeCopyFile
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET

class ParametersCOSIM:
    '''
        Class of COSIM parameters to generate automatically the COSIM folder and file structure
    '''

    def __init__(self, nameFolderCosimModel: str, nameCircuit: str = "", nameMagnet: str = ""):
        '''

        :param nameFolderCosimModel: String defining the name of the folder where the COSIM model will be saved
        :type nameFolderCosimModel: str
        :param nameCircuit: string defining the circuit name; at the moment, this is just a label
        :type nameCircuit: str

        '''

        self.nameFolderCosimModel = nameFolderCosimModel
        if nameCircuit == "":
            print("No Circuit-Name defined. Setting to _0")
            self.circuitName = "_0"
        if nameMagnet == "":
            print("No Magnet-Name defined. Setting to _0")
            self.nameMagnet = "_0"
        self.circuitName = nameCircuit
        if type(nameMagnet) != list: self.nameMagnet = [nameMagnet]
        else: self.nameMagnet = nameMagnet
        self.executionOrder = []
        self.SimulationNumber = []

        # Load and set the default config files (using ResourceReader allows reading from a "hidden" resource folder)
        self.nameTemplateConfigFileCosim = ResourceReader.getResourcePath(os.path.join('sing', 'STEAMConfig.json'))
        self.nameTemplateConfigFilePSpice = ResourceReader.getResourcePath(os.path.join('sing', 'PSpiceConfig.json'))
        self.nameTemplateConfigFileLedet = ResourceReader.getResourcePath(os.path.join('sing', 'LedetConfig.json'))

    def makeAllFolders(self, N_LEDET = 1):
        '''
            **Makes a COSIM folder with the required PSPICE and LEDET subfolders**

            Function to generate all the required subfolders and files for a COSIM model

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel

        # Make COSIM folder
        if not os.path.exists(nameFolderCosimModel):
            os.makedirs(nameFolderCosimModel)

        # Make SPICE model folder
        pathFolderPSpice = os.path.join(nameFolderCosimModel, 'PSpice')
        if not os.path.exists(pathFolderPSpice):
            os.makedirs(pathFolderPSpice)

        # Make LEDET model folder and sub-folders
        if N_LEDET == 1:
            nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET')
            if not os.path.isdir(nameFolderLedetModel):
                os.mkdir(nameFolderLedetModel)
            if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET')):
                os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET'))
            if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET', self.nameMagnet[0])):
                os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET', self.nameMagnet[0]))
            if not os.path.isdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[0], "Input")):
                os.mkdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[0], "Input"))
            if not os.path.isdir(os.path.join(nameFolderLedetModel,"LEDET", self.nameMagnet[0], "Input","Initialize variables")):
                os.mkdir(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[0],"Input","Initialize variables"))
                f = open(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[0],"Input","Initialize variables", " .gitkeep"), "w")
                f.close()
            if not os.path.isdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[0], "Input","Control current input")):
                os.mkdir(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[0],"Input","Control current input"))
                f = open(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[0],"Input","Control current input", " .gitkeep"), "w")
                f.close()
            if not os.path.isdir(os.path.join(nameFolderLedetModel , "Field maps")):
                os.mkdir(os.path.join(nameFolderLedetModel,"Field maps"))
            if not os.path.isdir(os.path.join(nameFolderLedetModel, "Field maps", self.nameMagnet[0])):
                os.mkdir(os.path.join(nameFolderLedetModel, "Field maps", self.nameMagnet[0]))
            if not os.path.isdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[0] ,"Output")):
                os.mkdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[0], "Output"))

        if N_LEDET > 1:
            for i in range(1, N_LEDET+1):
                # Make LEDET model folder and sub-folders
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET_'+ str(i))
                if not os.path.isdir(nameFolderLedetModel):
                    os.mkdir(nameFolderLedetModel)
                if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET')):
                    os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET'))
                if not os.path.isdir(os.path.join(nameFolderLedetModel, 'LEDET', self.nameMagnet[i-1])):
                    os.mkdir(os.path.join(nameFolderLedetModel, 'LEDET', self.nameMagnet[i-1]))
                if not os.path.isdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input")):
                    os.mkdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input"))
                if not os.path.isdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input//Initialize variables")):
                    os.mkdir( os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input", "Initialize variables"))
                    f = open(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input", "Initialize variables", " .gitkeep"), "w")
                    f.close()
                if not os.path.isdir(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[i-1],"Input","Control current input")):
                    os.mkdir(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input", "Control current input"))
                    f = open(os.path.join(nameFolderLedetModel, "LEDET", self.nameMagnet[i-1], "Input", "Control current input", " .gitkeep"), "w")
                    f.close()
                if not os.path.isdir(os.path.join(nameFolderLedetModel,"Field maps")):
                    os.mkdir(os.path.join(nameFolderLedetModel,"Field maps"))
                if not os.path.isdir(os.path.join(nameFolderLedetModel,"Field maps",self.nameMagnet[i-1])):
                    os.mkdir(os.path.join(nameFolderLedetModel,"Field maps",self.nameMagnet[i-1]))
                if not os.path.isdir(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[i-1],"Output")):
                    os.mkdir(os.path.join(nameFolderLedetModel,"LEDET",self.nameMagnet[i-1], "Output"))

    def copyConfigFiles(self, N_LEDET = 1):
        '''
            **Makes the configuration files required to run a COSIM model with one PSPICE and one LEDET models **

            Function to generate the configuration files for COSIM, one PSPICE, and one LEDET models

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel
        nameTemplateConfigFileCosim = self.nameTemplateConfigFileCosim
        nameTemplateConfigFilePSpice = self.nameTemplateConfigFilePSpice
        nameTemplateConfigFileLedet = self.nameTemplateConfigFileLedet

        # Check that the folder exists; if not, generate all required folders and subfolders
        if not os.path.exists(nameFolderCosimModel):
            self.makeAllFolders(N_LEDET = N_LEDET)

        # Copy template COSIM config file
        makeCopyFile(nameTemplateConfigFileCosim, os.path.join(nameFolderCosimModel, 'STEAMConfig.json'))

        # Copy template PSpice config file
        makeCopyFile(nameTemplateConfigFilePSpice, os.path.join(nameFolderCosimModel, 'PSpice', 'PSpiceConfig.json'))

        if N_LEDET == 1:
            # Copy template LEDET config file
            makeCopyFile(nameTemplateConfigFileLedet, os.path.join(nameFolderCosimModel, 'LEDET', 'LedetConfig.json'))
        else:
            for i in range(1, N_LEDET+1):
                makeCopyFile(nameTemplateConfigFileLedet,
                             os.path.join(nameFolderCosimModel, 'LEDET_'+ str(i), 'LedetConfig.json'))

    def copyIOPortFiles(self, fileName_IOPortDefinition: str, fileName_complementaryIOPortDefinition: str, N_LEDET = 1):
        '''
            **Copies the input/output port files required to run a COSIM model with one PSPICE and one LEDET models **

            Function to copy the I/O Port files in the correct subfolders

            :return: None
        '''

        nameFolderCosimModel = self.nameFolderCosimModel

        # Check that the required input files exist
        if not os.path.isfile(fileName_IOPortDefinition):
            raise Exception('Input file fileName_IOPortDefinition = {} not found!'.format(fileName_IOPortDefinition))
        if not os.path.isfile(fileName_complementaryIOPortDefinition):
            raise Exception(
                'Input file fileName_IOPortDefinition = {} not found!'.format(fileName_complementaryIOPortDefinition))

        # Check that the folder exists; if not, generate all required folders and subfolders
        if not os.path.exists(nameFolderCosimModel):
            self.makeAllFolders()

        # Copy PSPICE IOPort file
        makeCopyFile(fileName_IOPortDefinition,
                     os.path.join(nameFolderCosimModel, 'PSpice', 'PspiceInputOutputPortDefinition.json'))

        # Copy LEDET IOPort file
        if N_LEDET == 1:
            makeCopyFile(fileName_complementaryIOPortDefinition,
                         os.path.join(nameFolderCosimModel, 'LEDET', 'LedetInputOutputPortDefinition.json'))
        else:
            for i in range(N_LEDET):
                makeCopyFile(fileName_complementaryIOPortDefinition,
                             os.path.join(nameFolderCosimModel, 'LEDET'+str(i), 'LedetInputOutputPortDefinition.json'))

    def makeGenericIOPortFiles(self, CoilSections, ModelFolder, CoSimFolder: str, PSpiceExecutable: str, LEDETExecutable: str,
                               t_0 = [0, 2e-5], t_end = [2e-5, 0.5], t_step_max = [[1e-5, 1e-5], [1e-5, 1e-5]],
                               relTolerance = [1e-4, None], absTolerance = [1, None], executionOrder = [1, 2],
                               executeCleanRun = [True, True], N_LEDET = 1, QuenchMagnet = 0, SimulationNumber = [0], DistinctMagnets = 1, PSPICEinitialConditions = []):

        if ModelFolder.endswith('//'): ModelFolder.replace('//','\\')
        elif not ModelFolder.endswith('\\'): ModelFolder = ModelFolder + '\\'
        if len(SimulationNumber) < N_LEDET: self.SimulationNumber = SimulationNumber + (N_LEDET - len(SimulationNumber))*[0]
        else: self.SimulationNumber = SimulationNumber
        # Components which are used in the Ports
        Components = ["L", "CoilSections"]  # [0] = PSpice, [1]=LEDET
        # Setting the Coilsections
        CSections = []
        LSections = []
        for i in range(len(CoilSections)):
            CSectionsPerPort = []
            for j in range(len(CoilSections[i])):
                CSectionsPerPort.append(Components[1] + "_" + str(CoilSections[i][j]))
            CSections.append(CSectionsPerPort)
            LSections.append(Components[0] + "_" + str(i+1))

        # Variables used for convergence, for now its the first magnet current and the LEDET Voltages
        if N_LEDET == 1:
            convergenceVariables = ["I(x_mag_1." + Components[0] + "_1)", "U_inductive_dynamic_" + Components[1]+"_1"]
        else:
            convergenceVariables = ["I(x_mag_1." + Components[0] + "_1)", "U_inductive_dynamic_" + Components[1]+"_1"]
            for i in range(2,N_LEDET+1):
                convergenceVariables.append("U_inductive_dynamic_" + Components[1]+"_1")

        # couplingParameterLedet/PS- [x] = WholePort, ..[x][i] = in/out incl. Name and type, ...[x][i][0]=name,...[x][i][1]=type
        couplingParameterLedet = [[["I", ["TH", "EM"]]], [["R", ["TH"]], ["U", ["EM"]]]]
        couplingParameterPSpice = [[[["R", ["TH"]], ["U", ["EM"]]], [["I", ["TH", "EM"]]]],
                                    [[["U", ["EM"]]], [["U", ["EM"]]]]]

        # Building STEAM.config
        PSpiceFolder = ModelFolder +"PSPICE\\"
        if N_LEDET == 1:
            LedetFolder = ModelFolder + "LEDET\\"
        else:
            LedetFolder =  ModelFolder + "LEDET_" + str(1)+"\\"

        filename = self.nameFolderCosimModel + '//STEAMConfig.json'
        try:
            os.remove(filename)
        except:
            # print('Already cleaned')
            pass
        data = {"coSimulationDir": CoSimFolder}
        data["coSimulationModelSolvers"] = ["PSPICE", "LEDET"]
        data["coSimulationModelDirs"] = [PSpiceFolder, LedetFolder]
        data["coSimulationModelConfigs"] = ["PSpiceConfig.json", "LedetConfig.json"]
        data["coSimulationPortDefinitions"] = ["PSpiceInputOutputPortDefinition.json",
                                               "LedetInputOutputPortDefinition.json"]
        data["convergenceVariables"] = convergenceVariables
        data["t_0"] = t_0
        data["t_end"] = t_end
        data["t_step_max"] = t_step_max
        data["relTolerance"] = relTolerance
        data["absTolerance"] = absTolerance
        data["executionOrder"] = executionOrder
        self.executionOrder = executionOrder
        data["executeCleanRun"] = executeCleanRun
        if N_LEDET >1:
            for i in range(2, N_LEDET+1):
                data["coSimulationModelSolvers"].append("LEDET")
                LedetFolder = ModelFolder +'LEDET_' + str(i)+"\\"
                data["coSimulationModelDirs"].append(LedetFolder)
                data["coSimulationModelConfigs"].append("LedetConfig.json")
                data["coSimulationPortDefinitions"].append("LedetInputOutputPortDefinition.json")

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        # Building PSpiceConfig
        filename = os.path.join(self.nameFolderCosimModel,'PSpice','PSpiceConfig.json')
        with open(filename, 'r') as f:
            data = json.load(f)
            data["solverPath"] = PSpiceExecutable
            data["initialConditions"] = PSPICEinitialConditions

        try:
            os.remove(filename)
        except:
            #print('Already cleaned')
            pass
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        # Building LEDETConfig
        if N_LEDET == 1:
            filename = os.path.join(self.nameFolderCosimModel,'LEDET','LedetConfig.json')
            with open(filename, 'r') as f:
                data = json.load(f)
                data["solverPath"] = LEDETExecutable
                data["modelName"] = self.nameMagnet[0]
                data["simulationNumber"] = str(SimulationNumber[0])
            try:
                os.remove(filename)
            except:
                # print('Already cleaned')
                pass
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        else:
            if len(SimulationNumber) != N_LEDET:
                SimulationNumber = [0]*N_LEDET
                print("Simulation Number 0 is used for all LEDET models")
            for i in range(1,N_LEDET+1):
                filename = os.path.join(self.nameFolderCosimModel,'LEDET_'+str(i),'LedetConfig.json')
                with open(filename, 'r') as f:
                    data = json.load(f)
                    if executionOrder.count(2) > 1:
                        idxLEDET = LEDETExecutable.find('LEDET')
                        data["solverPath"] = LEDETExecutable[0:idxLEDET + 5] + "_"+str(i) + LEDETExecutable[idxLEDET + 5:]
                        print('COSIM Parallel mode: LEDET executable ',i,' should be: ', data["solverPath"],'.')
                    else: data["solverPath"] = LEDETExecutable
                    data["modelName"] = self.nameMagnet[i-1]
                    data["simulationNumber"] = str(SimulationNumber[i-1])
                try:
                    os.remove(filename)
                except:
                    # print('Already cleaned')
                    pass
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

        # LEDETInputPortDefinitions
        if N_LEDET == 1:
            filename = os.path.join(self.nameFolderCosimModel,'LEDET','LedetInputOutputPortDefinition.json')
            try:
                os.remove(filename)
            except:
                # print('Already cleaned')
                pass

            struct_total = []
            for i in range(len(CoilSections)):  # Number of Ports
                struct = {}
                struct["name"] = "Port_" + str(i+1) + "_" + str(0)
                struct["components"] = []
                for n in range(len(CSections[i])):  # All Coilsections
                    struct["components"].append(CSections[i][n])
                struct["inputs"] = []
                for j in range(len(couplingParameterLedet[0])):  # Number of In's per respective Port
                    substruct_in = {}
                    substruct_in["couplingParameter"] = couplingParameterLedet[0][j][0]
                    substruct_in["labels"] = []
                    for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Input
                        substruct_in["labels"].append(couplingParameterLedet[0][j][0] +"_" +  CSections[i][n])
                    substruct_in["types"] = couplingParameterLedet[0][j][1]
                    struct["inputs"].append(substruct_in)

                struct["outputs"] = []
                for k in range(len(couplingParameterLedet[1])):  # Number of Out's per respective Port
                    substruct_out = {}
                    substruct_out["couplingParameter"] = couplingParameterLedet[1][k][0]
                    substruct_out["labels"] = []
                    for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Output
                        if (couplingParameterLedet[1][k][0] == "U"):  # If Output is U
                            substruct_out["labels"].append("U_inductive_dynamic" +"_" +  CSections[i][n])
                        else:  # If output is I or R
                            substruct_out["labels"].append(couplingParameterLedet[1][k][0] +"_" +  CSections[i][n])
                    substruct_out["types"] = couplingParameterLedet[1][k][1]
                    struct["outputs"].append(substruct_out)

                struct_total.append(struct)

            with open(filename, 'w') as f:
                for i in range(len(struct_total)):
                    json.dump(struct_total[i], f, indent=4)
                    f.write('\n')
        else:
            for l in range(0,N_LEDET):
                filename = os.path.join(self.nameFolderCosimModel,'LEDET_'+str(l+1),'LedetInputOutputPortDefinition.json')
                try:
                    os.remove(filename)
                except:
                    # print('Already cleaned')
                    pass

                struct_total = []
                for i in range(len(CoilSections)):  # Number of Ports
                    struct = {}
                    struct["name"] = "Port_" + str(i+l*len(CoilSections)+1) + "_" + str(0)
                    struct["components"] = []
                    for n in range(len(CSections[i])):  # All Coilsections
                        struct["components"].append(CSections[i][n])
                    struct["inputs"] = []
                    for j in range(len(couplingParameterLedet[0])):  # Number of In's per respective Port
                        substruct_in = {}
                        substruct_in["couplingParameter"] = couplingParameterLedet[0][j][0]
                        substruct_in["labels"] = []
                        for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Input
                            substruct_in["labels"].append(couplingParameterLedet[0][j][0] + "_" + CSections[i][n])
                        substruct_in["types"] = couplingParameterLedet[0][j][1]
                        struct["inputs"].append(substruct_in)

                    struct["outputs"] = []
                    for k in range(len(couplingParameterLedet[1])):  # Number of Out's per respective Port
                        substruct_out = {}
                        substruct_out["couplingParameter"] = couplingParameterLedet[1][k][0]
                        substruct_out["labels"] = []
                        for n in range(len(CSections[i])):  # Append all Coilsections as Labels to Output
                            if (couplingParameterLedet[1][k][0] == "U"):  # If Output is U
                                substruct_out["labels"].append("U_inductive_dynamic" + "_" + CSections[i][n])
                            else:  # If output is I or R
                                substruct_out["labels"].append(couplingParameterLedet[1][k][0] + "_" + CSections[i][n])
                        substruct_out["types"] = couplingParameterLedet[1][k][1]
                        struct["outputs"].append(substruct_out)

                    struct_total.append(struct)

                with open(filename, 'w') as f:
                    for i in range(len(struct_total)):
                        json.dump(struct_total[i], f, indent=4)
                        f.write('\n')

        # PSpice
        filename = os.path.join(self.nameFolderCosimModel,'PSpice','PSpiceInputOutputPortDefinition.json')
        try:
            os.remove(filename)
        except:
            # print('Already cleaned')
            pass

        struct_total = []
        for n in range(0, N_LEDET):
            if n+1== QuenchMagnet and QuenchMagnet != 0:
                quench = '_Quench'
            else:
                quench = ''
            if DistinctMagnets != 1:
                DM = n+1
                M_add = "M"+str(DM)+'_'
            elif n == QuenchMagnet and QuenchMagnet != 0:
                DM = 1+QuenchMagnet
                M_add = ''
            else:
                DM = 1
                M_add = ''
            for i in range(len(CoilSections)):  # Number of Ports
                for j in range(2):  # 2Ports in PSpice
                    struct = {}
                    struct["name"] = "Port_" + str(i+n*len(CoilSections)+1) + "_" + str(j)
                    struct["components"] = [LSections[i]]
                    struct["inputs"] = []
                    for l in range(len(couplingParameterPSpice[j][0])):  # Number of In's
                        substruct_in = {}
                        substruct_in["couplingParameter"] = couplingParameterPSpice[j][0][l][0]
                        if (j == 0):  # Second Port in PSpice is U/U, check on that here
                            if (couplingParameterPSpice[j][0][l][0] == "U"):
                                cPPSpice = "V"
                            else:
                                cPPSpice = couplingParameterPSpice[j][0][l][0]
                            substruct_in["labels"] = [cPPSpice + "_field_"+M_add + str(i+1) + "_stim"+quench]  # First Port for Field
                        else:  # Second Port with circuit
                            substruct_in["labels"] = ["V_circuit_" +M_add+ str(i+1) + "_stim"+quench]
                        substruct_in["types"] = couplingParameterPSpice[j][0][l][1]
                        struct["inputs"].append(substruct_in)

                    struct["outputs"] = []
                    for k in range(len(couplingParameterPSpice[j][1])):  # Number of Out's
                        substruct_out = {}
                        substruct_out["couplingParameter"] = couplingParameterPSpice[j][1][k][0]
                        if (j == 0):  # Check again for outputs for which of the 2Ports for Pspice one is in
                            if (couplingParameterPSpice[j][1][k][0] == "U"):
                                cPPSpice = "V"
                            else:
                                cPPSpice = couplingParameterPSpice[j][1][k][0]
                            substruct_out["labels"] = [
                                cPPSpice + "(x_mag_" + str(DM)+ "." + Components[0] + "_" + str(i+1) + ")"]
                        else:
                            substruct_out["labels"] = ["V(x_mag_" + str(DM)+ "." + str(i+1) + "_v_l_diff)"]
                        substruct_out["types"] = couplingParameterPSpice[j][1][k][1]
                        struct["outputs"].append(substruct_out)

                    struct_total.append(struct)

        with open(filename, 'w') as f:
            for i in range(len(struct_total)):
                json.dump(struct_total[i], f, indent=4)
                f.write('\n')

    def FindLibPath(self, File):
        path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        for i in range(5):
            if os.path.isdir(os.path.join(path,"steam-pspice-library")):
               return  os.path.join(path,File)
            else:
                path =  os.path.abspath(os.path.join(path, os.pardir))
        print("Could not find PSPICE library. Please add manually.")
        return False

    def CopyCircuit(self, FileOld, FileNew):
        inOption = 0
        inAutoConverge = 0

        fN = open(FileNew, 'w+')
        with open(FileOld) as fp:
            for ls in fp:
                # print(ls)
                if ls.startswith("*.OPTION") or ls.startswith("* .OPTION"):
                    fN.write(ls[1:])
                    inOption = 1
                elif ls.startswith("*.AUTOCONVERGE") or ls.startswith("* .AUTOCONVERGE"):
                    fN.write(ls[1:])
                    inAutoConverge = 1
                elif ls.startswith("*+") or ls.startswith("* +"):
                    if inOption or inAutoConverge: fN.write(ls[1:])
                else:
                    inOption = 0
                    inAutoconverge = 0
                    fN.write(ls)
            fN.close()

    def copyCOSIMfiles(self, nameFileSING, StimulusFile, nameMagnet, N_LEDET=1, ManuallyStimulusFile = ''):
        LEDETFiles = os.path.abspath(os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)),os.pardir))
        LEDETFiles = os.path.join(LEDETFiles, "steam-ledet-input")
        nameFolderCosimModel = self.nameFolderCosimModel

        if type(nameMagnet) != list: nameMagnet = [nameMagnet]

        # Copy PSPICE model file
        if len(ManuallyStimulusFile) == 0:
            StimulusFile = self.FindLibPath(StimulusFile)
            if StimulusFile == False: return
        else:
            StimulusFile = ManuallyStimulusFile
        nameFolderPSpiceModel = os.path.join(nameFolderCosimModel, 'PSpice')
        if not os.path.isdir(nameFolderPSpiceModel):
            os.mkdir(nameFolderPSpiceModel)

        self.CopyCircuit(nameFileSING, os.path.join(nameFolderPSpiceModel, 'Circuit.cir'))
        # makeCopyFile(nameFileSING, os.path.join(nameFolderPSpiceModel, 'Circuit.cir'))
        makeCopyFile(StimulusFile, os.path.join(nameFolderPSpiceModel, 'ExternalStimulus.stl'))

        LEDET_Fs = []
        for i in range(N_LEDET):
            if N_LEDET > 1:
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET_'+str(i+1))
                if len(nameMagnet)>1:
                    sourcedir = os.path.join(LEDETFiles, nameMagnet[i])
                    nM = nameMagnet[i]
                else:
                    sourcedir = os.path.join(LEDETFiles, nameMagnet)
                    nM = nameMagnet
            else:
                sourcedir = os.path.join(LEDETFiles, nameMagnet[0])
                nameFolderLedetModel = os.path.join(nameFolderCosimModel, 'LEDET')
                nM = nameMagnet[0]
            sourcefiles = os.listdir(sourcedir)
            if not os.path.isdir(nameFolderLedetModel):
                os.mkdir(nameFolderLedetModel)
            destinationpath_field = nameFolderLedetModel + "//Field maps//" + nM
            destinationpath_para = nameFolderLedetModel + "//LEDET//" + nM + "//Input//"

            SimNumber = self.SimulationNumber[i]
            for file in sourcefiles:
                if file.endswith('.map2d') and not file.startswith(".sys"):
                    makeCopyFile(os.path.join(sourcedir, file), os.path.join(destinationpath_field, file))
                if file.endswith(str(nM)+"_"+str(SimNumber) +'.xlsx') and not file.startswith(".sys"):
                    shutil.copy(os.path.join(sourcedir, file), os.path.join(destinationpath_para, file))
                    LEDET_Fs.append(os.path.join(destinationpath_para, file))
                if file.endswith('_selfMutualInductanceMatrix.csv'):
                    shutil.copy(os.path.join(sourcedir, file), os.path.join(destinationpath_para, file))
        return LEDET_Fs

    def prepareLEDETFiles(self, files, N_PAR=1):
        TurnNumber = 0
        steps = 0

        ## Count most frequent execution order
        counter = 0
        num = self.executionOrder[0]
        for i in self.executionOrder:
            curr_frequency = self.executionOrder.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i

        # If num ==1 change to 2 as 1 is by convention PSPICE
        if num == 1: num = 2

        # Prepare the files based on single function
        if type(files) == list:
            for i in range(len(files)):
                file = files[i]
                [Tnew, Snew] = self.prepareSingleLEDETFile(file)
                if self.executionOrder[i+1] == num:
                    TurnNumber = TurnNumber + Tnew
                    steps = steps + Snew
            TurnNumber = int(TurnNumber / len(files))
            steps = int(steps / len(files))
        else:
            [TurnNumber, steps] = self.prepareSingleLEDETFile(files)

        ## Do some kind of check
        TurnNumber_All = TurnNumber*N_PAR

        print(TurnNumber_All,' Turns are planned to be simulated in parallel with about ', steps, ' time steps.')
        if TurnNumber_All >= 10000:
            print("You are trying to simulate ",str(TurnNumber_All),"in parallel mode. \n")
            maxN_PAR = np.floor(10000/TurnNumber)
            print("Consider not to user more than ", str(maxN_PAR)," parallel Simulations.")

    def prepareSingleLEDETFile(self, file):
        a = ParametersLEDET()
        a.readLEDETExcel(file)
        a.Options.flag_useExternalInitialization = 1
        a.Options.flag_generateReport = 0
        a.Options.flag_saveMatFile = 0
        a.Options.flag_automaticRefinedTimeStepping = 0
        a.writeFileLEDET(file)

        TurnNumber = max(a.Inputs.HalfTurnToInductanceBlock)
        tV = a.Options.time_vector_params
        steps = 0
        for i in range(0,len(tV),3):
            steps = steps + abs(abs(tV[i])-abs(tV[i+2]))/tV[i+1]

        return [TurnNumber, steps]

    def writeCOSIMBatch(self, COSIMfolder, COSIMexe, Destination = ''):
        if type(COSIMfolder) != list:
            COSIMfolder = [COSIMfolder]
        if Destination: fileName = Destination+'COSIM_nb_Batch.bat'
        else: fileName = 'COSIM_nb_Batch.bat'
        fN = open(fileName, 'w+')

        txt_stub = "java -jar " + COSIMexe
        for i in range(len(COSIMfolder)):
            tx_line = txt_stub + " " + str(COSIMfolder[i]) + "\\STEAMConfig.json" + " \n "
            fN.write(tx_line)
        fN.close()

