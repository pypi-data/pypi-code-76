from steam_nb_api.ledet.ParameterSweep import *
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
from steam_nb_api.ledet.ParametersLEDET import *
import pandas as pd
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.ledet.SimulationEvaluation import EvaluateSimulations
from steam_nb_api.ledet.QuenchAnalysis import QuenchPlanAnalysis
from steam_nb_api.ledet.AutomaticSweep import AutomaticSweep
import time

testfile1 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRC\MBRC_0.xlsx"
testfile2 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRB\MBRB_0.xlsx"
testfile3 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBRS\MBRS_0.xlsx"
testfile4 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MBX\MBX_0.xlsx"
testfile5 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCD\MCD_0.xlsx"
testfile6 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCO\MCO_0.xlsx"
testfile7 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"
testfile8 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXH\MCBXH_CopperWedges_ThCool_0.xlsx"
testfile9 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_ThCool_0.xlsx"
testfile10 = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_0.xlsx"
testfile11 = "C:\cernbox\TEMP2\MCBY_1AP_CopperWedges_ThCool_29.xlsx"
testfile12 = "C:\cernbox\LEDET\LEDET\MCBY_1AP_CopperWedges_ThCool\Input\MCBY_1AP_CopperWedges_ThCool_35.xlsx"
testfile13 = "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_23.xlsx"

ledetFolder = 'C:\\cernbox\\LEDET_MT\\'
ledetExe = 'LEDET_v1_08_03.exe'

def CompleteRun():
    start = time.time()
    a = ParametersLEDET()
    a.readLEDETExcel(testfile13)
    Sw = MinMaxSweep(a, 6)
    MagnetName = 'MQXFS4b'

    ##MQXF
    Sw.addParameterToSweep('tau_increaseRis', 0.001, 0.1)
    Sw.addParameterToSweep('f_ro_eff_inGroup', 0.75, 3)
    Sw.addParameterToSweep('tau_increaseRif', 0.001, 0.1)


    ##13mag
    # Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    # ##MBX/ MRBC/ MBRS/ MBRB
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3, basePoints = 3)
    # Sw.addParameterToSweep('R_c_inGroup', -6, -3, type='logarithmic', basePoints= 3)
    # Sw.addHeliumCrossSection(0, 6, basePoints= 4)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 35, 200, basePoints=6)

    ##8mag
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addHeliumCrossSection(3, 6, basePoints=4)

    ## MCBXH_CopperWedges -1
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 0.1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    # Sw.addParameterToSweep('l_magnet', 0.056, 0.14)
    # Sw.addQuenchSweep("tStartQuench",[1,1,1,1,1,1],[-0.2, -0.21, -0.22, -0.23, -0.24, -0.25])
    # Sw.addQuenchSweep("tStartQuench", [[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050],[1, 730],[321,1050]],
    #                   [[-0.2, -0.182],[-0.2, -0.182],[-0.15, -0.132],[-0.15, -0.132],[-0.1, -0.082],[-0.2, -0.082],[-0.05, -0.032],[-0.05, -0.032]])

    ##MCBY
    # Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    # Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)

    ## Current Sweep
    # Sw.addCurrentSweep(6650, 30)

    Sw.generatePermutations()
    end = time.time()
    print("Time:", end-start)
    start = time.time()
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Input\\",OffsetNumber=100)
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MBRC\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCD\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCO\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MO_1AP\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXH_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\LEDET\\LEDET\\MCBXV_CopperWedges_ThCool\\Input\\")
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber= 42, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBXV\\MCBXV_CopperWedges_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber=17, ROXIE_File='C:\\cernbox\\SWAN_projects\\steam-notebooks\\steam-ledet-input\\MCBY_1AP\\MCBY_1AP_CopperWedges_ThCool_All_WithIron_WithSelfField.map2d')
    # Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEMP2\\", OffsetNumber=50)


    end = time.time()
    print("Time:", end - start)
    print("Preparation done")

    # SimNumbers = np.linspace(100,315, 216).astype(int)

    # RunSimulations(ledetFolder, ledetExe, MagnetName, Simulations = SimNumbers, RunSimulations=False)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCO\\Output\\Txt Files", 'MCO',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCO.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations("C:\\cernbox\\LEDET\\LEDET\\MCD\\Output\\Txt Files", 'MCD',
    #                     'C:\\cernbox\\Validation_MCDO\\Exp Data\\RCD.A56B1_2018-03-16_PM_I_A_AutoAlign.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET_SimulationFiles_Quench\LEDET\MBRS\Output\Txt Files', 'MBRS',
    #                      'C:\cernbox\Validation_IPD\Validation MBRS\Exp Data\RD3.R4_20181203_135959_IA - Cut.csv',
    #                     Sw, Mat=False, SkipAlign=True)
    # EvaluateSimulations('C:\cernbox\LEDET\LEDET\MBRC\Output\Txt Files', 'MBRC',
    #                      'C:\cernbox\Validation_IPD\Validation MBRC\Exp Data\RD2.L8_20181203_131307_IA - Cut.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB2', 'MO_1AP', 'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B2_PM_I_A.csv',
    #                     Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB1', 'MO_1AP',
    #                     'C:\\cernbox\\LHC-SM-API\\ROD_ROF\\ROD.A12B1_PM_I_A.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\1st Sweep-RRR_fro_tQ\\Output\\Txt Files', 'MCBXH_CopperWedges',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations('C:\\cernbox\\Validation_MCBX_HV\\LEDET Validation\\2nd Sweep-RRR_fro_tQ_THCOOL\\Output\\Txt Files',
    #                     'MCBXH_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                      Sw, Mat=False, showBestFit = 20)
    # EvaluateSimulations("C:\\cernbox\\TEMP\\",
    #                     'MCBXV_CopperWedges_ThCool', 'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXV2.R1_2017-04-20_PM_I_ARAW.csv',
    #                      Sw, Mat=False)
    # EvaluateSimulations("C:\\cernbox\\TEMP2\\",
    #                     'MCBXH_CopperWedges_ThCool',
    #                     'C:\\cernbox\\Validation_MCBX_HV\\Exp Data\\RCBXH1.R1_2018-03-11_PM_I_ARAW.csv',
    #                     Sw, Mat=False)
    EvaluateSimulations("C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Txt Files",
                        MagnetName,
                        'C:\\cernbox\\MasterThesis\\Test23_ParSweepMeas.csv',
                        Sw, Mat=False)


