from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.utils.SelfMutualInductanceCalculation import SelfMutualInductanceCalculation
import numpy as np
import os
import sys
import datetime
import xlrd
from pathlib import Path
from steam_nb_api.utils import workbook as w
from steam_nb_api.utils import arrays as a
from py4j.java_gateway import launch_gateway, java_import, JavaGateway, JavaObject, GatewayParameters, Py4JNetworkError
from py4j.java_collections import ListConverter

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

class CircuitFrequencyModelling:
    def customPrint(self,s):
        if self.flag_print:
            print(s)

    def __init__(self,nameCircuit,subcirdirpath,excelpath,flag_print):

        self.flag_print = flag_print

        # File loading
        eospath = os.getcwd()
        eossplit = eospath.split(os.path.sep)
        SWAN_index = eossplit.index('SWAN_projects')  # If this line throws an error it is most likely because the current working directory doesn't include 'SWAN_projects'
        eospath = ''
        for j in range(SWAN_index):
            eospath = eospath + eossplit[j] + '/'
        self.eospath = eospath

        #subcirdir = eospath + subcirdirpath
        subcirdir = subcirdirpath
        self.subcirdir = subcirdir

        excelname = eospath + excelpath

        xl_workbook = xlrd.open_workbook(excelname)
        a = xl_workbook.sheet_by_index(0)

        circs_name = []
        for i in range(0, a.nrows):
            circs_name.append(a.cell(i, 0).value)
        ind = circs_name.index(nameCircuit)

        circs_columns = []
        for i in range(0, a.ncols):
            circs_columns.append(a.cell(0, i).value)

        # Circuit parameters

        # Array for each magnet type
        try:
            N_MAG = np.int_(a.cell(ind, circs_columns.index('N_MAG [-]')).value.split(','))
        except:
            N_MAG = [int(a.cell(ind, circs_columns.index('N_MAG [-]')).value)]
        self.N_MAG = N_MAG

        try:
            MAG_TYPE = a.cell(ind, circs_columns.index('MAG_TYPE [-]')).value.split(',')
        except:
            MAG_TYPE = [a.cell(ind, circs_columns.index('MAG_TYPE [-]')).value]
        self.MAG_TYPE = MAG_TYPE

        try:
            L_BUSBAR = np.float_(a.cell(ind, circs_columns.index('L_BUSBAR [H]')).value.split(','))
        except:
            L_BUSBAR = [float(a.cell(ind, circs_columns.index('L_BUSBAR [H]')).value)]
        self.L_BUSBAR = L_BUSBAR

        try:
            R_PAR = np.float_(a.cell(ind, circs_columns.index('R_PARALLEL [Ohm]')).value.split(','))
        except:
            R_PAR = [a.cell(ind, circs_columns.index('R_PARALLEL [Ohm]')).value]
        self.R_PAR = R_PAR

        try:
            C_PAR = np.float_(a.cell(ind, circs_columns.index('C_PARALLEL [F]')).value.split(','))
        except:
            C_PAR = [a.cell(ind, circs_columns.index('C_PARALLEL [F]')).value]
        self.C_PAR = C_PAR

        # Only non array
        R_SER = a.cell(ind, circs_columns.index('R_SERIES [Ohm]')).value
        self.R_SER = R_SER

        # Netlist
        pointsPerDecade = int(a.cell(ind, circs_columns.index('pointsPerDecade')).value)
        startFrequency = a.cell(ind, circs_columns.index('startFrequency')).value
        stopFrequency = a.cell(ind, circs_columns.index('stopFrequency')).value

        self.pointsPerDecade = pointsPerDecade
        self.startFrequency = startFrequency
        self.stopFrequency = stopFrequency

        self.nameCircuit = nameCircuit

        # Scales
        F_SCALE_C_GROUND = a.cell(ind, circs_columns.index('F_SCALE_C_GROUND')).value
        F_SCALE_C_T2T = a.cell(ind, circs_columns.index('F_SCALE_C_T2T')).value
        F_SCALE_L = a.cell(ind, circs_columns.index('F_SCALE_L')).value
        F_SCALE_R = a.cell(ind, circs_columns.index('F_SCALE_R')).value

        self.F_SCALE_C_GROUND = F_SCALE_C_GROUND
        self.F_SCALE_C_T2T = F_SCALE_C_T2T
        self.F_SCALE_L = F_SCALE_L
        self.F_SCALE_R = F_SCALE_R

        flag_R_Par = a.cell(ind, circs_columns.index('flag_R_Par')).value
        R_Par = a.cell(ind, circs_columns.index('R_Par (Ohm)')).value

        self.flag_R_Par = flag_R_Par
        self.R_Par = R_Par

        # Eddy current loops
        flag_E_loops = a.cell(ind, circs_columns.index('flag_E_loops')).value
        E_loops = np.array(a.cell(ind, circs_columns.index('E_loops [L (H), R (Ohm), k]')).value.split(','))
        E_loops = E_loops.astype(np.float)
        E_loops = E_loops.reshape(np.int_(len(E_loops) / 3), 3)

        self.flag_E_loops = flag_E_loops
        self.E_loops = E_loops

        self.customPrint('Number of magnet types:')
        self.customPrint(len(MAG_TYPE))

    def netlist(self,model):
        # model is either turns or groups dependent on the wanted model
        path_gateway = self.eospath + 'SWAN_projects/steam-notebooks/steam/*'

        # Launch a Gateway in a new Java process, this returns port
        port = launch_gateway(classpath=path_gateway)
        # JavaGateway instance is connected to a Gateway instance on the Java side
        gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
        # Get STEAM API Java classes
        MutualInductance = gateway.jvm.component.MutualInductance
        Netlist = gateway.jvm.netlist.Netlist
        CommentElement = gateway.jvm.netlist.elements.CommentElement
        GeneralElement = gateway.jvm.netlist.elements.GeneralElement
        GlobalParameterElement = gateway.jvm.netlist.elements.GlobalParameterElement
        ParameterizedElement = gateway.jvm.netlist.elements.ParameterizedElement
        ACSolverElement = gateway.jvm.netlist.solvers.ACSolverElement
        CircuitalPreconditionerSubcircuit = gateway.jvm.preconditioner.CircuitalPreconditionerSubcircuit
        TextFile = gateway.jvm.utils.TextFile
        CSVReader = gateway.jvm.utils.CSVReader

        MAG_TYPE = self.MAG_TYPE
        N_MAG = self.N_MAG
        L_BUSBAR = self.L_BUSBAR
        R_PAR = self.R_PAR
        C_PAR = self.C_PAR
        R_SER = self.R_SER

        nameCircuit = self.nameCircuit

        pointsPerDecade = self.pointsPerDecade
        startFrequency = self.startFrequency
        stopFrequency = self.stopFrequency

        F_SCALE_C_GROUND = self.F_SCALE_C_GROUND
        F_SCALE_C_T2T = self.F_SCALE_C_T2T
        F_SCALE_L = self.F_SCALE_L
        F_SCALE_R = self.F_SCALE_R

        flag_R_Par = self.flag_R_Par
        R_Par = self.R_Par
        flag_E_loops = self.flag_E_loops
        E_loops = self.E_loops

        netlist = Netlist("")

        libraryPaths = []

        for i in range(len(MAG_TYPE)):
            libraryPaths = libraryPaths + ["\"" + self.subcirdir + "\\" + MAG_TYPE[i] + "_" + model + ".lib\""]

        netlist.setLibraryPaths(a.convert_list_to_string_array(gateway, libraryPaths))

        global_param = []
        global_values = []

        E_param_param = []
        E_param_values = []

        # PARAM for all non magnet components

        # Array components
        #print(MAG_TYPE)
        #print(N_MAG)
        #print(L_BUSBAR)
        #print(R_PAR)
        #print(C_PAR)
        for i in range(len(MAG_TYPE)):
            global_param = global_param + [str.format('L_BUSBAR_{}_{}', i + 1, MAG_TYPE[i]), str.format('R_PARALLEL_{}_{}', i + 1, MAG_TYPE[i]),str.format('C_PARALLEL_{}_{}', i + 1, MAG_TYPE[i])]
            global_values = global_values + [str.format('{}', L_BUSBAR[i]), str.format('{}', R_PAR[i]), str.format('{}', C_PAR[i])]

        # Series resistance
        global_param = global_param + ['R_SERIES']
        global_values = global_values + [str.format('{}', R_SER)]

        # Scales
        if model == "magnet":
            global_param = global_param + ['F_SCALE_C_GROUND', 'F_SCALE_L', 'F_SCALE_R']
            global_values = global_values + [str.format('{}', F_SCALE_C_GROUND), str.format('{}', F_SCALE_L), str.format('{}', F_SCALE_R)]
        else:
            global_param = global_param + ['F_SCALE_C_GROUND', 'F_SCALE_C_T2T', 'F_SCALE_L', 'F_SCALE_R']
            global_values = global_values + [str.format('{}', F_SCALE_C_GROUND), str.format('{}', F_SCALE_C_T2T), str.format('{}', F_SCALE_L), str.format('{}', F_SCALE_R)]

        if flag_E_loops:
            self.customPrint("WARNING: Eddy current loops added, will cause errors if less eddy current loops are present in the used library files.")
            for i in range(len(E_loops)):
                E_param_param = E_param_param + [str.format('L_EDDY{}', i + 1), str.format('R_EDDY{}', i + 1),
                                                 str.format('K_EDDY{}', i + 1)]
                E_param_values = E_param_values + [str.format('{}', E_loops[i][0]), str.format('{}', E_loops[i][1]),
                                                   str.format('{}', E_loops[i][2])]

            global_param = global_param + E_param_param
            global_values = global_values + E_param_values

        if flag_R_Par:
            self.customPrint("WARNING: Parallel resistance added, will cause errors if the parallel resistance isn't present in the used library files.")
            global_param = global_param + ['R_Par']
            global_values = global_values + [str.format('{}', R_Par)]

        global_param = a.create_string_array(gateway, global_param)
        global_values = a.create_string_array(gateway, global_values)

        netlist.add(CommentElement("**** Global parameters ****"))
        netlist.add(GlobalParameterElement(global_param, global_values))
        netlist.add(CommentElement("* Magnet types:"))
        s = "* " + str(MAG_TYPE)
        netlist.add(CommentElement(s))

        netlist.add(CommentElement("* .STEP PARAM R_Par 10k, 100k, 10k"))

        #placeholder nodes
        nodes = gateway.new_array(gateway.jvm.String, 2)
        nodesX = gateway.new_array(gateway.jvm.String, 3)

        GROUND_NODE = "0"

        netlist.add(CommentElement("* Circuit:"))

        # ADD series resistance FIRST
        name = "R_Series"
        nodes[0], nodes[1] = "0series_in" , "0series_out"
        value = "{R_SERIES}"
        netlist.add(GeneralElement(name, nodes, value));

        k = 1 #Overall index (starts at 1 since the series resistance is the first node)
        for i in range(len(N_MAG)):
            for j in range(N_MAG[i]):
                s = str.format("* Cell: {}" , k)
                netlist.add(CommentElement(s))

                #L_BUSBAR
                name=str.format("L_BUSBAR_{}_{}_N_{}", i + 1, MAG_TYPE[i], j + 1)
                if k == 1:
                    nodes[0], nodes[1] = "0series_out" , str.format("{}mid" , k)
                else:
                    nodes[0], nodes[1] = str.format("{}out" , k-1) , str.format("{}mid" , k)
                value = "{L_BUSBAR_"+str(i+1)+"_"+MAG_TYPE[i]+"}"
                netlist.add(GeneralElement(name, nodes, value));
                #magnet
                name=str.format("x_{}_{}_N_{}", i + 1, MAG_TYPE[i], j + 1)
                nodes[0], nodes[1] = str.format("{}mid" , k) , str.format("{}out" , k)
                nodesX[0], nodesX[1], nodesX[2] = nodes[0], nodes[1], GROUND_NODE
                attribute = MAG_TYPE[i]+"_"+model
                if model == "magnet":
                    magnet_param = ["F_SCALE_C_GROUND","\n+ F_SCALE_L","F_SCALE_R"] #"\n+" is added to make new lines when needed
                    magnet_val = ["F_SCALE_C_GROUND","F_SCALE_L","F_SCALE_R"]
                else:
                    magnet_param = ["F_SCALE_C_GROUND","F_SCALE_C_T2T","\n+ F_SCALE_L","F_SCALE_R"] #"\n+" is added to make new lines when needed
                    magnet_val = ["F_SCALE_C_GROUND","F_SCALE_C_T2T","F_SCALE_L","F_SCALE_R"]

                if flag_E_loops:
                    for E_i in range(len(E_loops)):
                        magnet_param = magnet_param + [str.format("\n+ L_EDDY{}", E_i + 1), str.format("R_EDDY{}", E_i + 1),
                                                         str.format("K_EDDY{}", E_i + 1)]
                        magnet_val = magnet_val + [str.format("L_EDDY{}", E_i + 1), str.format("R_EDDY{}", E_i + 1),
                                                         str.format("K_EDDY{}", E_i + 1)]

                if flag_R_Par:
                    magnet_param = magnet_param + ["\n+ R_Par"]
                    magnet_val = magnet_val + ["R_Par"]

                magnet_parameters = a.create_string_array(gateway, magnet_param)
                magnet_values = a.create_string_array(gateway,magnet_val)
                netlist.add(ParameterizedElement(name, nodesX, attribute, magnet_parameters, magnet_values))
                #R_PAR
                name=str.format("R_PAR_{}_{}_N_{}", i + 1, MAG_TYPE[i], j + 1)
                value = "{R_PARALLEL_"+str(i+1)+"_"+MAG_TYPE[i]+"}"
                netlist.add(GeneralElement(name, nodes, value));
                #C_PAR
                name=str.format("C_PAR_{}_{}_N_{}", i + 1, MAG_TYPE[i], j + 1)
                value = "{C_PARALLEL_"+str(i+1)+"_"+MAG_TYPE[i]+"}"
                netlist.add(GeneralElement(name, nodes, value));

                k=k+1 # update index

        #last busbar
        s = "Last busbar"
        netlist.add(CommentElement(s))
        name = "L_BUSBAR_END"
        nodes[0], nodes[1] = str.format("{}out" , k-1) , GROUND_NODE
        value = "{L_BUSBAR_"+str(len(N_MAG))+"_"+MAG_TYPE[-1]+"}"
        netlist.add(GeneralElement(name, nodes, value));

        # Voltage source
        netlist.add(CommentElement(" Voltage source"));
        name = "V_AC"
        nodes[0], nodes[1] = GROUND_NODE , "0series_in"
        value = "AC 1"
        netlist.add(GeneralElement(name, nodes, value));

        # Voltage measurement
        netlist.add(CommentElement(" Voltage measurement"));
        name = "E_total_voltage"
        nodes[0], nodes[1] = GROUND_NODE, "0total_voltage"
        value = "VALUE = {V(0series_out)-V(" + str.format("{}out" , k-1) + ")}"
        netlist.add(GeneralElement(name, nodes, value));

        netlist.setSolver(ACSolverElement.Builder()
                            .pointsPerDecade(pointsPerDecade)
                            .startFrequency(startFrequency)
                            .stopFrequency(stopFrequency)
                            .build())

        netlistAsListString = netlist.generateNetlistFile("BINARY")

        cwd = os.getcwd()
        Path(cwd + '/' + nameCircuit).mkdir(parents=True, exist_ok=True)
        Circ = nameCircuit + '/' + nameCircuit + "_" + model +'.cir'
        s = model + '-based netlist file generated.'
        print(s)

        #remove empty "+" lines
        netlistAsListString = [sub.replace('\n+ \n+', '\n+') for sub in netlistAsListString]

        #change probe line
        probe_ind = netlistAsListString.index('\n.PROBE')
        netlistAsListString[probe_ind] = '\n* Configuration file\n.INC configurationFileFrequency.cir'
        netlistAsListString = ListConverter().convert(netlistAsListString, gateway._gateway_client)

        TextFile.writeMultiLine(Circ, netlistAsListString, False)

        return netlist, netlistAsListString