def AutomaticRun():
    LEDETFolder = 'C:\\cernbox\LEDET\\LEDET_SimulationFiles_Quench'
    LEDETExe = 'LEDET_v1_07_01_6February2020.exe'
    MagnetName = 'MO_1AP'
    MeasFile = 'C:\cernbox\LHC-SM-API\ROD_ROF\ROD.A12B2_PM_I_A.csv'
    SetUpFile = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MO_1AP\MO_1AP_8magBB_0.xlsx"

    ASw = AutomaticSweep(8, SetUpFile, LEDETFolder, LEDETExe, MagnetName, MeasFile)
    ASw.addParameterToSweep('l_magnet', 2.56, 4.8)
    ASw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
    ASw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
    #ASw.AutomaticRun(101)

    ASw.LearnAndTrainAll()
    return ASw

def testConsistencyChecks():
    a = ParametersLEDET()
    a.readLEDETExcel(testfile10)
    x = a.consistencyCheckLEDET()
    print(x)

def testvQ():
    nameFileLEDET = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXA\MQXA_0.xlsx"
    # nameFileLEDET = 'C:\cernbox\LEDET_MT\LEDET\MQXFBP2\Input\MQXFBP2_10.xlsx'
    RoxieFile = "C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MQXA\MQXA_All_WithIron_WithSelfField.map2d"
    # RoxieFile = "C:\cernbox\LEDET_MT\Field Maps\MQXFBP2\MQXFBP2_All_WithIron_WithSelfField.map2d"
    # RoxieFile = "C:\\cernbox\\LEDET_MT\\Field Maps\\MQXFBP2\\"
    a = ParametersLEDET()
    a.readLEDETExcel(nameFileLEDET)
    [vQ, l, th_con_h, delta_t_h, th_con_w, delta_t_w] = a.adjust_vQ(RoxieFile)
    return a

def testQuenchPlanAnalysis(FileName_TDMS, FileName_Sim, verbose = False):
    Coil108 = {'C108_I1_I2':[],
               'C108_I2_I3':np.concatenate((np.linspace(29, 45, 17), np.linspace(229, 245, 17))),
               'C108_I3_I4':np.concatenate((np.linspace(46, 49, 4), np.linspace(246, 249, 4))),
               'C108_I4_I5':[],
               'C108_I5_I6':np.array([50]),
               'C108_I6_I7':[],
               'C108_I7_I8':np.array([250]),
               'C108_I8_O1':[],
               'C108_O1_O2':[],
               'C108_O2_O3':np.array([28]),
               'C108_O3_O4':[],
               'C108_O4_O5':np.array([228]),
               'C108_O5_O6':np.concatenate((np.linspace(17, 27, 11), np.linspace(217, 227, 11))),
               'C108_O6_O7':np.concatenate((np.linspace(1, 16, 16), np.linspace(201, 216, 16))),
               'C108_O7_O8':[]}
    Coil109 = {'C109_I1_I2':[],
               'C109_I2_I3':np.concatenate((np.linspace(329, 345, 17), np.linspace(129, 145, 17))),
               'C109_I3_I4':np.concatenate((np.linspace(146, 149, 4), np.linspace(346, 349, 4))),
               'C109_I4_I5':[],
               'C109_I5_I6':np.array([150]),
               'C109_I6_I7':[],
               'C109_I7_I8':np.array([350]),
               'C109_I8_O1':[],
               'C109_O1_O2':[],
               'C109_O2_O3':np.array([128]),
               'C109_O3_O4':[],
               'C109_O4_O5':np.array([328]),
               'C109_O5_O6':np.concatenate((np.linspace(117, 127, 11), np.linspace(317, 327, 11))),
               'C109_O6_O7':np.concatenate((np.linspace(101, 116, 16), np.linspace(301, 316, 16))),
               'C109_O7_O8':[]}
    Coil110 = {'C110_I1_I2':[],
               'C110_I2_I3':np.concatenate((np.linspace(79, 95, 17), np.linspace(279, 295, 17))),
               'C110_I3_I4':np.concatenate((np.linspace(96, 99, 4), np.linspace(296, 299, 4))),
               'C110_I4_I5':[],
               'C110_I5_I6':np.array([100]),
               'C110_I6_I7':[],
               'C110_I7_I8':np.array([300]),
               'C110_I8_O1':[],
               'C110_O1_O2':[],
               'C110_O2_O3':np.array([78]),
               'C110_O3_O4':[],
               'C110_O4_O5':np.array([278]),
               'C110_O5_O6':np.concatenate((np.linspace(267, 277, 11), np.linspace(67, 77, 11))),
               'C110_O6_O7':np.concatenate((np.linspace(51, 66, 16), np.linspace(251, 266, 16))),
               'C110_O7_O8':[]}
    Coil111 = {'C111_I1_I2':[],
               'C111_I2_I3':np.concatenate((np.linspace(179, 195, 17), np.linspace(379, 395, 17))),
               'C111_I3_I4':np.concatenate((np.linspace(196, 199, 4), np.linspace(396, 399, 4))),
               'C111_I4_I5':[],
               'C111_I5_I6':np.array([200]),
               'C111_I6_I7':[],
               'C111_I7_I8':np.array([400]),
               'C111_I8_O1':[],
               'C111_O1_O2':[],
               'C111_O2_O3':np.array([178]),
               'C111_O3_O4':[],
               'C111_O4_O5':np.array([378]),
               'C111_O5_O6':np.concatenate((np.linspace(367, 377, 11), np.linspace(167, 177, 11))),
               'C111_O6_O7':np.concatenate((np.linspace(151, 166, 16), np.linspace(351, 366, 16))),
               'C111_O7_O8':[]}
    a = QuenchPlanAnalysis(FileName_TDMS, FileName_Sim, verbose = verbose)
    # a = QuenchPlanAnalysis(0, FileName_Sim)
    # a.ProvideTurnsToCoilStructure(Coil = [Coil109,Coil110,Coil111,Coil108])
    a.ProvideTurnsToCoilStructure(CoilCsv = 'C:\cernbox\MasterThesis\CoilStructure_MQXFS4b.csv')
    # a.QuenchPlanAnalysis(Plot = 1)
    # a.FindQuenchTDMS(0.1, 0.007, Plot=0)
    a.PlotVoltageTap(Coil = 110)
    # a.PlotVoltageTap(TapName = 'C109_I2_I3')
    # a.calculateAllQuenchIntegrals(TDMS = 0)
    # a.calculateAllQuenchIntegrals(SIM = 0)
    return a