class FrequencyModelling:
    # This dataclass is created to generate frequency based netlist of any LHC magnet. The class is based around
    # creating to different models, one based on the turns of the magnet and one based of the groups of the magnet.
    # This is done so that the simulation can be done faster if needed by the group based model, at the cost of loosing
    # detail. Which is especially useful for the very complex magnet models normally taking hours to run.

    def customPrint(self,s):
        if self.flag_print:
            print(s)

    def __init__(self,nameMagnet,swanpath,inputpath,flag_print):
        # Initiate the model. The function loads in the relevant files from LEDET and Roxie, as specfied in the input arguments.
        # The function further more calculates and saves relevant data to be used in by other functions.
        #
        # NOTE: New groups (called turn-groups in specific cases) are created since the coupling coefficient of the
        #       original groups can't be calculated correctly
        #
        # ASSUMPTION: this code is always run inside SWAN_projects for now, meaning that the first part of the string,
        #             in particulairly the user, can be found by searching for 'SWAN_projects' in os.getcwd()
        #
        # Input Arguments
        # nameMagnet                : The name of the magnet. This is used to find the correct file folder, LEDET excel file and Roxie file.
        # inputpath                 : Everything that is not the magnet name in the LEDET excel file name.
        # roxieextension            : Similair to excelfilename however only part of the filename is needed, since the 'Iron' and 'SelfField' part of the name is found automatically
        # headerlines               : The amount of headerlines in the Roxie file
        # swanpath                  : The partial path string from 'SWAN_projects' and onwards to the file folder containing the LEDET file
        # flag_print                : If this flag is low almost all printing is disabled, only the netlist generation and time stamp is still printed.
        #
        # Capacitance specifications:
        # epsR_LayerToInner         : The relative permittivity of the insulation between the inner grounding and turns
        # epsR_LayerToOuter         : The relative permittivity of the insulation between the outer grounding and turns
        # epsR_BetweenLayers        : The relative permittivity of the insulation between the layers of the magnet
        # hIns_LayerToInner         : The thickness of the insulation between the inner grounding and turns
        # hIns_LayerToOuter         : The thickness of the insulation between the outer grounding and turns
        # hIns_BetweenLayers        : The thickness of the insulation between the between the layers of the magnet
        # narrow_inner              : A list of the first half of the groups which have a capacitance to ground from
        #                           : their narrow side, to the inner side of the magnet
        # wide_first                : A list of the first half of the groups which have a capacitance to ground from
        #                           : their wide side, to the inner side of the magnet
        # narrow_outer              : A list of the first half of the groups which have a capacitance to ground from
        #                           : their narrow side, to the outer side of the magnet
        # wide_last                : A list of the first half of the groups which have a capacitance to ground from
        #                           : their wide side, to the outer side of the magnet
        #
        # Inputs:
        # Excel_Extension           : Everything after the magnet name in the excel filename (usually '_0.xlsx')
        # Roxie_Extension           : Part of the extension after the magnet name in the roxie filename. However since
        #                             information about the SelfField and Iron is available only the rest of the
        #                             filename is needed (usually 'E1' - 'E8' or 'All')
        # Roxie_Headerlines         : The amount headerlines in the Roxie file (usually 1)
        # flag_strandCorrection     : Passed directly to the 'calculateInductance' function
        # flag_sumTurnToTurn        : Passed directly to the 'calculateInductance' function
        # flag_writeOutput          : Passed directly to the 'calculateInductance' function
        # dev_max                   : The maximum allowed relative deviation when comparing the calculated turns based
        #                             M-matrix to the one found in the LEDET file.
        # flag_CapacitanceToInner   : If the flag is high the capacitance between the inner grounding and the magnet is calculated
        # flag_CapacitanceToOuter   : If the flag is high the capacitance between the outer grounding and the magnet is calculated
        # Capacity_T2T              : An array that lists the values of the capacitance between the nodes specified by Contact_To and Contact_From
        # Contact_To                : An array of nodes to which the capacitance should be added (between Contact_To and Contact_From)
        # Contact_From              : An array of nodes to which the capacitance should be added (between Contact_To and Contact_From)
        # flag_T2TCapWidth          : If the flag is high the capacitance between the turns width-wise is calculated
        # flag_T2TCapHeight         : If the flag is high the capacitance between the turns heihgt-wise is calculated
        # epsR_BetweenLayers        : The relative permittivity of the additional insulation between the layers of the turns
        # hIns_BetweenLayers        : The thickness of the additional insulation between the layers of the turns
        # flag_writeFile            : If true a '.cir' file is created based on the magnet name. The file has an extension
        #                             specifying if it is a turn or group based model. The file is created inside a subdirectory,
        #                             also named in relation to either turns or groups, of the folder containing the notebook
        #                             used to run the code.
        # flag_R_Par                : If true the function adds a parallel resistance with the value 'R_par' to the netlist
        # R_Par                     : The value of the added parallel resistance (Implemented as a parameter in the netlist)
        # flag_E_loops              : If true the function adds a eddy current loops based on 'E_loops' to the netlist
        # E_loops                   : The values of resistance, inductance and coupling coefficients of the added eddy current
        #                             loops. FORMAT: [[L1,R1,K1] , [L2,R2,K2] , ... , [LX,RX,KX]]
        # Coil_Select               : This is used to choose which coilsections to model (0 is used for all coilsections)
        # F_SCALE_C_GROUND          : The default scaling of the capacitance to ground in the netlist (added as a parameter)
        # F_SCALE_C_T2T             : The default scaling of the capacitance between turns/groups in the netlist
        #                             (added as a parameter)
        # F_SCALE_L                 : The default scaling of the self inductance in the netlist (added as a parameter)
        # F_SCALE_R                 : The default scaling of the resistance in the netlist (added as a parameter)
        # pointsPerDecade           : Points per decade in the AC simulation
        # startFrequency            : Start frequency of the AC simulation
        # stopFrequency             : Stop frequency of the AC simulation

        # print flag
        self.flag_print = flag_print

        # File loading
        eospath = os.getcwd()
        eossplit = eospath.split(os.path.sep)
        SWAN_index = eossplit.index('SWAN_projects')  # If this line throws an error it is most likely because the current working directory doesn't include 'SWAN_projects'
        eospath = ''
        for j in range(SWAN_index):
            eospath = eospath + eossplit[j] + '/'

        #capname = eospath + cappath

        inputname = eospath + inputpath

        #xl_workbook = xlrd.open_workbook(capname)
        #a = xl_workbook.sheet_by_index(0)

        xl_workbook2 = xlrd.open_workbook(inputname)
        b = xl_workbook2.sheet_by_index(0)

        # Inputs

        # magnets name is redone for robustness
        magnets_name = []
        for i in range(0, b.nrows):
            magnets_name.append(b.cell(i, 0).value)
        ind = magnets_name.index(nameMagnet)
        magnets_columns = []
        for i in range(0, b.ncols):
            magnets_columns.append(b.cell(0, i).value)

        flag_R_Par = b.cell(ind, magnets_columns.index('flag_R_Par')).value
        R_Par = b.cell(ind, magnets_columns.index('R_Par (Ohm)')).value

        # File specifics
        excelextension = b.cell(ind, magnets_columns.index('Excel_Extension')).value
        excelfilename = nameMagnet + excelextension
        roxieextension = b.cell(ind, magnets_columns.index('Roxie_Extension')).value
        roxieextension = '_' + roxieextension + '_' # add flanking '_'
        headerLines = b.cell(ind, magnets_columns.index('Roxie_Headerlines')).value

        # Eddy current loops
        flag_E_loops = b.cell(ind, magnets_columns.index('flag_E_loops')).value
        E_loops = np.array(b.cell(ind, magnets_columns.index('E_loops [L (H), R (Ohm), k]')).value.split(','))
        E_loops = E_loops.astype(np.float)
        E_loops = E_loops.reshape(np.int_(len(E_loops) / 3), 3)

        # Scales
        F_SCALE_C_GROUND = b.cell(ind, magnets_columns.index('F_SCALE_C_GROUND')).value
        F_SCALE_C_T2T = b.cell(ind, magnets_columns.index('F_SCALE_C_T2T')).value
        F_SCALE_L = b.cell(ind, magnets_columns.index('F_SCALE_L')).value
        F_SCALE_R = b.cell(ind, magnets_columns.index('F_SCALE_R')).value

        # Self-mutual inductance calculation, using SMIC (https://cernbox.cern.ch/index.php/s/37F87v3oeI2Gkp3)
        flag_strandCorrection = b.cell(ind, magnets_columns.index('flag_strandCorrection')).value
        flag_sumTurnToTurn = b.cell(ind, magnets_columns.index('flag_sumTurnToTurn')).value
        flag_writeOutput = b.cell(ind, magnets_columns.index('flag_writeOutput')).value
        dev_max = b.cell(ind, magnets_columns.index('dev_max')).value  # maximum relative deviation

        # Capacitance to ground
        flag_CapacitanceToInner = b.cell(ind, magnets_columns.index('flag_CapacitanceToInner')).value
        flag_CapacitanceToOuter = b.cell(ind, magnets_columns.index('flag_CapacitanceToOuter')).value
        flag_CapacitanceWide = b.cell(ind, magnets_columns.index('flag_CapacitanceWide')).value

        # Capacitance between turns/groups
        flag_T2TCapWidth = b.cell(ind, magnets_columns.index('flag_T2TCapWidth')).value
        flag_T2TCapHeight = b.cell(ind, magnets_columns.index('flag_T2TCapHeight')).value

        # Netlist
        pointsPerDecade = int(b.cell(ind, magnets_columns.index('pointsPerDecade')).value)
        startFrequency = b.cell(ind, magnets_columns.index('startFrequency')).value
        stopFrequency = b.cell(ind, magnets_columns.index('stopFrequency')).value

        flag_writeFile = b.cell(ind, magnets_columns.index('flag_writeFile')).value

        # LEDET and Roxie
        filename = eospath + swanpath + excelfilename

        LEDET = ParametersLEDET()

        LEDET.readLEDETExcel(filename)

        # Acquire data from ROXIE .map2d file
        # Roxie filename autimatically found from LEDET options
        if LEDET.Options.flagIron:
            roxieextension += 'WithIron_'
        else:
            roxieextension += 'NoIron_'
        if LEDET.Options.flagSelfField:
            roxieextension += 'WithSelfField'
        else:
            roxieextension += 'NoSelfField'
        roxieextension = roxieextension + '.map2d'
        fileNameRoxie = eospath + swanpath + nameMagnet + roxieextension

        strandToHalfTurn = np.array([])

        x = []
        y = []
        I = []

        ## Read file
        file = open(fileNameRoxie, "r")
        fileContent = file.read()

        ## Separate rows
        fileContentByRow = fileContent.split("\n")

        for index in range(len(fileContentByRow) - 1):
            if index > headerLines:
                fc = fileContentByRow[index]
                row = fc.split()
                strandToHalfTurn = np.hstack([strandToHalfTurn, int(row[1])])
                x = np.hstack([x, float(row[3]) / 1000])  # in [m]
                y = np.hstack([y, float(row[4]) / 1000])  # in [m]
                I = np.hstack([I,float(row[8])])
        # Count number of groups defined
        nCoilSectionsDefined = np.max(LEDET.Inputs.GroupToCoilSection)
        nCoilSectionsDefined = nCoilSectionsDefined.astype(np.int64)
        nGroupsDefined = len(LEDET.Inputs.GroupToCoilSection)

        self.customPrint('')
        self.customPrint(str(nCoilSectionsDefined) + ' coil sections defined.')
        self.customPrint(str(nGroupsDefined) + ' groups defined.')

        # Number of half-turns in each group
        nT = LEDET.Inputs.nT
        nT = nT.astype(np.int64)  # needs to be integers (LEDET is inputtet as float)

        nHalfTurns = int(sum(nT));
        nTurns = int(nHalfTurns / 2)

        nStrandsL = LEDET.Inputs.nStrands_inGroup
        nStrandsL = np.int_(nStrandsL)
        DStrandsL = LEDET.Inputs.ds_inGroup

        # Uneven strand correction
        # If the number of strands in the conductor of a group is odd, change it to an even number and adjust the strand diameter to maintain the same cross-section
        # This is needed because some electro-magnetic calculation programs, such as ROXIE, only accept an even number of strands in the magnetic field map
        if any(nStrandsL % 2) and any(nStrandsL != 1):
            self.customPrint('WARNING: The number of strands in the conductor of a group is odd. The number of strands will be reduced by 1, and the corresponding strand diameter will be increased by sqrt(Ns/(Ns-1)) to maintain the same strand cross-section.')
            for g in range(nGroupsDefined):
                if ((nStrandsL[g] % 2)==1) and (nStrandsL[g]>1):
                    DStrandsL[g]=DStrandsL[g]*np.sqrt(nStrandsL[g]/(nStrandsL[g]-1)) # Scale the strand diameter
                    nStrandsL[g]=nStrandsL[g]-1 # Reduce the number of strands by 1


        nS = np.repeat(nStrandsL, nT)  # Number of strands in each half-turn

        strandToHalfTurn = np.int_(strandToHalfTurn)

        #polarity from LEDET
        #polaritiesL1 = np.repeat(LEDET.Inputs.polarities_inGroup, nT)  # polarity for each half turn
        #polarities = np.repeat(polaritiesL1, nS)  # polarity for each strand
        #polarities = polarities.astype(np.int64)

        #polarity from Roxy
        polarities = np.sign(I)
        polarities = polarities.astype(np.int64)


        # Calculate group to which each half-turn belongs
        indexTstart = np.hstack([1, 1 + np.cumsum(nT[:-1])]);
        indexTstop = np.cumsum(nT);
        HalfTurnToGroup = np.zeros((1, nHalfTurns), dtype=int)
        HalfTurnToGroup = HalfTurnToGroup[0]
        HalfTurnToCoilSection = np.zeros((1, nHalfTurns), dtype=int)
        HalfTurnToCoilSection = HalfTurnToCoilSection[0]
        for g in range(1, nGroupsDefined + 1):
            HalfTurnToGroup[indexTstart[g - 1] - 1:indexTstop[g - 1]] = g
            HalfTurnToCoilSection[indexTstart[g - 1] - 1:indexTstop[g - 1]] = LEDET.Inputs.GroupToCoilSection[g - 1]

        # Calculate group to which each strand belongs
        indexSstart = np.hstack([1, 1 + np.cumsum(nS[:-1])]);
        indexSstop = np.cumsum(nS);
        strandToGroup = np.zeros((1, sum(nS)), dtype=int)
        strandToGroup = strandToGroup[0]
        strandToCoilSection = np.zeros((1, sum(nS)), dtype=int)
        strandToCoilSection = strandToCoilSection[0]
        for ht in range(1, nHalfTurns + 1):
            strandToGroup[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToGroup[ht - 1]
            strandToCoilSection[indexSstart[ht - 1] - 1:indexSstop[ht - 1]] = HalfTurnToCoilSection[ht - 1]

        # Calculate diameter of each strand
        Ds = np.zeros((1, sum(nS)), dtype=float)
        Ds = Ds[0]
        for g in range(1, nGroupsDefined + 1):
            Ds[np.where(strandToGroup == g)] = LEDET.Inputs.ds_inGroup[g - 1]

        # New groups (called turn-groups in specific cases) since the coupling coefficient of the original groups can't be calculated correctly
        turnGroup_ind = int(nGroupsDefined / 2)
        strandToTurnGroup = np.concatenate((strandToGroup[strandToGroup < turnGroup_ind + 1],strandToGroup[strandToGroup > turnGroup_ind] - turnGroup_ind))
        HalfTurnToTurnGroup = HalfTurnToGroup.copy()
        HalfTurnToTurnGroup[HalfTurnToTurnGroup>turnGroup_ind] = HalfTurnToTurnGroup[HalfTurnToTurnGroup>turnGroup_ind]-turnGroup_ind

        # number of half turns in each turn-group
        nTG = nT[:turnGroup_ind] + nT[turnGroup_ind:]

        self.customPrint(str(max(strandToTurnGroup)) + ' turn-groups defined.')

        #Turns to group
        TurnToGroup=HalfTurnToGroup[HalfTurnToGroup < turnGroup_ind + 1]

        # Electrical order
        EO_turns = LEDET.Inputs.el_order_half_turns
        EO_turns = np.int_(EO_turns[EO_turns<nTurns+1])
        temp = TurnToGroup[EO_turns - 1] # The group of each turn in electrical order
        EO_groups = temp[0]
        for i in range(1,len(temp)): # Removing repeat values
            if temp[i-1] != temp[i]:
                EO_groups=np.append(EO_groups,temp[i])
        # A test could be to check if len(EO_groups) == turnGroup_ind

        # Capacitor specifics
        #magnets_name = []
        #for i in range(0, a.nrows):
        #    magnets_name.append(a.cell(i, 0).value)
        #ind = magnets_name.index(nameMagnet)

        #magnets_columns = []
        #for i in range(0, a.ncols):
        #    magnets_columns.append(a.cell(0, i).value)

        epsR_LayerToInner = b.cell(ind, magnets_columns.index('epsR_LayerToInner')).value
        epsR_LayerToOuter = b.cell(ind, magnets_columns.index('epsR_LayerToOuter')).value
        epsR_WideFirst = b.cell(ind, magnets_columns.index('epsR_WideFirst')).value
        epsR_WideLast = b.cell(ind, magnets_columns.index('epsR_WideLast')).value
        epsR_BetweenLayers = b.cell(ind, magnets_columns.index('epsR_BetweenLayers')).value

        hIns_LayerToInner = b.cell(ind, magnets_columns.index('hIns_LayerToInner (m)')).value
        hIns_LayerToOuter = b.cell(ind, magnets_columns.index('hIns_LayerToOuter (m)')).value
        hIns_WideFirst = b.cell(ind, magnets_columns.index('hIns_WideFirst (m)')).value
        hIns_WideLast = b.cell(ind, magnets_columns.index('hIns_WideLast (m)')).value
        hIns_BetweenLayers = b.cell(ind, magnets_columns.index('hIns_BetweenLayers (m)')).value

        try:
            narrow_inner = np.int_(b.cell(ind, magnets_columns.index('Narrow_Inner')).value.split(','))
        except:
            narrow_inner = [int(b.cell(ind, magnets_columns.index('Narrow_Inner')).value)]

        try:
            narrow_outer = np.int_(b.cell(ind, magnets_columns.index('Narrow_Outer')).value.split(','))
        except:
            narrow_outer = [int(b.cell(ind, magnets_columns.index('Narrow_Outer')).value)]

        try:
            wide_first = np.int_(b.cell(ind, magnets_columns.index('Wide_FirstTurn')).value.split(','))
        except:
            wide_first = [int(b.cell(ind, magnets_columns.index('Wide_FirstTurn')).value)]

        try:
            wide_last = np.int_(b.cell(ind, magnets_columns.index('Wide_LastTurn')).value.split(','))
        except:
            wide_last = [int(b.cell(ind, magnets_columns.index('Wide_LastTurn')).value)]


        # self section
        self.nameMagnet = nameMagnet
        self.LEDET = LEDET
        self.x = x
        self.y = y
        self.nT = nT
        self.nTG = nTG
        self.strandToHalfTurn = strandToHalfTurn
        self.strandToGroup = strandToGroup
        self.strandToTurnGroup = strandToTurnGroup
        self.HalfTurnToGroup = HalfTurnToGroup
        self.HalfTurnToTurnGroup = HalfTurnToTurnGroup
        self.TurnToGroup = TurnToGroup
        self.nStrandsL = nStrandsL
        self.nS = nS
        self.Ds = Ds
        self.polarities = polarities
        self.nHalfTurns = nHalfTurns
        self.nTurns = nTurns
        self.turnGroup_ind = turnGroup_ind
        self.nGroupsDefined = nGroupsDefined
        self.eospath = eospath
        self.EO_groups = EO_groups
        self.EO_turns = EO_turns

        self.epsR_LayerToInner = epsR_LayerToInner
        self.epsR_LayerToOuter = epsR_LayerToOuter
        self.epsR_WideFirst = epsR_WideFirst
        self.epsR_WideLast = epsR_WideLast
        self.epsR_BetweenLayers = epsR_BetweenLayers
        self.hIns_LayerToInner = hIns_LayerToInner
        self.hIns_LayerToOuter = hIns_LayerToOuter
        self.hIns_WideFirst = hIns_WideFirst
        self.hIns_WideLast = hIns_WideLast
        self.hIns_BetweenLayers = hIns_BetweenLayers

        self.narrow_inner = narrow_inner
        self.narrow_outer = narrow_outer
        self.wide_first = wide_first
        self.wide_last = wide_last

        self.flag_R_Par = flag_R_Par
        self.R_Par = R_Par
        self.flag_E_loops = flag_E_loops
        self.E_loops = E_loops
        self.F_SCALE_C_GROUND = F_SCALE_C_GROUND
        self.F_SCALE_C_T2T = F_SCALE_C_T2T
        self.F_SCALE_L = F_SCALE_L
        self.F_SCALE_R = F_SCALE_R
        self.flag_strandCorrection = flag_strandCorrection
        self.flag_sumTurnToTurn = flag_sumTurnToTurn
        self.flag_writeOutput = flag_writeOutput
        self.dev_max = dev_max
        self.flag_CapacitanceToInner = flag_CapacitanceToInner
        self.flag_CapacitanceToOuter = flag_CapacitanceToOuter
        self.flag_CapacitanceWide = flag_CapacitanceWide
        self.flag_T2TCapWidth = flag_T2TCapWidth
        self.flag_T2TCapHeight = flag_T2TCapHeight
        self.pointsPerDecade = pointsPerDecade
        self.startFrequency = startFrequency
        self.stopFrequency = stopFrequency
        # self.Coil_Select = Coil_Select
        self.flag_writeFile = flag_writeFile


    def epsRCabIns(self):
        # Used to translate the insulation type from LEDET to an usuable value in calculations.
        epsR_CabIns = self.LEDET.Inputs.insulationType_inGroup
        epsR_CabIns = np.where(epsR_CabIns == 1, 4.4 , epsR_CabIns) # G10
        epsR_CabIns = np.where(epsR_CabIns == 2, 3.4 , epsR_CabIns) # kapton
        return epsR_CabIns

    def SelfMutualInductanceCalc(self,type):
        # This function uses the 'calculateInductance' function from the 'SelfMutualInductanceCalculation' dataclass
        # to calculate the mutual-inductance (M) matrixes based on turns and groups.
        # The calculated turn based M-matrix is compared to the one from the LEDET file, to check if they are a match.
        # The amount of deviation is printed. However since deviation aren't necesarilly cause for concern the code
        # continous, no matter the result of the deviation test.
        # Some corrections are made, so that the length of the magnet, as well as the yoke effect is taken into account.
        # Finally the coupling coefficients (k) matrixes are calculated since PSpice needs those.
        #
        # type: The type of call to the function, it decides which alterations are done to the calculations
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind
        nGroupsDefined = self.nGroupsDefined

        flag_strandCorrection = self.flag_strandCorrection
        flag_sumTurnToTurn = self.flag_sumTurnToTurn
        flag_writeOutput = self.flag_writeOutput
        dev_max = self.dev_max

        if type=='Change_Ds_to_hBare':
            Ds = np.zeros((1, sum(nS)), dtype=float)
            Ds = Ds[0]
            for g in range(1,nGroupsDefined+1):
                if nStrandsL[g-1] == 1:
                    Ds[np.where(strandToGroup==g)] = LEDET.Inputs.hBare_inGroup[g-1]
                else:
                    Ds[np.where(strandToGroup==g)] = LEDET.Inputs.ds_inGroup[g-1]
        else:
            Ds = self.Ds

        coil = SelfMutualInductanceCalculation(x, y, polarities, nS, Ds, strandToHalfTurn, strandToTurnGroup,flag_strandCorrection, flag_sumTurnToTurn, flag_writeOutput,nameMagnet)  # Coilsection changed to groups

        if self.flag_print:
            # Calculate self-mutual inductance between half-turns, turns, and turn-groups, per unit length [H/m]
            print('')
            M_halfTurns_calculated_m, M_turns_calculated_m, M_groups_calculated_m, L_mag0_calculated_m = coil.calculateInductance(x, y, polarities, nS, Ds, strandToHalfTurn, strandToTurnGroup,flag_strandCorrection=0)  # Coilsection changed to groups
        else:
            with HiddenPrints():
                # Calculate self-mutual inductance between half-turns, turns, and turn-groups, per unit length [H/m]
                M_halfTurns_calculated_m, M_turns_calculated_m, M_groups_calculated_m, L_mag0_calculated_m = coil.calculateInductance(x, y, polarities, nS, Ds, strandToHalfTurn, strandToTurnGroup,flag_strandCorrection=0)  # Coilsection changed to groups

        # Self-mutual inductance between turn-groups, per unit length [H/m] (replaces coilsection)
        M_groups0_m = M_groups_calculated_m
        # Self-mutual inductances between turns, per unit length [H/m]
        M_InductanceBlock_m = M_turns_calculated_m
        # Total magnet self-mutual inductance, per unit length [H/m]
        L_mag0_m = L_mag0_calculated_m

        self.customPrint('')
        self.customPrint('Total magnet self-inductance per unit length: ' + str(L_mag0_m) + ' H/m')

        # Defining to which inductive block each half-turn belongs
        HalfTurnToInductanceBlock = range(1, int(nTurns + 1))
        HalfTurnToInductanceBlock = []
        for i in range(2):
            for j in range(1, int(nTurns+ 1)):
                HalfTurnToInductanceBlock.append(j)

        # Deviation test
        M_dev = abs(M_InductanceBlock_m - LEDET.Inputs.M_InductanceBlock_m)  # deviation of each element
        M_dev_rel = M_dev / abs(M_InductanceBlock_m)  # relative deviation of each element
        nDev = sum(sum(M_dev_rel > dev_max))  # number of deviations in the entire matrix
        sizeM = len(M_dev) * len(M_dev[0])
        self.customPrint('')
        self.customPrint('Number of deviations: ' + str(nDev) + ' out of ' + str(sizeM))

        # Iron yoke effect
        M_groups_m = M_groups0_m * LEDET.Inputs.fL_L[0]
        M_turns_m = M_turns_calculated_m * LEDET.Inputs.fL_L[0]
        L_mag0_m = L_mag0_calculated_m * LEDET.Inputs.fL_L[0]

        # Self-mutual inductances between turn-groups
        M_groups = M_groups_m * LEDET.Inputs.l_magnet
        # Self-mutual inductances between turns
        M_turns = M_turns_m * LEDET.Inputs.l_magnet
        # Total magnet self-mutual inductance
        L_mag0 = L_mag0_m * LEDET.Inputs.l_magnet
        self.Total_Inductance = L_mag0
        self.customPrint('')
        self.customPrint('Total inductance:')
        s = str(L_mag0)+' H'
        self.customPrint(s)

        # Changed to M to L for easier comparison to older code
        L_turns = M_turns
        L_groups = M_groups

        # Matrix calc version
        L_turns_diag = np.diagonal(L_turns)
        L_turns_diag_rep = np.tile(L_turns_diag, (len(L_turns), 1))  # this replicates the effect of L_xx[i][i] (or [j][j] i'm not sure, but it shouldn't matter)
        denom_turns = np.sqrt(L_turns_diag_rep.T * L_turns_diag_rep)
        k_turns = L_turns / denom_turns  # matrix alt to k_turns[i][j]=L_turns[i][j]/np.sqrt(L_turns[j][j]*L_turns[i][i])
        L_groups_diag = np.diagonal(L_groups)
        L_groups_diag_rep = np.tile(L_groups_diag, (len(L_groups), 1))  # this replicates the effect of L_xx[i][i] (or [j][j] i'm not sure, but it shouldn't matter)
        denom_groups = np.sqrt(L_groups_diag_rep.T * L_groups_diag_rep)
        k_groups = L_groups / denom_groups  # matrix alt to k_groups[i][j]=L_groups[i][j]/np.sqrt(L_groups[j][j]*L_groups[i][i])

        # replace diagonal with 0's
        np.fill_diagonal(k_turns, 0)
        np.fill_diagonal(k_groups, 0)

        self.customPrint('')
        self.customPrint('max |k_turns| (should be lower than 1):')
        self.customPrint(np.max(abs(k_turns)))

        self.customPrint('')
        self.customPrint('max |k_groups| (should be lower than 1):')
        self.customPrint(np.max(abs(k_groups)))

        return L_turns, L_groups, k_turns, k_groups

    def SelfMutualInductance(self):
        # This function uses the SelfMutualInductanceCalc internal function to
        # calculate the inductance and coupling coefficients.
        # The function furthermore checks for coupling coeffecients above 1
        # and either throws an error or recalculates based on augmented values

        nS = self.nS
        L_turns, L_groups, k_turns, k_groups = self.SelfMutualInductanceCalc('Initial_call') #The initial call of the function

        if np.max(abs(k_turns))>1 or np.max(abs(k_groups))>1:
            self.customPrint('')
            self.customPrint('Initial Self-Mutual Inductance calculation returned k>1')
            if any(nS==1):
                L_turns, L_groups, k_turns, k_groups = self.SelfMutualInductanceCalc('Change_Ds_to_hBare') #Change Ds to the height of conductor
                if np.max(abs(k_turns))>1 or np.max(abs(k_groups))>1:
                     raise Exception('k>1 for single-strand magnet')
                     sys.exit(1)
            else:
                 raise Exception('k>1 for non single-strand magnet')
                 sys.exit(1)

        if len(k_turns) >= 1414: #A length of above 1414 will give a matrix of around 2 million values, which will require about 1 million lines
            self.customPrint('')
            self.customPrint('Warning: Netlist will be over 1 million lines long, might cause memory shortage errors')

        return L_turns, L_groups, k_turns, k_groups

    def Resistance(self):
        # The resistance based on turns and groups is calculated.
        # More specifically the resistance of the half turns in each group is calculated with the formula shown below:
        # R = rho_Cu / (pi * strand_diameter^2 / 4 * nStrandsL * fraction_Cu) * magnetic_length
        # Then these resistance values are repeated and summed to create the turn and group based resistance.
        # All the needed information is preloaded into the model by the 'init' function.
        LEDET = self.LEDET
        nT = self.nT
        nTG = self.nTG
        nStrandsL = self.nStrandsL
        nS = self.nS
        nS = self.nS
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind

        rho_Cu = 1.6965e-8
        strand_diameter = LEDET.Inputs.ds_inGroup
        fraction_Cu = 1 - LEDET.Inputs.f_SC_strand_inGroup
        magnetic_length = LEDET.Inputs.l_mag_inGroup
        R_ght = rho_Cu / (np.pi * strand_diameter * strand_diameter / 4 * nStrandsL * fraction_Cu) * magnetic_length  # Resistance of each EACH HALF TURN in a specific group
        R_turns = np.repeat(R_ght[0:int(len(nT) / 2)] + R_ght[int(len(nT) / 2):len(nT)], nT[0:int(len(nT) / 2)])  # len(nT) is assumed to be even!
        R_groups = R_ght[:turnGroup_ind] * nTG
        self.Total_Resistance = sum(R_turns)

        #print('R_turns = ')
        #print(R_turns)
        #print('R_groups = ')
        #print(R_groups)

        return R_turns, R_groups

    def groupToHalfTurnGen(self,groups,a_f_l):
        # From a list of the half-turn based groups find the halfturns in each group and concatenate them to an array.
        #
        # Input :
        # groups: The groups that needs to be translated to halfturns
        # a_f_l : either 'All', 'First' or 'Last', depending on if all, only the first or only the last of the halfturns of each group is needed
        HalfTurnToGroup = self.HalfTurnToGroup
        halfturns = np.array([])
        for i in range(len(groups)):
            temp = HalfTurnToGroup == groups[i]
            new = [index for index, value in enumerate(temp) if value == 1]
            if a_f_l == 'First':
                new = np.amin(new)
            elif a_f_l == 'Last':
                new = np.amax(new)
            elif a_f_l != 'All':
                customPrint('groupToHalfTurnGen passed unknown a_f_l, all halfturns are passed.')
            # 'ALl' is not strictly needed anything that is not 'First' or 'Last'
            halfturns = np.int_(np.append(halfturns,new)) # find the indexes for the halfturns in groups[i]
        halfturns=halfturns+1
        return halfturns

    def CapCalc(self,From,To,Contact_Area,ins_epsR,ins_height):
        # Calculates the capacitance for the halfturns in the To and From arrays.
        #
        # IF USED TO CALCULATE TURN2TURN CAPACITACE THEN THE FIRST 2 ARRAYs
        # IN 'ins_epsR' AND 'ins_height' NEEDS TO BE THAT OF THE TURN INSULATION
        # THESE ARE THEN USED FOR THE TO AND FROM HALFTURN, RESPECTIVELY.
        #
        # Inputs        :
        # From          : The halfturns where the capacitor is placed from
        # To            : The halfturns where the capacitor is placed to (If To = [0], then the capacitors go to ground)
        # Contact_Area  : The relevant contact area for all the groups of the magnet
        # ins_epsR      : An array of all the relevant epsR of the insulation layers (Each insulation layer is modelled as a
        #                 capacitor. These capacitors are then series connected)
        # ins_height    : The thickness of the relevant insulation layers (Can both be single values or array based
        #               : on the groups)

        HalfTurnToGroup = self.HalfTurnToGroup

        eps0 = 1 / (4 * np.pi * 1E-7 * 299792458 ** 2)

        C = []
        if To[0]==0: # To ground
            ins_epsR = np.array(ins_epsR).T
            ins_height = np.array(ins_height).T
            for i in range(len(From)):
                i_From = HalfTurnToGroup[From[i] - 1] - 1
                C_Array = eps0 * ins_epsR[i_From] * (Contact_Area[i_From] / ins_height[i_From])
                C_Temp = 1 / np.sum(1/C_Array)
                C = np.append(C, C_Temp)
        else:
            for i in range(len(From)):
                i_From = HalfTurnToGroup[From[i] - 1] - 1
                i_To = HalfTurnToGroup[To[i] - 1] - 1
                CA_From = Contact_Area[i_From]  # Contact area of the from-halfturn
                CA_To = Contact_Area[i_To]  # Contact area of the to-halfturn
                if CA_From < CA_To:  # find index of the minimum
                    i_CA = i_From
                else:
                    i_CA = i_To

                # Create the correct arrays for epsR and height -> [From,To,Additional_Layer_1,...,Additional_Layer_X]
                temp_epsR = []
                temp_height = []
                for k in range(len(ins_epsR)):
                    if k == 1: # The 'To' halfturn insulation
                        temp_epsR.append(ins_epsR[k][i_To])
                        temp_height.append(ins_height[k][i_To])
                    else:
                        temp_epsR.append(ins_epsR[k][i_From])
                        temp_height.append(ins_height[k][i_From])

                temp_epsR = np.array(temp_epsR)
                temp_height = np.array(temp_height)

                C_Array = eps0 * temp_epsR * (Contact_Area[i_CA] / temp_height)
                C_Temp = 1 / np.sum(1/C_Array)
                C = np.append(C, C_Temp)
        return C

    def CapSum(self,C,From,To):
        # Sums capacitances in parallel by checking if To and From match an already existen pair of nodes.
        # If the pair exist C is added to the already existing value, if not the value and node pair are appended to their respective arrays.
        # The function automatically disregards any shorted capacitances. (Useful for summation of groups)
        C_new = []
        From_new = []
        To_new = []
        for i in range(len(C)):
            if To[i] != From[i]:
                if sum((To_new == To[i]) * (From_new == From[i])) or sum((From_new == To[i]) * (To_new == From[i])):  # check if current combination of contact to and from already exist
                    C_new[(To_new == To[i]) * (From_new == From[i])] = \
                    C_new[(To_new == To[i]) * (From_new == From[i])] + \
                    C[i]
                    # Both cases needs to be accounted for
                    C_new[(From_new == To[i]) * (To_new == From[i])] = \
                    C_new[(From_new == To[i]) * (To_new == From[i])] + \
                    C[i]
                else:
                    C_new = np.append(C_new, C[i])
                    From_new = np.append(From_new, From[i])
                    To_new = np.append(To_new, To[i])

        From_new = np.int_(From_new)
        To_new = np.int_(To_new)

        return C_new, From_new, To_new

    def CapacitanceToGround(self):
        # This function calculates the capacitance to ground from each turn and group.
        # The capacitance is calculated under the assumption that the turns and groups can be approximated as parallel
        # plates. And hence the formula shown below can be used:
        # C = eps_0 * eps_r * A / d, where eps_0 is the vacuum permitivity, eps_r is the relative permitivity of the
        # insulation, A is the contact area, and d is the distance between plates.
        # Different types of insulation is dealt with by modelling each type of insulation as it own capacitor,
        # which are then placed in series.
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        HalfTurnToTurnGroup = self.HalfTurnToTurnGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        Ds = self.Ds
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind

        epsR_CabIns = self.epsRCabIns()

        # needs to be repeated for each group to fit into 2D array
        epsR_LayerToInner = np.repeat(self.epsR_LayerToInner,len(epsR_CabIns))
        epsR_LayerToOuter = np.repeat(self.epsR_LayerToOuter,len(epsR_CabIns))
        epsR_WideFirst = np.repeat(self.epsR_WideFirst,len(epsR_CabIns))
        epsR_WideLast = np.repeat(self.epsR_WideLast,len(epsR_CabIns))
        epsR_BetweenLayers = np.repeat(self.epsR_BetweenLayers,len(epsR_CabIns))
        hIns_LayerToInner = np.repeat(self.hIns_LayerToInner,len(epsR_CabIns))
        hIns_LayerToOuter = np.repeat(self.hIns_LayerToOuter,len(epsR_CabIns))
        hIns_WideFirst = np.repeat(self.hIns_WideFirst,len(epsR_CabIns))
        hIns_WideLast = np.repeat(self.hIns_WideLast,len(epsR_CabIns))
        hIns_BetweenLayers = np.repeat(self.hIns_BetweenLayers,len(epsR_CabIns))

        flag_CapacitanceToInner = self.flag_CapacitanceToInner
        flag_CapacitanceToOuter = self.flag_CapacitanceToOuter
        flag_CapacitanceWide = self.flag_CapacitanceWide
        # LEDET inputs

        l_mag_inGroup = LEDET.Inputs.l_mag_inGroup
        wBare_inGroup = LEDET.Inputs.wBare_inGroup
        hBare_inGroup = LEDET.Inputs.hBare_inGroup
        wIns_inGroup = LEDET.Inputs.wIns_inGroup
        hIns_inGroup = LEDET.Inputs.hIns_inGroup

        eps0 = 1 / (4 * np.pi * 1E-7 * 299792458 ** 2)

        C_half = np.array([]) # array containing all the capacitors to ground (halfturns)
        ind_half = np.array([]) # indexes for C_half
        if flag_CapacitanceToInner and self.narrow_inner[0] != 0:
            narrow_inner=np.array(self.narrow_inner)
            #narrow_inner = np.concatenate((narrow_inner,narrow_inner+turnGroup_ind))
            narrow_inner = self.groupToHalfTurnGen(narrow_inner,'All')
            CA_n_i = (l_mag_inGroup * (hBare_inGroup + 2 * hIns_inGroup)) # Contact Area from the narrow side of the turns to the inner grounding
            C_n_i = self.CapCalc(narrow_inner, [0], CA_n_i, [epsR_CabIns,epsR_LayerToInner], [hIns_inGroup,hIns_LayerToInner])
            ind_half = np.append(ind_half,narrow_inner)
            C_half = np.append(C_half,C_n_i)

        if flag_CapacitanceToOuter and self.narrow_outer[0] != 0:
            narrow_outer = np.array(self.narrow_outer)
            #narrow_outer = np.concatenate((narrow_outer,narrow_outer+turnGroup_ind))
            narrow_outer = self.groupToHalfTurnGen(narrow_outer,'All')
            CA_n_o = (l_mag_inGroup * (hBare_inGroup + 2 * hIns_inGroup))  # Contact Area from the narrow side of the turns to the outer grounding
            C_n_o = self.CapCalc(narrow_outer, [0], CA_n_o, [epsR_CabIns,epsR_LayerToOuter], [hIns_inGroup,hIns_LayerToOuter])
            ind_half = np.append(ind_half,narrow_outer)
            C_half = np.append(C_half,C_n_o)

        if flag_CapacitanceWide and self.wide_first[0] != 0:
            wide_first = np.array(self.wide_first)
            #wide_first = np.concatenate((wide_first,wide_first+turnGroup_ind))
            wide_first = self.groupToHalfTurnGen(wide_first,'First')
            CA_w_f = (l_mag_inGroup * (wBare_inGroup + 2 * wIns_inGroup))  # Contact Area from the wide side of the turns to the inner grounding (CHECK!)
            C_w_f = self.CapCalc(wide_first, [0], CA_w_f, [epsR_CabIns,epsR_WideFirst], [hIns_inGroup,hIns_WideFirst])
            ind_half = np.append(ind_half,wide_first)
            C_half = np.append(C_half,C_w_f)

        if flag_CapacitanceWide and self.wide_last[0] != 0:
            wide_last = np.array(self.wide_last)
            #wide_last = np.concatenate((wide_last,wide_last+turnGroup_ind))
            wide_last = self.groupToHalfTurnGen(wide_last,'Last')
            CA_w_l = (l_mag_inGroup * (wBare_inGroup + 2 * wIns_inGroup))  # Contact Area from the wide side of the turns to the outer grounding (CHECK!)
            C_w_l = self.CapCalc(wide_last, [0], CA_w_l, [epsR_CabIns,epsR_WideLast], [hIns_inGroup,hIns_WideLast])
            ind_half = np.append(ind_half,wide_last)
            C_half = np.append(C_half,C_w_l)

        ind_half = np.int_(ind_half)

        ind_turns0 = ind_half.copy()

        ind_turns0[ind_turns0 > nTurns] = ind_turns0[ind_turns0 > nTurns] - nTurns #indexes for turns

        ind_groups0 = HalfTurnToTurnGroup[ind_half-1] # indexes for turn-groups



        # dc -> don't care
        C_turns, ind_turns, dc = self.CapSum(C_half, ind_turns0, np.zeros((len(ind_turns0),1))) # the To input/output is 0 in all cases, since they are grounded
        C_groups, ind_groups, dc = self.CapSum(C_half, ind_groups0, np.zeros((len(ind_groups0),1)))

        self.Total_Capacitance = sum(C_turns)


        return C_turns, ind_turns, C_groups, ind_groups

    def CapacitanceT2T(self):
        # Calculates the capacitance between turns and between groups.
        # The calculation is done similairly to the capacitance to ground calculation and is based on heat exchange
        # information from the LEDET file.
        # The capacitance is found between each half-turn and is then summed, since the capacitors would be in parallel,
        # to create the value for each turn.
        # To create the group capacitance the same is done. However since there will be capacitance between turns inside
        # each group these capacitances are disregarded, since they are shorted in this model.
        nameMagnet = self.nameMagnet
        LEDET = self.LEDET
        x = self.x
        y = self.y
        nT = self.nT
        nTG = self.nTG
        strandToHalfTurn = self.strandToHalfTurn
        strandToGroup = self.strandToGroup
        strandToTurnGroup = self.strandToTurnGroup
        HalfTurnToGroup = self.HalfTurnToGroup
        nStrandsL = self.nStrandsL
        nS = self.nS
        Ds = self.Ds
        polarities = self.polarities
        nHalfTurns = self.nHalfTurns
        nTurns = self.nTurns
        turnGroup_ind = self.turnGroup_ind
        HalfTurnToGroup = self.HalfTurnToGroup

        epsR_CabIns = self.epsRCabIns()

        # needs to be repeated for each group to fit into 2D array
        epsR_BetweenLayers = np.repeat(self.epsR_BetweenLayers,len(epsR_CabIns))
        hIns_BetweenLayers = np.repeat(self.hIns_BetweenLayers,len(epsR_CabIns))


        flag_T2TCapWidth = self.flag_T2TCapWidth
        flag_T2TCapHeight = self.flag_T2TCapHeight

        l_mag_inGroup = LEDET.Inputs.l_mag_inGroup
        wBare_inGroup = LEDET.Inputs.wBare_inGroup
        hBare_inGroup = LEDET.Inputs.hBare_inGroup
        wIns_inGroup = LEDET.Inputs.wIns_inGroup
        hIns_inGroup = LEDET.Inputs.hIns_inGroup

        eps0 = 1 / (4 * np.pi * 1E-7 * 299792458 ** 2)

        Capacity_T2T_Width = []
        Capacity_T2T_Height = []

        ContactW_From = np.int_(LEDET.Inputs.iContactAlongWidth_From)
        ContactW_To = np.int_(LEDET.Inputs.iContactAlongWidth_To)
        ContactH_From = np.int_(LEDET.Inputs.iContactAlongHeight_From)
        ContactH_To = np.int_(LEDET.Inputs.iContactAlongHeight_To)

        Contact_Area_Width = (l_mag_inGroup * (wBare_inGroup + 2 * wIns_inGroup))
        Contact_Area_Height = (l_mag_inGroup * (hBare_inGroup + 2 * hIns_inGroup))

        if flag_T2TCapWidth:
            Capacity_T2T_Width = self.CapCalc(ContactW_From, ContactW_To, Contact_Area_Width, [epsR_CabIns,epsR_CabIns], [wIns_inGroup,wIns_inGroup])
        #     for i in range(len(ContactW_From)):
        #         i_Width_From = HalfTurnToGroup[ContactW_From[i] - 1] - 1
        #         i_Width_To = HalfTurnToGroup[ContactW_To[i] - 1] - 1
        #         CA_From = Contact_Area_Width[i_Width_From]  # Contact area of the from cable
        #         CA_To = Contact_Area_Width[i_Width_To]  # Contact area of the to cable
        #         if CA_From < CA_To:  # find index of the minimum
        #             i_Width = i_Width_From
        #         else:
        #             i_Width = i_Width_To
        #
        #         Capacity_T2T_Width_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Width_To] * (Contact_Area_Width[i_Width] / (wIns_inGroup[i_Width_To]))) \
        #                                      + 1 / (eps0 * epsR_CabIns[i_Width_From] * (Contact_Area_Width[i_Width] / (wIns_inGroup[i_Width_From]))))
        #         Capacity_T2T_Width = np.append(Capacity_T2T_Width, Capacity_T2T_Width_Temp)
        else:
            for i in range(len(ContactW_From)):
                Capacity_T2T_Width = np.append(Capacity_T2T_Width, 0)

        if flag_T2TCapHeight:
            Capacity_T2T_Height = self.CapCalc(ContactH_From, ContactH_To, Contact_Area_Height, [epsR_CabIns,epsR_CabIns,epsR_BetweenLayers], [wIns_inGroup,wIns_inGroup,hIns_BetweenLayers])
        #     for i in range(len(ContactH_From)):
        #         i_Height_From = HalfTurnToGroup[ContactH_From[i] - 1] - 1
        #         i_Height_To = HalfTurnToGroup[ContactH_To[i] - 1] - 1
        #         CA_From = Contact_Area_Height[i_Height_From]  # Contact area of the from cable
        #         CA_To = Contact_Area_Height[i_Height_To]  # Contact area of the to cable
        #         if CA_From < CA_To:  # find index of the minimum contact area
        #             i_Height = i_Height_From
        #         else:
        #             i_Height = i_Height_To
        #
        #         # is this correct, or should it be some average epsR_CabIns, and with a thickness of wIns_inGroup[i_Width_To] + wIns_inGroup[i_Width_From]
        #         Capacity_T2T_Height_Temp = 1 / (1 / (eps0 * epsR_CabIns[i_Height_To] * (Contact_Area_Height[i_Height] / (hIns_inGroup[i_Height_To]))) \
        #                                       + 1 / (eps0 * epsR_BetweenLayers * (Contact_Area_Height[i_Height] / (hIns_BetweenLayers))) \
        #                                       + 1 / (eps0 * epsR_CabIns[i_Height_From] * (Contact_Area_Width[i_Height] / (hIns_inGroup[i_Height_From]))))
        #         Capacity_T2T_Height = np.append(Capacity_T2T_Height, Capacity_T2T_Height_Temp)
        else:
            for i in range(len(ContactH_From)):
                Capacity_T2T_Height = np.append(Capacity_T2T_Height, 0)

        # Concatenate T2T capacitance, should be easier to write the netlist
        # first width then height!
        Capacity_T2T = np.concatenate((Capacity_T2T_Width, Capacity_T2T_Height))
        Contact_From = np.concatenate((ContactW_From, ContactH_From))
        Contact_To = np.concatenate((ContactW_To, ContactH_To))

        # change contact to and from to be for turns instead of half turns
        Contact_From_t0 = Contact_From
        Contact_To_t0 = Contact_To
        Contact_From_t0[Contact_From_t0 > nTurns] = Contact_From_t0[Contact_From_t0 > nTurns] - nTurns
        Contact_To_t0[Contact_To_t0 > nTurns] = Contact_To_t0[Contact_To_t0 > nTurns] - nTurns

        # change contact to and from to be for groups instead of half turn
        Contact_From_g0 = HalfTurnToGroup[Contact_From-1]
        Contact_To_g0 = HalfTurnToGroup[Contact_To-1]

        Capacity_T2T_turns, Contact_From_turns, Contact_To_turns = self.CapSum(Capacity_T2T, Contact_From_t0, Contact_To_t0)
        Capacity_T2T_groups, Contact_From_groups, Contact_To_groups = self.CapSum(Capacity_T2T, Contact_From_g0, Contact_To_g0)


        return Capacity_T2T_turns, Contact_From_turns, Contact_To_turns, Capacity_T2T_groups, Contact_From_groups, Contact_To_groups

    def netlist (self,L,R,C,C_ind,k,Capacity_T2T_new,Contact_From_new,Contact_To_new):
        # Creates a netlist of all the calculated components as well as additional custom components and scaling
        # factors, which can be changed later in the generated netlist.
        # This function only creates one netlist, and hence should be run with different inputs for the turn and group
        # based models.
        # This function supports implementation of a custom parallel resistance and an eddy current loops.
        #
        # NOTE: This function creates the netlist according to the electrical order of turns specified in the LEDET file.
        #
        # Input arguments
        # L                 : The self inductances of the model
        # R                 : The resistance of the model
        # C                 : The capacitance to ground of the model
        # k                 : The coupling coefficients of the model
        # Capacity_T2T_new  : The capacitance between turns/groups in the model
        # Contact_From_new  : An array of nodes to which the capacitance should be added (between Contact_To_new and
        #                     Contact_From_new)
        # Contact_To_new    : An array of nodes to which the capacitance should be added (between Contact_To_new and
        #                     Contact_From_new)
        flag_writeFile = self.flag_writeFile
        flag_R_Par = self.flag_R_Par
        R_Par = self.R_Par
        flag_E_loops = self.flag_E_loops
        E_loops = self.E_loops
        F_SCALE_C_GROUND = self.F_SCALE_C_GROUND
        F_SCALE_C_T2T = self.F_SCALE_C_T2T
        F_SCALE_L = self.F_SCALE_L
        F_SCALE_R = self.F_SCALE_R
        pointsPerDecade = self.pointsPerDecade
        startFrequency = self.startFrequency
        stopFrequency = self.stopFrequency
        # Coil_Select = self.Coil_Select
        turnGroup_ind = self.turnGroup_ind
        nTurns = self.nTurns
        LEDET = self.LEDET
        nT = self.nT
        nameMagnet = self.nameMagnet

        path_gateway = self.eospath + 'SWAN_projects/steam-notebooks/steam/*'

        # Launch a Gateway in a new Java process, this returns port
        port = launch_gateway(classpath=path_gateway)
        # JavaGateway instance is connected to a Gateway instance on the Java side
        gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
        # Get STEAM API Java classes
        MutualInductance = gateway.jvm.component.MutualInductance
        Netlist = gateway.jvm.netlist.Netlist
        CommentElement = gateway.jvm.netlist.elements.CommentElement
        GeneralElement = gateway.jvm.netlist.elements.GeneralElement
        GlobalParameterElement = gateway.jvm.netlist.elements.GlobalParameterElement
        ACSolverElement = gateway.jvm.netlist.solvers.ACSolverElement
        CircuitalPreconditionerSubcircuit = gateway.jvm.preconditioner.CircuitalPreconditionerSubcircuit
        TextFile = gateway.jvm.utils.TextFile
        CSVReader = gateway.jvm.utils.CSVReader

        # Turns flag
        flag_turn = self.nTurns == len(L)

        # Electrical order:
        nameOrder = np.arange(1, self.nTurns + 1)
        if flag_turn:
            nameOrder = self.EO_turns
        else:
            nameOrder = self.EO_groups


        # Coil section selection
        # if Coil_Select[0] != 0:
        #     GroupToCoilSelection = LEDET.Inputs.GroupToCoilSection[:turnGroup_ind]
        #     currentGroups = np.array([])
        #     currentTurns = np.array([])
        #     for i in range(len(Coil_Select)):
        #         temp = np.array([j for j, e in enumerate(GroupToCoilSelection) if e == Coil_Select[i]])+1
        #         currentGroups = np.append(currentGroups,temp)
        #     currentGroups = np.int_(currentGroups)
        #     sum_nT = np.append(1,np.cumsum(nT)+1)
        #     for i in range(len(currentGroups)):
        #         temp = range(sum_nT[currentGroups[i]-1],sum_nT[currentGroups[i]])
        #         currentTurns = np.append(currentTurns,temp)
        #     currentTurns = np.int_(currentTurns)
        #     if flag_turn:
        #         currentNotes = currentTurns
        #     else:
        #         currentNotes = currentGroups


        netlist = Netlist("")

        globalParameters_Parameters = ['F_SCALE_C_GROUND', 'F_SCALE_C_T2T', 'F_SCALE_L', 'F_SCALE_R']
        globalParameters_Values = [str.format('{}', F_SCALE_C_GROUND), str.format('{}', F_SCALE_C_T2T),
                                   str.format('{}', F_SCALE_L), str.format('{}', F_SCALE_R)]

        E_param_param = []
        E_param_values = []

        if flag_E_loops:
            for i in range(len(E_loops)):
                E_param_param = E_param_param + [str.format('L_EDDY{}', i + 1), str.format('R_EDDY{}', i + 1),
                                                 str.format('K_EDDY{}', i + 1)]
                E_param_values = E_param_values + [str.format('{}', E_loops[i][0]), str.format('{}', E_loops[i][1]),
                                                   str.format('{}', E_loops[i][2])]

            globalParameters_Parameters = globalParameters_Parameters + E_param_param
            globalParameters_Values = globalParameters_Values + E_param_values

        if flag_R_Par:
            globalParameters_Parameters = globalParameters_Parameters + ['R_Par']
            globalParameters_Values = globalParameters_Values + [str.format('{}', R_Par)]

        globalParameters_Parameters = a.create_string_array(gateway, globalParameters_Parameters)
        globalParameters_Values = a.create_string_array(gateway, globalParameters_Values)

        netlist.add(CommentElement("**** Global parameters ****"))
        netlist.add(GlobalParameterElement(globalParameters_Parameters, globalParameters_Values))

        netlist.add(CommentElement("* .STEP PARAM R_Par 10k, 100k, 10k"))

        nodesL = gateway.new_array(gateway.jvm.String, len(L), 2)
        nodesR = gateway.new_array(gateway.jvm.String, len(R), 2)


        GROUND_NODE = "00_mGND"

        for i in range(len(L)):
            if i == 0:
                nodesL[i][0] = str.format("{}in", i + 1)
            else:
                nodesL[i][0] = str.format("{}out", i)

            # L - negative (right terminal) - imid, e.g., 1mid
            nodesL[i][1] = str.format("{}mid", i + 1);

            # R_par - positive (left terminal) - imid, e.g., 1mid
            nodesR[i][0] = str.format("{}mid", i + 1);

            # R_par - negative (right terminal) - iout, e.g., 1out
            nodesR[i][1] = str.format("{}out", i + 1);

        namesL = gateway.new_array(gateway.jvm.String, len(L))
        namesR = gateway.new_array(gateway.jvm.String, len(R))

        nodes = gateway.new_array(gateway.jvm.String, 2)

        for i in range(len(L)):
            netlist.add(CommentElement(str.format("* Cell {}", i + 1)))

            # Add inductors
            namesL[i] = str.format("L_{}", nameOrder[i])
            nodes[0], nodes[1] = nodesL[i][1], nodesL[i][0]
            value = '{' + str(L[nameOrder[i]-1][nameOrder[i]-1]) + '*F_SCALE_L}'
            netlist.add(GeneralElement(namesL[i], nodes, value))

            # Add resistance in series with the inductor
            namesR[i] = str.format("R_{}", nameOrder[i])
            nodes[0], nodes[1] = nodesR[i][1], nodesR[i][0]
            value = '{' + str(R[nameOrder[i]-1]) + '*F_SCALE_R}'
            netlist.add(GeneralElement(namesR[i], nodes, value))


        nodesT2TC = gateway.new_array(gateway.jvm.String, len(Capacity_T2T_new), 2)

        nodesC = gateway.new_array(gateway.jvm.String, len(C), 2)

        #The code below interchanges the index of the nameOrder array with the order contained inside the array.
        #This is done since the nameOrder can't be used, since the amount of capacitors between turns/groups doesn't
        #correspond with the amount of turns/groups.
        reverseOrder=np.array([i for i, v in sorted(enumerate(nameOrder), key=lambda iv: iv[1])])+1

        namesC = gateway.new_array(gateway.jvm.String, len(C))

        # Add capacitance to ground
        netlist.add(CommentElement(" Capacitance to ground"))
        for i in range(len(C)):
            nodeC = reverseOrder[C_ind[i]-1]-1 # Capacitance at the input of the cell, aka output of previous cell
            if nodeC == 0:
                nodesC[i][0] = str.format("{}in", nodeC + 1) #First cell exception
            else:
                nodesC[i][0] = str.format("{}out", nodeC);
            nodesC[i][1] = GROUND_NODE;
            namesC[i] = str.format("C_{}", C_ind[i])
            nodes[0], nodes[1] = nodesC[i][1], nodesC[i][0]
            value = '{' + str(C[i]) + '*F_SCALE_C_GROUND}'
            netlist.add(GeneralElement(namesC[i], nodes, value))

        for i in range(len(Capacity_T2T_new)):
            nodeFrom = reverseOrder[Contact_From_new[i]-1]-1 # Capacitance at the input of the cell, aka output of previous cell
            nodeTo = reverseOrder[Contact_To_new[i]-1]-1 # Capacitance at the input of the cell, aka output of previous cell
            if nodeFrom == 0:
                nodesT2TC[i][0] = str.format("{}in", nodeFrom + 1) #First cell exception
            else:
                nodesT2TC[i][0] = str.format("{}out", nodeFrom);
            if nodeTo == 0:
                nodesT2TC[i][1] = str.format("{}in", nodeTo + 1) #First cell exception
            else:
                nodesT2TC[i][1] = str.format("{}out", nodeTo);

        namesT2TC = gateway.new_array(gateway.jvm.String, len(Capacity_T2T_new))

        if flag_turn:
            netlist.add(CommentElement(" Turn to Turn Capacitance"))
        else:
            netlist.add(CommentElement(" Group to Group Capacitance"))

        for i in range(len(Capacity_T2T_new)):
            namesT2TC[i] = str.format("C_T2T_{}_{}", Contact_From_new[i], Contact_To_new[i])
            nodes[0], nodes[1] = nodesT2TC[i][1], nodesT2TC[i][0]
            value = '{' + str(Capacity_T2T_new[i]) + '*F_SCALE_C_T2T}'
            netlist.add(GeneralElement(namesT2TC[i], nodes, value))

        netlist.add(CommentElement(" Mutual coupling between cells"))
        # Add inductive coupling coefficients - upper diagonal
        for row in range(len(L)):
            for col in range(row + 1, len(L)):
                name = str.format("K_{}_{}", row + 1, col + 1)
                nodes[0], nodes[1] = str.format("L_{}", row + 1), str.format("L_{}", col + 1)
                value = str(k[row][col])
                netlist.add(GeneralElement(name, nodes, value))

        # Add parallel resistance
        if flag_R_Par:
            netlist.add(CommentElement("* Parallel resistance"));
            name = "R_Par";
            nodes[0], nodes[1] = nodesL[0][0], nodesR[len(L) - 1][1]
            value = '{R_Par}';
            netlist.add(GeneralElement(name, nodes, value));

        # Add eddy current loops
        if flag_E_loops:
            nodesR_E = gateway.new_array(gateway.jvm.String, 2)
            nodesL_E = gateway.new_array(gateway.jvm.String, 2)
            nodesG_E = gateway.new_array(gateway.jvm.String, 2)

            netlist.add(CommentElement(" Eddy current loops"));
            for i in range(len(E_loops)):
                netlist.add(CommentElement(str.format("* Loop {}", i + 1)));

                nameR = str.format('R_EDDY{}', i + 1)
                nameL = str.format('L_EDDY{}', i + 1)
                nameG = str.format('R_EDDY{}_GND', i + 1)

                nodesR_E[0], nodesR_E[1] = str.format('{}E_L', i + 1), str.format('{}E_R', i + 1)
                nodesL_E[0], nodesL_E[1] = str.format('{}E_R', i + 1), str.format('{}E_L', i + 1)
                nodesG_E[0], nodesG_E[1] = str.format('{}E_L', i + 1), '0'

                valueL = '{' + nameL + '}'
                valueR = '{' + nameR + '}'
                valueK = '{' + str.format('K_EDDY{}', i + 1) + '}'
                valueG = '1E12'

                netlist.add(GeneralElement(nameR, nodesR_E, valueR));
                netlist.add(GeneralElement(nameL, nodesL_E, valueL));
                netlist.add(GeneralElement(nameG, nodesG_E, valueG));

                netlist.add(CommentElement(' Coupling coefficients'));
                for j in range(len(L)):
                    name = str.format("K_E_{}_{}", i + 1, j + 1)
                    nodes[0], nodes[1] = nameL, str.format("L_{}", j + 1)
                    value = valueK
                    netlist.add(GeneralElement(name, nodes, value))

        # Voltage source
        netlist.add(CommentElement(" Voltage source"));
        name = "V_AC"
        nodes[0], nodes[1] = nodesR[len(L) - 1][1], nodesL[0][0]
        value = "AC 1"
        netlist.add(GeneralElement(name, nodes, value));


        netlist.add(CommentElement(" Connection between local ground and last node"));
        name = "V_localGround"
        nodes[0], nodes[1] = "00_mGND", str.format("{}out",len(L))
        value = "0"
        netlist.add(GeneralElement(name, nodes, value));

        # Voltage measurement
        netlist.add(CommentElement(" Voltage measurement"));
        name = "E_total_voltage"
        nodes[0], nodes[1] = "0", "0total_voltage"
        value = "VALUE = {V(1in)-V(" + str.format("{}out" , len(L)) + ")}"
        netlist.add(GeneralElement(name, nodes, value));

        # Add a resistor between local and global ground for a bias point calculation
        netlist.add(CommentElement(" Resistance to ground"));
        name = "R_GND"
        nodes[0], nodes[1] = "0", GROUND_NODE
        value = "1e6"
        netlist.add(GeneralElement(name, nodes, value));

        netlist.setSolver(ACSolverElement.Builder()
                            .pointsPerDecade(pointsPerDecade)
                            .startFrequency(startFrequency)
                            .stopFrequency(stopFrequency)
                            .build())

        netlistAsListString = netlist.generateNetlistFile("BINARY")

        if flag_writeFile:
            if flag_turn:
                cwd = os.getcwd()
                Path(cwd + '/' + nameMagnet).mkdir(parents=True, exist_ok=True)
                #cwd = cwd + '/' + nameMagnet
                Circ = nameMagnet + '/' + nameMagnet + '_turns.cir'
                # subckt
                last = str(nTurns)+'out'
                subname = nameMagnet + '_turns'
            else:
                cwd = os.getcwd()
                Path(cwd + '/' + nameMagnet).mkdir(parents=True, exist_ok=True)
                #cwd = cwd + '/' + nameMagnet
                Circ = nameMagnet + '/' + nameMagnet + '_groups.cir'
                #subckt
                last = str(turnGroup_ind)+'out'
                subname = nameMagnet + '_groups'

            #change probe line
            probe_ind = netlistAsListString.index('\n.PROBE')
            netlistAsListString[probe_ind] = '\n* Configuration file\n.INC configurationFileFrequency.cir'
            netlistAsListString = ListConverter().convert(netlistAsListString, gateway._gateway_client)

            TextFile.writeMultiLine(Circ, netlistAsListString, False)

            # Display time stamp
            currentDT = datetime.datetime.now()
            print(' ')
            print('Time stamp: ' + str(currentDT))

            if flag_turn:
                print('Turn-based netlist file generated.')
            else:
                print('Group-based netlist file generated.')

            # subckt generation
            start = netlistAsListString.index('* PSPICE Netlist Simulation File')
            end = netlistAsListString.index('* Voltage source')
            subckt = '.subckt ' + subname + ' 00_IN 00_OUT 00_mGND\n'
            Lib = list([subckt])
            Lib.extend(netlistAsListString[start+1:end])
            Lib.extend(['\n.ends '])
            #paramInd = netlistAsListString.index('**** Global parameters ****')
            #firstCellInd = netlistAsListString.index('* Cell 1')
            #Lib = Lib[:paramInd-1] + Lib[firstCellInd-1:] # Remove everyting related to parameters (WHY -1?!)
            stepInd = [i for i, s in enumerate(Lib) if '.STEP PARAM' in s]
            for i in range(len(stepInd)): #doesn't run if the stepInd is empty
                Lib.pop(stepInd[len(stepInd)-1-i]) #go through from back to front, so that the indexes still correspond to the correct string

            Lib = [sub.replace('.PARAM', '+ PARAMS:') for sub in Lib]

            #Lib = [sub.replace('(0', '(00_mGND') for sub in Lib]
            #Lib = [sub.replace(' 0)', ' 00_mGND)') for sub in Lib]
            Lib = [sub.replace('1in', '00_IN') for sub in Lib]
            Lib = [sub.replace(last, '00_OUT') for sub in Lib]

            psub = 'subckt/Items/'
            Path(cwd + '/' + psub).mkdir(parents=True, exist_ok=True)
            #cwd = cwd + '/' + nameMagnet
            Libname = psub + subname + '.lib'
            java_Lib = ListConverter().convert(Lib, gateway._gateway_client)
            TextFile.writeMultiLine(Libname, java_Lib, False)

        else:
            print('Netlist generation done, file generation disabled.')

        return netlist, netlistAsListString

    def netlistMagnet(self):
        # Creates a simple netlist only consisting of the total inductance, total resistance and total capacitance to ground.
        flag_writeFile = self.flag_writeFile
        flag_R_Par = self.flag_R_Par
        R_Par = self.R_Par
        flag_E_loops = self.flag_E_loops
        E_loops = self.E_loops
        F_SCALE_C_GROUND = self.F_SCALE_C_GROUND
        F_SCALE_L = self.F_SCALE_L
        F_SCALE_R = self.F_SCALE_R
        pointsPerDecade = self.pointsPerDecade
        startFrequency = self.startFrequency
        stopFrequency = self.stopFrequency
        nameMagnet = self.nameMagnet

        path_gateway = self.eospath + 'SWAN_projects/steam-notebooks/steam/*'

        # Launch a Gateway in a new Java process, this returns port
        port = launch_gateway(classpath=path_gateway)
        # JavaGateway instance is connected to a Gateway instance on the Java side
        gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))
        # Get STEAM API Java classes
        MutualInductance = gateway.jvm.component.MutualInductance
        Netlist = gateway.jvm.netlist.Netlist
        CommentElement = gateway.jvm.netlist.elements.CommentElement
        GeneralElement = gateway.jvm.netlist.elements.GeneralElement
        GlobalParameterElement = gateway.jvm.netlist.elements.GlobalParameterElement
        ACSolverElement = gateway.jvm.netlist.solvers.ACSolverElement
        CircuitalPreconditionerSubcircuit = gateway.jvm.preconditioner.CircuitalPreconditionerSubcircuit
        TextFile = gateway.jvm.utils.TextFile
        CSVReader = gateway.jvm.utils.CSVReader

        netlist = Netlist("")

        globalParameters_Parameters = ['F_SCALE_C_GROUND', 'F_SCALE_L', 'F_SCALE_R']
        globalParameters_Values = [str.format('{}', F_SCALE_C_GROUND), str.format('{}', F_SCALE_L), str.format('{}', F_SCALE_R)]

        E_param_param = []
        E_param_values = []

        if flag_E_loops:
            for i in range(len(E_loops)):
                E_param_param = E_param_param + [str.format('L_EDDY{}', i + 1), str.format('R_EDDY{}', i + 1),
                                                 str.format('K_EDDY{}', i + 1)]
                E_param_values = E_param_values + [str.format('{}', E_loops[i][0]), str.format('{}', E_loops[i][1]),
                                                   str.format('{}', E_loops[i][2])]

            globalParameters_Parameters = globalParameters_Parameters + E_param_param
            globalParameters_Values = globalParameters_Values + E_param_values

        if flag_R_Par:
            globalParameters_Parameters = globalParameters_Parameters + ['R_Par']
            globalParameters_Values = globalParameters_Values + [str.format('{}', R_Par)]

        globalParameters_Parameters = a.create_string_array(gateway, globalParameters_Parameters)
        globalParameters_Values = a.create_string_array(gateway, globalParameters_Values)

        netlist.add(CommentElement("**** Global parameters ****"))
        netlist.add(GlobalParameterElement(globalParameters_Parameters, globalParameters_Values))

        netlist.add(CommentElement("* .STEP PARAM R_Par 10k, 100k, 10k"))

        GROUND_NODE = "1out"

        nodes = gateway.new_array(gateway.jvm.String, 2)

        # Add inductor
        nameL = "L_total"
        nodes[0], nodes[1] = "1in" , "1mid"
        value = '{' + str(self.Total_Inductance) + '*F_SCALE_L}'
        netlist.add(GeneralElement(nameL, nodes, value))

        # Add resistance in series with the inductor
        nameR = "R_total"
        nodes[0], nodes[1] = "1mid" , "1out"
        value = '{' + str(self.Total_Resistance) + '*F_SCALE_R}'
        netlist.add(GeneralElement(nameR, nodes, value))

        # Add capacitance to ground from input
        nameC = "C_total"
        nodes[0], nodes[1] = "1in", GROUND_NODE
        value = '{' + str(self.Total_Capacitance) + '*F_SCALE_C_GROUND*0.40528473456}' # added 1/(pi/2)^2 correction
        netlist.add(GeneralElement(nameC, nodes, value))


        # Add parallel resistance
        if flag_R_Par:
            netlist.add(CommentElement("* Parallel resistance"));
            name = "R_Par";
            nodes[0], nodes[1] = "1in", "1out"
            value = '{R_Par}';
            netlist.add(GeneralElement(name, nodes, value));

        # Add eddy current loops
        if flag_E_loops:
            nodesR_E = gateway.new_array(gateway.jvm.String, 2)
            nodesL_E = gateway.new_array(gateway.jvm.String, 2)
            nodesG_E = gateway.new_array(gateway.jvm.String, 2)

            netlist.add(CommentElement(" Eddy current loops"));
            for i in range(len(E_loops)):
                netlist.add(CommentElement(str.format("* Loop {}", i + 1)));

                nameR = str.format('R_EDDY{}', i + 1)
                nameL = str.format('L_EDDY{}', i + 1)
                nameG = str.format('R_EDDY{}_GND', i + 1)

                nodesR_E[0], nodesR_E[1] = str.format('{}E_L', i + 1), str.format('{}E_R', i + 1)
                nodesL_E[0], nodesL_E[1] = str.format('{}E_R', i + 1), str.format('{}E_L', i + 1)
                nodesG_E[0], nodesG_E[1] = str.format('{}E_L', i + 1), '0'

                valueL = '{' + nameL + '}'
                valueR = '{' + nameR + '}'
                valueK = '{' + str.format('K_EDDY{}', i + 1) + '}'
                valueG = '1E12'

                netlist.add(GeneralElement(nameR, nodesR_E, valueR));
                netlist.add(GeneralElement(nameL, nodesL_E, valueL));
                netlist.add(GeneralElement(nameG, nodesG_E, valueG));

                netlist.add(CommentElement(' Coupling coefficients'));
                name = str.format("K_E_{}", i + 1)
                nodes[0], nodes[1] = nameL, "L_total"
                value = valueK
                netlist.add(GeneralElement(name, nodes, value))

        # Voltage source
        netlist.add(CommentElement(" Voltage source"));
        name = "V_AC"
        nodes[0], nodes[1] = "1out", "1in"
        #nodes[0], nodes[1] = "1in", "1out" # matched based on the D1 group model
        #nodes[0], nodes[1] = nodesL[0][0], nodesR[len(L) - 1][1]
        value = "AC 1"
        netlist.add(GeneralElement(name, nodes, value));

        # Voltage measurement
        netlist.add(CommentElement(" Voltage measurement"));
        name = "E_total_voltage"
        nodes[0], nodes[1] = "0", "0total_voltage"
        value = "VALUE = {V(1in)-V(1out)}"
        #value = "VALUE = {V(" + str.format("{}out" , len(L)) + ")-V(1in)}"
        netlist.add(GeneralElement(name, nodes, value));

        # Add a resistor to ground for a bias point calculation
        netlist.add(CommentElement(" Resistance to ground"));
        name = "R_GND"
        nodes[0], nodes[1] = "1out", "0"
        value = "1e6"
        netlist.add(GeneralElement(name, nodes, value));

        netlist.setSolver(ACSolverElement.Builder()
                            .pointsPerDecade(pointsPerDecade)
                            .startFrequency(startFrequency)
                            .stopFrequency(stopFrequency)
                            .build())

        netlistAsListString = netlist.generateNetlistFile("BINARY")

        if flag_writeFile:
            cwd = os.getcwd()
            Path(cwd + '/' + nameMagnet).mkdir(parents=True, exist_ok=True)
            #cwd = cwd + '/' + nameMagnet
            Circ = nameMagnet + '/' + nameMagnet + '_magnet.cir'
            # subckt
            subname = nameMagnet + '_magnet'

            #change probe line
            probe_ind = netlistAsListString.index('\n.PROBE')
            netlistAsListString[probe_ind] = '\n* Configuration file\n.INC configurationFileFrequency.cir'
            netlistAsListString = ListConverter().convert(netlistAsListString, gateway._gateway_client)

            TextFile.writeMultiLine(Circ, netlistAsListString, False)

            # Display time stamp
            currentDT = datetime.datetime.now()
            print(' ')
            print('Time stamp: ' + str(currentDT))

            print('Magnet-based netlist file generated.')

            # subckt generation
            start = netlistAsListString.index('* PSPICE Netlist Simulation File')
            end = netlistAsListString.index('* Voltage source')
            subckt = '.subckt ' + subname + ' 00_IN 00_OUT 00_mGND\n'
            Lib = list([subckt])
            Lib.extend(netlistAsListString[start+1:end])
            Lib.extend(['\n.ends '])
            #paramInd = netlistAsListString.index('**** Global parameters ****')
            #firstCellInd = netlistAsListString.index('* Cell 1')
            #Lib = Lib[:paramInd-1] + Lib[firstCellInd-1:] # Remove everyting related to parameters (WHY -1?!)
            stepInd = [i for i, s in enumerate(Lib) if '.STEP PARAM' in s]
            for i in range(len(stepInd)): #doesn't run if the stepInd is empty
                Lib.pop(stepInd[len(stepInd)-1-i]) #go through from back to front, so that the indexes still correspond to the correct string

            Lib = [sub.replace('.PARAM', '+ PARAMS:') for sub in Lib]

            #replace capacitance nodes
            Lib = [sub.replace('C_total (1in 1out)', 'C_total (00_IN 00_mGND)') for sub in Lib]
            #Lib = [sub.replace('(0', '(00_mGND') for sub in Lib]
            #Lib = [sub.replace(' 0)', ' 00_mGND)') for sub in Lib]
            Lib = [sub.replace('1in', '00_IN') for sub in Lib]
            Lib = [sub.replace('1out', '00_OUT') for sub in Lib]

            psub = 'subckt/Items/'
            Path(cwd + '/' + psub).mkdir(parents=True, exist_ok=True)
            #cwd = cwd + '/' + nameMagnet
            Libname = psub + subname + '.lib'
            java_Lib = ListConverter().convert(Lib, gateway._gateway_client)
            TextFile.writeMultiLine(Libname, java_Lib, False)

        else:
            print('Netlist generation done, file generation disabled.')

        return netlist, netlistAsListString