def PrepareSimulations():
    PlanFile = "C:\cernbox\MasterThesis\MQFBP2 Test\MQXFBP2_QuenchPlan_Masterfile.xlsx"
    RefFile = "C:\cernbox\MasterThesis\MQFBP2 Test\MQXFBP2_Ref_0.xlsx"
    OutputDirectory = "C:\cernbox\TEMP"

    a = QuenchPlanAnalysis(0, 0)
    a.PrepareSimulations(PlanFile, RefFile, OutputDirectory,
                         QHpairs=[[1,5],[2,6],[3,7],[4,8],[9,13],[10,14],[11,15],[12,16]])


# testConsistencyChecks()

# CompareLEDETParameters("C:\cernbox\MB_1.xlsx","C:\cernbox\MB_65.xlsx")

# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_0.xlsx", "C:\cernbox\MasterThesis\QuenchPlans\MQXF_V2_2924.xlsx")
# CompareLEDETParameters("C:\\cernbox\\steam-notebook-api\\test\\ledet\\resources\\TestFile_1.xlsx", "C:\\cernbox\\steam-notebook-api\\test\\ledet\\TestFile1.xlsx")
# CompareLEDETParameters("C:\cernbox\MasterThesis\QuenchPlans\MQXF_V2_5400.xlsx", "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_14.xlsx")
# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_18.xlsx", "C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_15.xlsx")
# CompareLEDETParameters("C:\cernbox\SWAN_projects\steam-notebooks\steam-ledet-input\MCBXV\MCBXV_CopperWedges_ThCool_0.xlsx", "C:\cernbox\TEMP2\MCBXH_CopperWedges_ThCool_100.xlsx")
# CompareLEDETParameters("C:\cernbox\COSIM\\600A\RCS.A45B2\Output_3\\3_LEDET\Model\LEDET\MCS\Input\MCS_0_.xlsx","C:\cernbox\SWAN_projects\steam-notebooks\steam-sing-input\\600A_Rpar\cosim_model_RCS.A45B2\LEDET_2\LEDET\MCS\Input\MCS_0.xlsx")
# CompareLEDETParameters("C:\cernbox\LEDET_MT\LEDET\MQXFS4b\Input\MQXFS4b_23.xlsx", "C:\cernbox\MQXF_V2_2924.xlsx")

# CompareLEDETParameters("C:\cernbox\MB_92.xlsx", "C:\cernbox\MB_98.xlsx")


# test_readLEDETExcel()
# test_setgetAttributes()
# test_permutations()
# test_SetUpSimulations()
# test_EvaluateSimulations()

# CompleteRun()

# PrepareSimulations()

# a  = testvQ()

# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810151854_a026(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111418_a003(0).tdms"
td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111846_a008(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810101854_tb017(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810101725_tb016(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171217_a041(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810121049_a012(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810120908_a009(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810111541_a006(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171446_a042(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171007_a036(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810171144_a039(0).tdms"
# td_data = "C:\\cernbox\\MasterThesis\\Measurement_data\\MQXFS4b\\HCMQXSM001-CR000042__H1810161600_a033(0).tdms"

# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFBP2\\Output\\Mat Files\\SimulationResults_LEDET_10.mat"
sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_12.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_10.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_27.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_15.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_23.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_18.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_3.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_12.mat"
# sim_data = "C:\\cernbox\\LEDET_MT\\LEDET\\MQXFS4b\\Output\\Mat Files\\SimulationResults_LEDET_26.mat"

a = testQuenchPlanAnalysis(td_data, sim_data)
# a.ExtractFeatures()
# a = testQuenchPlanAnalysis(0, sim_data)
# a = testQuenchPlanAnalysis(td_data, 0)


# a = ParametersLEDET()
# a.readLEDETExcel(testfile7)
# Sw = MinMaxSweep(a, 3)
# MagnetName = 'MCBXH_CopperWedges'
# Sw.addParameterToSweep('l_magnet', 4.16, 5.2)
# Sw.addParameterToSweep('f_ro_eff_inGroup', 1, 3)
# Sw.addParameterToSweep('RRR_Cu_inGroup', 100, 300)
# Sw.addQuenchSweep("tStartQuench",[0,2],[-3,5])
# Sw.addQuenchSweep("tStartQuench",[[1,4],[2,5]],[[-3,5],[1,2]])
# Sw.addHeliumCrossSection(3, 6, basePoints=4)
# Sw.generatePermutations()
# Sw.prepareSimulation(MagnetName, "C:\\cernbox\\TEST-DELTE\\")

# x = AutomaticRun()
