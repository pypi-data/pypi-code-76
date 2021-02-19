import re
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors as mcolors
import h5py
from steam_nb_api.ledet.ParameterSweep import *
from nptdms import TdmsFile
import nptdms
from scipy import signal
import csv
from scipy.integrate import simps

@dataclass
class TDMSdata:
    FileName: str = ''
    Tolerance: float = 20.0
    groupHF:  nptdms.GroupObject = nptdms.GroupObject('HF')
    groupMF: nptdms.GroupObject = nptdms.GroupObject('MF')
    VoltageVertices: np.ndarray = np.array([])
    TimeFrame_MF: np.ndarray = np.array([])
    t_steps_MF:  float = 0.0
    t_d_MF: float = 0.0
    trigger_PC: int = 0
    trigger_shoot: int = 0
    I_DCCT_MF: np.ndarray = np.array([])
    I_DCCT_HF: np.ndarray = np.array([])
    I_CLIQ: np.ndarray = np.array([])
    U_CLIQ: np.ndarray = np.array([])
    C_CLIQ: float = 0.0
    f_CLIQ: np.ndarray = np.array([])
    I_QH: np.ndarray = np.array([])
    U_QH: np.ndarray = np.array([])
    QL1: float = 0.0
    QL2: float = 0.0
    Quenches: np.ndarray = np.array([])

@dataclass
class SIMdata:
    FileName: str = ''
    TimeFrame: np.ndarray = np.array([])
    trigger_PC: int = 0
    XY_mag_ave: np.ndarray = np.array([])
    I_CoilSections: np.ndarray = np.array([])
    I_CLIQ: np.ndarray = np.array([])
    directionsCLIQ: np.ndarray = np.array([])
    U_CLIQ: np.ndarray = np.array([])
    C_CLIQ: float = 0.0
    f_CLIQ: np.ndarray = np.array([])
    I_QH: np.ndarray = np.array([])
    U_QH: np.ndarray = np.array([])
    QL1: float = 0.0
    QL2: float = 0.0
    Quenches: np.ndarray = np.array([])
    Thotspot: np.ndarray = np.array([])
    U_CoilSections: np.ndarray = np.array([])
    T_adiabatic: np.ndarray = np.array([])
    el_connections: np.ndarray = np.array([])

class QuenchPlanAnalysis():
    ## Domain: Helper and init function
    def __init__(self, FileNameTDMS, FileNameSIMData, beforePC = 0.4, verbose =  False):
        self.beforePC = beforePC
        self.Colors = self.__generateColors()
        self.verbose = verbose

        self.MergedVoltages = {}
        self.MergedVoltagesPolarities = {}
        self.CopyMVP = []

        self.SIMdata = SIMdata()
        self.SIMdata.FileName = FileNameSIMData
        if FileNameSIMData: self.__CreateSIMDataObject()

        self.TDMSdata = TDMSdata()
        self.TDMSdata.FileName = FileNameTDMS
        if FileNameTDMS: self.__CreateTDMSDataObject()

    def __generateColors(self):
        # setting colors for plotting
        col = mcolors.TABLEAU_COLORS.keys()
        col2 = mcolors.BASE_COLORS.keys()
        col3 = mcolors.CSS4_COLORS.keys()
        colors = []
        for c in col:
            colors = colors + [c]
        for c in col3:
            if c == 'white' or c == 'snow' or c == 'azure' or c == 'aliceblue': continue
            colors = colors + [c]
        for c in col2:
            if c == 'w': continue
            colors = colors + [c]
        return colors*99

    #############################################################################################################
    ## Domain: Set-up TestPlans from given MasterFile
    def __findOccurrences(self, s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def __constructLUT_SPA(self, rate, I00, t_Start, t_PC):
        LUT = [I00, I00]
        TimeLUT = [t_Start, t_PC]
        t = 0
        while I00 > rate:
            LUT.append(I00 -rate)
            I00 = I00 - rate
            TimeLUT.append(t + 1)
            t = t + 1
        LUT.append(0)
        TimeLUT.append(t + I00 / rate)
        return [LUT, TimeLUT]

    def __suggestTimeStep(self, t):
        if t < 0.3: return 0.000025
        elif t < 1: return 0.0001
        elif t < 3: return 0.001
        else: return 0.01

    def __RefineTimeVector(self, time_vector):
        new_timeVector = np.ones((len(time_vector),))
        for i in range(len(time_vector)):
            if (i + 1) % 3 == 0 or i == 0:
                new_timeVector[i] = time_vector[i]
                TimeStep = self.__suggestTimeStep(time_vector[i])
            elif (i-1)%3 == 0: new_timeVector[i] = TimeStep
            elif i%3 == 0: new_timeVector[i] = time_vector[i]-time_vector[i+1]+TimeStep
        return new_timeVector

    def __ExtendTimeVector(self, time_vector, endTime):
        time_vector = np.append(time_vector, [time_vector[-1]+self.__suggestTimeStep(time_vector[-1]), self.__suggestTimeStep(time_vector[-1]), endTime])
        return time_vector

    def __ExtractQHidx(self, Trigger, QHpairs):
        idxQH = np.array([])
        numbers = re.findall(r'\d+', Trigger)
        for i in range(len(numbers)):
            idxQH = np.append(idxQH, [int(x)-1 for x in QHpairs[int(numbers[i])-1]])
        return idxQH.astype(int)

    def PrepareSimulations(self, PlanFile, RefFile, OutputDirectory, MagnetName = '', QHpairs = [[]], nQHseries = 2,
                           t_QH_Fire = 0.002, t_CLIQ_Fire = 0.0005):
        # Find MagnetName in RefFile Name
        if not MagnetName:
            RFile = RefFile.replace('\\', '//')
            idxRef = self.__findOccurrences(RFile, '/')
            idxRef = idxRef[-1] + 1
            idxScore = RFile.find('_')
            MagnetName = RFile[idxRef:idxScore]
        if self.verbose: print("MagnetName = ",MagnetName)

        ##  Prepare simulations
        df = pd.read_excel(PlanFile)
        SimNumbers = []
        for index, row in df.iterrows():
                if index==0: continue
                a = ParametersLEDET()
                a.readLEDETExcel(RefFile)

                ## 1. Adjust current in the circuit
                a.setAttribute("Inputs", "I00", df.iloc[index]['Current'])
                if df.iloc[index]['Trigger Type'] == 'SPA':
                    [LUT, TimeLUT] = self.__constructLUT_SPA(df.iloc[index]['Ramp Rate'], df.iloc[index]['Current'],
                                                             a.Inputs.t_PC_LUT[0], a.Inputs.t_PC_LUT[1])
                    a.setAttribute('Inputs', 't_PC_LUT', TimeLUT)
                    if a.Options.time_vector_params[-1]<50:
                        print("I assume a slow discharge. Extend time vector.")
                        a.setAttribute('Options', 'time_vector_params',
                                       self.__ExtendTimeVector(a.Options.time_vector_params, 50))
                else:
                    LUT = a.Inputs.I_PC_LUT
                    LUT[LUT != 0] = df.iloc[index]['Current']

                    if df.iloc[index]['Current'] < (a.Options.Iref / 10):
                        print('Small current detected. I will refine the time vector.')
                        a.setAttribute('Options', 'time_vector_params',
                                       self.__RefineTimeVector(a.Options.time_vector_params))
                    elif df.iloc[index]['Current'] < (a.Options.Iref / 4) and a.Options.time_vector_params[-1]<10:
                        print("I assume a slow discharge. Extend time vector.")
                        a.setAttribute('Options', 'time_vector_params',
                                       self.__ExtendTimeVector(a.Options.time_vector_params, 10))

                a.setAttribute('Inputs', 'I_PC_LUT', LUT)

                ### 2. Adjust CLIQ
                if df.iloc[index]['CLIQ'] == df.iloc[index]['CLIQ']:
                    a.setAttribute("Inputs", "U0", df.iloc[index]['V_CLIQ'])
                    a.setAttribute("Inputs", "C", df.iloc[index]['C_CLIQ'] / 1000)
                    if df.iloc[index]['C_CLIQ']<25:
                        print('Small CLIQ capacitance detected. I will refine the time vector.')
                        a.setAttribute('Options', 'time_vector_params',
                                       self.__RefineTimeVector(a.Options.time_vector_params))
                    if df.iloc[index]['Delay_CLIQ']<0:
                        a.setAttribute("Inputs", "tCLIQ", df.iloc[index]['Delay_CLIQ']/ 1000-t_CLIQ_Fire)
                    else: a.setAttribute("Inputs", "tCLIQ", df.iloc[index]['Delay_CLIQ']/ 1000+t_CLIQ_Fire)
                else:
                    a.setAttribute("Inputs", "tCLIQ", 9999)

                ### 3. Adjust Energy Extraction
                if df.iloc[index]['EE'] == df.iloc[index]['EE']:
                    a.setAttribute("Inputs", "tEE", df.iloc[index]['Delay_EE'])
                    a.setAttribute("Inputs", "R_EE", df.iloc[index]['R_EE'])
                else:
                    a.setAttribute("Inputs", "tEE", 9999)

                ### 4. Adjust Quench Heater
                if df.iloc[index]['QH'] == df.iloc[index]['QH']:
                    nQH = len(a.getAttribute("Inputs", "tQH"))
                    if len(QHpairs) == 1:
                        if self.verbose: print('No Quench Heater pairs provided. Set all QH to be handled together.')
                        QHpairs[0] = np.linspace(0,nQH-1, nQH).astype(int).tolist()

                    V_QH = [df.iloc[index]['V_QH'] / nQHseries] * nQH
                    a.setAttribute("Inputs", "U0_QH", V_QH)

                    t_QH = np.ones(nQH) * 9999
                    t_noFire = np.where(a.Inputs.tQH>1000)
                    if df.iloc[index]['Delay_QH']<0:
                        QH_delay = df.iloc[index]['Delay_QH'] / 1000 - t_QH_Fire
                    else:
                        QH_delay = df.iloc[index]['Delay_QH'] / 1000 + t_QH_Fire

                    if df.iloc[index]['Trigger Type'] == df.iloc[index]['Trigger Type']:
                        if 'QH' in df.iloc[index]['Trigger Type']:
                            QHidx_Fire = self.__ExtractQHidx(df.iloc[index]['Trigger Type'], QHpairs)
                            t_QH[:] = t_QH_Fire
                            t_QH[QHidx_Fire] = QH_delay
                        else: t_QH[:] = QH_delay
                    else: t_QH[:] = QH_delay
                    t_QH[t_noFire] = 9999
                    a.setAttribute("Inputs", "tQH", t_QH)
                else:
                    a.setAttribute("Inputs", "tQH", [9999] * len(a.getAttribute("Inputs", "tQH")))

                a.writeFileLEDET( os.path.join(OutputDirectory, MagnetName+ '_'+str(index)+'.xlsx'))
                SimNumbers.append(index)
        return

    #############################################################################################################
    ## Domain: Functions used by both SIMdata/TMDSdata
    def __zero_runs(self, I, Itol = 10):
        if len(I.shape)<2: I = np.array([I]).transpose()
        I[abs(I) < Itol] = 0
        iszero = np.concatenate(([0], np.equal(I[:,0], 0).view(np.int8), [0]))
        absdiff = np.abs(np.diff(iszero))
        ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
        return ranges

    def __FrequencyCLIQ(self, I_CLIQ, SIM = 0, TDMS = 0, F_CYCLE = 1, Plot = 0, I_tol = 50):
        if SIM: TimeFrame = self.SIMdata.TimeFrame
        elif TDMS: TimeFrame = self.TDMSdata.TimeFrame_MF
        else:
            print('Please specify which frequency shall be calculated. [SIM = 1/ TDMS = 1]')
            return np.array([0])
        I_CLIQ_copy = I_CLIQ
        I_CLIQ_copy[abs(I_CLIQ_copy) < I_tol] = 0
        zeros = self.__zero_runs(I_CLIQ_copy)

        l_Ic = int(len(I_CLIQ)/2)
        if not len(zeros)>1 or abs(sum(I_CLIQ[:l_Ic])/len(I_CLIQ[:l_Ic]))<1.2*abs(sum(I_CLIQ[l_Ic:])/len(I_CLIQ[l_Ic:])):
            if self.verbose: print('No CLIQ signal found.')
            return 0
        t_Start = TimeFrame[zeros[0][1]]
        zero_cycles = zeros[:-1]
        cycles = 0.5

        f_CLIQ = np.array([])
        for i in range(1,len(zero_cycles)):
            t_end = sum(TimeFrame[zero_cycles[i][0]:zero_cycles[i][1]])/(zero_cycles[i][1]- zero_cycles[i][0])
            # compensate a cycle if the zero-cycle was not detected
            zc_check = (sum(I_CLIQ[zero_cycles[i-1][1]:zero_cycles[i][0]])/(zero_cycles[i][0]-zero_cycles[i-1][1]))/np.max(abs(I_CLIQ[zero_cycles[i-1][1]:zero_cycles[i][0]]))
            if abs(zc_check) < 0.2: cycles = cycles + 0.5
            T = (t_end - t_Start)
            f = cycles/ T
            f_CLIQ = np.append(f_CLIQ, f)
            cycles = cycles+0.5

        if Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(TimeFrame, I_CLIQ)
            ax.grid(True)
        if len(f_CLIQ)<2: F_CYCLE = 0
        return f_CLIQ[F_CYCLE]

    def _CalculateCLIQCapacitance(self, TimeFrame, I_CLIQ, U_CLIQ, kernel_size, I_tol = 50):
        if len(I_CLIQ.shape)<2: I_CLIQ = np.array([I_CLIQ]).transpose()
        if len(U_CLIQ.shape) < 2: U_CLIQ = np.array([U_CLIQ])
        if len(TimeFrame.shape) < 2: TimeFrame = np.array([TimeFrame]).transpose()

        filtered = signal.medfilt(U_CLIQ[0], kernel_size=kernel_size)
        I_filt = signal.medfilt(I_CLIQ[:, 0], kernel_size=5)

        I_filt[abs(I_filt)<I_tol] = 0
        zeros = self.__zero_runs(signal.medfilt(I_filt, kernel_size=5))
        cutIdx = zeros[-1][0]
        IntI = simps(I_CLIQ[:cutIdx,0], TimeFrame[:cutIdx,0])
        U0 = filtered[0]

        if len(filtered)-2000 > cutIdx: offIdx = -2000
        elif len(filtered)-1000 > cutIdx: offIdx = -1000
        else: offIdx = cutIdx
        Uoffset = sum(filtered[offIdx:])/len(filtered[offIdx:])
        Uend = filtered[cutIdx]-Uoffset
        C = abs(IntI) /abs((Uend-U0))
        if self.verbose: print('Measured CLIQ capacitance: ', C * 1000, ' mF')
        return C

    def __calculateQuenchIntegral(self, time, current):
        dt = np.gradient(time)
        QL = np.sum(np.multiply(dt, np.power(current, 2))) / 1E6
        return QL

    def _FindFiring(self, I, TimeFrame, dI_tol = 10):
        t_Start = []
        if len(TimeFrame.shape) < 2: TimeFrame = np.array([TimeFrame]).transpose()
        if len(I.shape)<2:
            I = np.array([I]).transpose()
            zeros = self.__zero_runs(I, Itol = dI_tol)
            if not len(zeros) > 0 or abs(sum(I) / len(I)) < 0.5 or zeros[0][1] == len(I):
                if self.verbose: print('No signal found.')
                return np.nan
            t_Start = TimeFrame[zeros[0][1]]
        else:
            for i in range(I.shape[1]):
                I_c = np.array([I[:,i]]).transpose()
                zeros = self.__zero_runs(I_c, Itol = dI_tol)
                if not len(zeros) > 0 or abs(sum(I_c ) / len(I_c )) < 0.5 or zeros[0][1] == len(I):
                    t_Start.append(np.nan)
                    if self.verbose: print('No signal found.')
                    continue
                t_Start.append(TimeFrame[zeros[0][1]][0])
        return np.round(t_Start,7)

    def AvailableVoltageTaps(self):
        print('*** Available Voltage-taps ***')
        print(list(self.MergedVoltages.keys()))

    def AvailableCoils(self):
        print('*** Available Coils ***')
        current_coil = 0
        for i in range(len(self.TDMSdata.VoltageVertices)):
            c_coil = self.TDMSdata.VoltageVertices[i][1]
            if c_coil != current_coil:
                print(c_coil)
                current_coil = c_coil

    def GetCoilStructure(self, Print = 0, Plot = 1):
        if Print:
            print('*** Turn to Tap binding: ***')
            for key in self.MergedVoltages.keys():
                print('Voltage tap ', key, " --> ", self.MergedVoltages[key])
        if Plot:
            fig = plt.figure(figsize=(12,12))
            ax = fig.add_subplot(111)
            count = 0
            legend =[]
            for key in self.MergedVoltages.keys():
                idxTap = self.MergedVoltages[key]
                legend.append(key)
                ax.scatter(self.SIMdata.XY_mag_ave[0,idxTap.astype(int)-1], self.SIMdata.XY_mag_ave[1,idxTap.astype(int)-1], s = 10, c = self.Colors[count])
                count = count + 1
            ax.axis('equal')
            ax.grid('minor')
            ax.set_xlabel("x [mm]")
            ax.set_ylabel("y [mm]")
            ax.set_title("Turns to V-Taps")
            ax.legend(legend, loc='best', bbox_to_anchor=(1.05, 1.0))
            plt.tight_layout()

        return

    def GetTDMSCoilStructure(self):
        print('*** Provided eletrical connections in TDMS data ***')
        CoilCount = 0
        for i in range(len(self.TDMSdata.VoltageVertices)):
            temp = self.TDMSdata.VoltageVertices[i][1]
            if CoilCount != temp:
                CoilCount = temp
                print("*** Coil: ", CoilCount)
            print("-->",self.TDMSdata.VoltageVertices[i][2]+self.TDMSdata.VoltageVertices[i][3],
                  " to ", self.TDMSdata.VoltageVertices[i][4]+self.TDMSdata.VoltageVertices[i][5])
        return

    #############################################################################################################
    ## Domain: Handle SIM data Object
    def __CreateSIMDataObject(self):
        if self.SIMdata.FileName.endswith('.mat'):
            file = self.SIMdata.FileName
            f = h5py.File(file, 'r')
            self.SIMdata.TimeFrame = np.array(f.get("time_vector"))
            self.SIMdata.I_CoilSections = np.array(f.get("I_CoilSections")).transpose()
            self.SIMdata.I_CLIQ = np.array(f.get("Ic")) .transpose()
            trigger = np.array(f.get("t_PC"))[0][0]-self.beforePC
            if trigger < float(self.SIMdata.TimeFrame[0]):
                self.beforePC = -1* self.SIMdata.TimeFrame[0]
                trigger = np.array(f.get("t_PC"))[0][0] - self.beforePC
                if self.verbose: print("Switch aligning to tStart of Simulation!")
            trigger_shoot = np.where(abs(self.SIMdata.TimeFrame-trigger)<1E-4)[0][0]
            self.SIMdata.trigger_PC = np.where(abs(self.SIMdata.TimeFrame-np.array(f.get("t_PC"))[0][0])<1E-7)[0][0]
            self.SIMdata.TimeFrame = self.SIMdata.TimeFrame[trigger_shoot:]
            self.SIMdata.I_CoilSections = self.SIMdata.I_CoilSections[:, trigger_shoot:]
            self.SIMdata.I_CLIQ = self.SIMdata.I_CLIQ[trigger_shoot:]
            self.SIMdata.f_CLIQ = self.__FrequencyCLIQ(self.SIMdata.I_CLIQ, SIM=1)
            self.SIMdata.directionsCLIQ = np.array(f.get("directionCurrentCLIQ"))
            U_CLIQ = np.array(f.get("Uc"))
            self.SIMdata.U_CLIQ = U_CLIQ[:][trigger_shoot:]
            if self.SIMdata.f_CLIQ > 0:
                self.SIMdata.C_CLIQ = self._CalculateCLIQCapacitance(self.SIMdata.TimeFrame, self.SIMdata.I_CLIQ,
                                                                     self.SIMdata.U_CLIQ, 3)
            I_QH = np.array(f.get("I_QH"))
            self.SIMdata.I_QH = I_QH[:][trigger_shoot:]
            U_QH = np.array(f.get("U_QH"))
            self.SIMdata.U_QH = U_QH[:][trigger_shoot:]
            self.SIMdata.XY_mag_ave = np.array(f.get("XY_MAG_ave"))
            TimeToQuench = np.array(f.get("timeToQuench"))
            idxQuench = np.argmin(TimeToQuench)
            tQuench = np.min(TimeToQuench)
            self.SIMdata.Quenches = [idxQuench, tQuench, 0]
            T_ht = np.array(f.get("T_ht"))
            self.SIMdata.Thotspot = [np.max(T_ht), np.unravel_index(np.argmax(T_ht),T_ht.shape)]
            self.SIMdata.T_adiabatic = np.array(f.get("HotSpotT"))
            self.SIMdata.U_CoilSections = np.array(f.get("peakUground_half_turns"))
            self.SIMdata.el_connections = np.array(f.get("el_order_half_turns"))
            self.SIMdata.Uturn_half_turns = np.array(f.get("Uturn_half_turns_reordered"))
        else:
            print("Please provide .mat file for Simulation.")

    def __FindQuenchSIM(self, tQuench):
        if tQuench == tQuench:
            try:
                idxQuench = np.where(abs(self.SIMdata.TimeFrame - float(tQuench)) < 1E-7)[0][0]
            except:
                try:
                    idxQuench = np.where(abs(self.SIMdata.TimeFrame - float(tQuench)) < 1E-4)[0][0]
                except:
                    if self.verbose: print("Quench time not found in simulation time frame, t=", tQuench)
                    idxQuench = 0
        else:
            idxQuench = -3#self.SIMdata.trigger_PC
        return idxQuench

    #############################################################################################################
    ## Domain: Handle TDMS data object
    def __CreateTDMSDataObject(self):
        tdms_file = TdmsFile.read(self.TDMSdata.FileName)
        ## Save groups
        for group in tdms_file.groups():
            if group.name == 'HF': self.TDMSdata.groupHF = tdms_file['HF']
            elif group.name == 'MF': self.TDMSdata.groupMF = tdms_file['MF']
            else: print("Don't understand group: ", group)

        ## Pick channels and store conveniently
        I_Heaters = []
        U_Heaters = []
        for channel in self.TDMSdata.groupHF.channels():
            if channel.name == 'IDCCT_HF': self.TDMSdata.I_DCCT_HF = channel.data
        for channel in self.TDMSdata.groupMF.channels():
            if channel.name == 'IDCCT_HF':
                self.TDMSdata.I_DCCT_MF = channel.data*1000
                self.TDMSdata.t_steps_MF = channel.properties['wf_samples']
                self.TDMSdata.t_d_MF = channel.properties['wf_increment']
            if channel.name == 'Trigger_PC':
                trigger_data = channel.data
            if channel.name == 'I Cliq':self.TDMSdata.I_CLIQ = channel.data
            if channel.name == 'V Cliq': self.TDMSdata.U_CLIQ = channel.data
            if channel.name.startswith("I_Heater"): I_Heaters.append(channel.name)
            if channel.name.startswith("U_Heater"): U_Heaters.append(channel.name)
        ## Set up Timeframe
        self.TDMSdata.TimeFrame_MF = np.linspace(0,self.TDMSdata.t_steps_MF*self.TDMSdata.t_d_MF, int(self.TDMSdata.t_steps_MF))
        #self.TDMSdata.goupHF['IDCCT_HF'].time_track()
        trigger_shoot = np.gradient(trigger_data, self.TDMSdata.t_d_MF)
        trigger_shoot = np.where(abs(trigger_shoot)>self.TDMSdata.Tolerance)[0][0]-int(self.beforePC/self.TDMSdata.t_d_MF)
        self.TDMSdata.trigger_PC = int(self.beforePC/self.TDMSdata.t_d_MF)
        self.TDMSdata.trigger_shoot = trigger_shoot
        self.TDMSdata.TimeFrame_MF = self.TDMSdata.TimeFrame_MF[trigger_shoot:]-self.TDMSdata.TimeFrame_MF[trigger_shoot]\
                                     -self.TDMSdata.TimeFrame_MF[self.TDMSdata.trigger_PC+1]
        self.TDMSdata.I_DCCT_MF = self.TDMSdata.I_DCCT_MF[trigger_shoot:]
        self.TDMSdata.I_CLIQ = self.TDMSdata.I_CLIQ[trigger_shoot:]
        self.TDMSdata.U_CLIQ = self.TDMSdata.U_CLIQ[trigger_shoot:]
        self.TDMSdata.f_CLIQ = self.__FrequencyCLIQ(self.TDMSdata.I_CLIQ, TDMS= 1)
        if self.TDMSdata.f_CLIQ > 0:
            self.TDMSdata.C_CLIQ = self._CalculateCLIQCapacitance(self.TDMSdata.TimeFrame_MF, self.TDMSdata.I_CLIQ,
                                                                  self.TDMSdata.U_CLIQ, 17)
        self.__FillHeaterArrays(I_Heaters, trigger_shoot)
        self.__FillHeaterArrays(U_Heaters, trigger_shoot)
        self.__CreateVoltageVertices()
        return

    def __FillHeaterArrays(self, Heaters, trigger_shoot):
        Heat_len = len(self.TDMSdata.groupMF[Heaters[0]].data[trigger_shoot:])
        if Heaters[0].startswith('I'): self.TDMSdata.I_QH = np.zeros((len(Heaters), Heat_len))
        elif Heaters[0].startswith('U'): self.TDMSdata.U_QH = np.zeros((len(Heaters), Heat_len))
        for k in Heaters:
            order = int(k[-1])
            if Heaters[0].startswith('I'): self.TDMSdata.I_QH[order-1] = self.TDMSdata.groupMF[k].data[trigger_shoot:]
            elif Heaters[0].startswith('U'): self.TDMSdata.U_QH[order-1] = self.TDMSdata.groupMF[k].data[trigger_shoot:]

    def __CreateVoltageVertices(self):
        ## 1. Extract all channels that are relevant
        # Version 1
        temp_Sections_1 = re.compile("([a-zA-Z]+)([0-9]+)([a-zA-Z]+)([0-9]+)([a-zA-Z]+)([0-9]+)")
        temp_Coils_1 = re.compile("([0-9]+)([a-zA-Z]+)")
        CSections = []
        Coils = []
        Coils_Diff = []

        for channel in self.TDMSdata.groupMF.channels():
            if channel.properties['TransducerType'] == 'vtaps':
                chName = channel.name.replace("_"," ")
                chName = chName.replace("-"," ")
                chName = chName.replace(" ", "")
                try:
                    res = temp_Sections_1.match(chName).groups()
                    ChN = res + (str(res[0]+res[1]+'_'+res[2]+res[3]+"_"+res[4]+res[5]),) + (str(res[0]+res[1]+'_'+res[4]+res[5]+"_"+res[2]+res[3]),)+ (channel.name,)
                    CSections.append(ChN)
                except:
                    chName = channel.name.replace("_", "I")
                    chName = chName.replace("-", "O")
                    chName = chName.replace(" ", "")
                    try:
                        res = temp_Sections_1.match(chName).groups()
                        ChN = res + (str(res[0] + res[1] + '_'  + res[3] + "_" + res[5]),) + (
                        str(res[0] + res[1] + '_' + res[5] + "_"  + res[3]),) + (channel.name,)
                        CSections.append(ChN)
                    except:
                        pass
                if chName.startswith("Vcoil"):
                    try:
                        res = temp_Coils_1.match(chName[5:]).groups()
                        ChN = res + (channel.name,)
                        Coils_Diff.append(ChN)
                    except:
                        Coils.append((chName[5:], channel.name))

        ## 2. order them in coils
        def getKey0(item):
            return item[0]
        def getKey1(item):
            return item[1]
        CSections = sorted(CSections, key=getKey1)
        Coils = sorted(Coils, key=getKey0)
        Coils_Diff = sorted(Coils_Diff, key=getKey0)

        self.TDMSdata.VoltageVertices = CSections

        ##TODO: also construct sth. for Diffs and Coils

        return

    def ProvideTurnsToCoilStructure(self, Coil = [], CoilCsv = ''):
        if Coil:
            if not self.MergedVoltages:
                for i in range(len(Coil)):
                    self.MergedVoltages = {**self.MergedVoltages, **Coil[i]}
                MVcopy = self.MergedVoltages.copy()
                counter = 0
                for old_key in MVcopy.keys():
                    if len(self.MergedVoltages[old_key]) == 0:
                        self.MergedVoltages.pop(old_key)
                    else:
                        found = 0
                        for i in range(len(self.TDMSdata.VoltageVertices)):
                            if old_key == self.TDMSdata.VoltageVertices[i][6] or  old_key == self.TDMSdata.VoltageVertices[i][7]:
                                new_key = self.TDMSdata.VoltageVertices[i][8]
                                self.MergedVoltages[new_key] = self.MergedVoltages.pop(old_key)
                                # if int(self.TDMSdata.VoltageVertices[i][3]) > int(self.TDMSdata.VoltageVertices[i][5]):
                                #     if self.TDMSdata.VoltageVertices[i][2] == 'I' and self.TDMSdata.VoltageVertices[i][4] == 'O':
                                #         self.MergedVoltagesPolarities[new_key] = 1
                                #     else: self.MergedVoltagesPolarities[new_key] = -1
                                # else:
                                #     self.MergedVoltagesPolarities[new_key] = 1
                                self.MergedVoltagesPolarities[new_key] = self.CopyMVP[counter]
                                counter = counter + 1
                                found = 1
                                break
                        if not found:
                            if self.verbose: print("Couldn't find voltage-tap: {} in TDMS.".format(old_key))
                            self.MergedVoltages.pop(old_key)
                    counter = counter +1
                return
            else:
                self.__CreateTDMSDataObject()
                self.ProvideTurnsToCoilStructure(Coil)
                return
        elif CoilCsv:
            with open(CoilCsv, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                counter = 0
                c_coil = 0
                turn_count = 0
                current_dict = {}
                Coil = []
                for row in csv_reader:
                    if not any(row): continue
                    if not row[0]: continue
                    if counter<2:
                        counter = counter +1
                        continue
                    current_coil = row[0]
                    if current_coil != c_coil:
                        if current_dict: Coil.append(current_dict)
                        current_dict = {}
                        c_coil = current_coil

                    if float(row[0])<100:
                        key_name = 'P' + row[0] + '_' + row[1] + '-' + row[2]
                    else:
                        key_name = 'C'+row[0]+'_'+row[1]+'_'+row[2]
                    nTurns = float(row[3])
                    if nTurns == 0: continue
                    turns = self.SIMdata.el_connections[turn_count:turn_count+int(nTurns*2)]
                    current_dict[key_name] = turns[:,0]
                    turn_count = turn_count + int(nTurns*2)
                    self.CopyMVP.append(float(row[4]))
                Coil.append(current_dict)
            self.ProvideTurnsToCoilStructure(Coil)
            return
        else:
            print('Please provide either Coil-Dictionary or CSV-File containing the voltage-tap to turn binding')
            return

    def FindQuenchTDMS(self, Vthreshold, ValidationTime, Plot=1):
        found = []
        if not self.MergedVoltages:
            print("Please first provide Coil-Structure. ")
            print("Obj.ProvideTurnsToCoilStructure(self, TurnsToVtaps: Dict)")
            return

        for key in self.MergedVoltages.keys():
            Udata = self.TDMSdata.groupMF[key].data
            if self.TDMSdata.trigger_shoot > 10000:
                offset = np.sum(Udata[:10000]) / 10000
                Udata = Udata - offset
                Vthr = Vthreshold
            else:
                print("Failed to calculate SNR for Voltage channel.")
                return
            Qidx = np.where(abs(Udata[:self.TDMSdata.trigger_shoot+self.TDMSdata.trigger_PC]) > Vthr)[0]
            Qidx = Qidx[np.where(Qidx-self.TDMSdata.trigger_shoot > 0)[0]]
            if len(Qidx)> 0:
                for i in range(len(Qidx)):
                    tSteps = int(ValidationTime / self.TDMSdata.t_d_MF)
                    QQidx = np.where(abs(Udata[Qidx[i]:Qidx[i] + tSteps]) > Vthr)[0]
                    if len(QQidx) >= (0.95*tSteps) and (Qidx[i]+tSteps)<(self.TDMSdata.trigger_shoot+self.TDMSdata.trigger_PC):
                        tQuench = self.TDMSdata.TimeFrame_MF[Qidx[i]-self.TDMSdata.trigger_shoot]
                        idx_tQuench = Qidx[i]-self.TDMSdata.trigger_shoot
                        found.append((key,  tQuench, idx_tQuench))
                        if Plot:
                            # try:
                            fig = plt.figure()
                            ax = fig.add_subplot(111)
                            ax.grid(True)
                            ax.set_title("Detected quench in - "+key)
                            ax.set_ylim([-3*Vthr,3*Vthr])
                            ax.set_xlabel("Time, t [ms]")
                            ax.set_ylabel("Voltage [V]")
                            if idx_tQuench-tSteps<0: tSteps = idx_tQuench
                            ax.plot(self.TDMSdata.TimeFrame_MF[idx_tQuench-tSteps:idx_tQuench+int(5*tSteps)]*1000, Udata[Qidx[i]-tSteps:Qidx[i]+int(5*tSteps)],'--')
                            ax.axvline(self.TDMSdata.TimeFrame_MF[idx_tQuench]*1000,c='r')
                            ax.axhline(Vthr, c='r', ls='--')
                            ax.legend(["$U_{Res,"+key+"}$","$t_{Quench}$","$U_{Threshold}$"])
                            # except:
                            #     pass
                        break
            # fig = plt.figure()
            # ax = fig.add_subplot(111)
            # ax.set_title(key)
            # ax.plot(np.linspace(0, len(Udata), len(Udata)), Udata, '--')
            # ax.set_xlim([self.TDMSdata.trigger_shoot-50,self.TDMSdata.trigger_shoot+50+self.TDMSdata.trigger_PC])
            # ax.set_ylim([-5*Vthr, 5*Vthr])
        if not found:
            print("No quench detected.")
            found.append(("NaN",0,self.TDMSdata.trigger_PC))
        else:
            def getSecond(elem):
                return elem[1]
            found.sort(key=getSecond)
            print("*** Ordered detected Quenches ***")
            for j in range(len(found)):
                print("Detected Quench in {} at {} ms".format(found[j][0], np.round(found[j][1] * 1000, 2)))

            if Plot:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                count = 0
                legend = []
                for j in range(len(found)):
                    key = found[j][0]
                    idxTap = self.MergedVoltages[key]
                    tx = str(count) + ": " + key + " at " + str(np.round(found[j][1] * 1000, 2)) + " ms"
                    legend.append(tx)
                    cmap = cm.get_cmap('winter', len(found))
                    c = cmap(abs(found[j][1]*1000) / abs(found[0][1]*1000))
                    c = np.array([c])
                    pos = ax.scatter(self.SIMdata.XY_mag_ave[0, idxTap.astype(int) - 1],
                               self.SIMdata.XY_mag_ave[1, idxTap.astype(int) - 1], s=10, c=c)
                    count = count + 1
                ax.axis('equal')
                ax.grid('minor')
                ax.set_xlabel("x [mm]")
                ax.set_ylabel("y [mm]")
                ax.set_title("Detected Quenches")
                ax.legend(legend)
        self.TDMSdata.Quenches = np.array(found)

    def ExtractFeatures(self):
        ## Extract Timing features:
        print('Timing')
        # # Extract t_PC
        dIdt_Coil = np.zeros((self.SIMdata.I_CoilSections.shape))
        for i in range((dIdt_Coil.shape[1])):
            dIdt_Coil[:,i] = np.gradient(self.SIMdata.I_CoilSections[:,i], self.SIMdata.TimeFrame[:,0])
        print('t_PC_Sim: ', self._FindFiring(dIdt_Coil, self.SIMdata.TimeFrame))
        dIdt_Coil = np.gradient(signal.medfilt(self.TDMSdata.I_DCCT_MF, kernel_size = 17), self.TDMSdata.TimeFrame_MF)
        print('t_PC_Meas: ', self._FindFiring(dIdt_Coil, self.TDMSdata.TimeFrame_MF, dI_tol = 10000))
        # # Extract t_QH
        dIdt_QH = np.zeros((self.SIMdata.I_QH.shape))
        for i in range((dIdt_QH.shape[0])):
            dIdt_QH[i,:] = np.gradient(self.SIMdata.I_QH[i,:], self.SIMdata.TimeFrame[:,0])
        print('t_QH_Sim: ', self._FindFiring(dIdt_QH.transpose(), self.SIMdata.TimeFrame))
        dIdt_QH = np.zeros((self.TDMSdata.I_QH.shape))
        for i in range((dIdt_QH.shape[0])):
            dIdt_QH[i,:] = np.gradient(signal.medfilt(self.TDMSdata.I_QH[i,:], kernel_size = 11), self.TDMSdata.TimeFrame_MF)
        print('t_QH_Meas: ', self._FindFiring(dIdt_QH.transpose(), self.TDMSdata.TimeFrame_MF, dI_tol=1000))
        # # # Extract t_CLIQ
        dIdt_CLIQ = np.gradient(self.SIMdata.I_CLIQ[:,0], self.SIMdata.TimeFrame[:,0])
        print('t_CLIQ_Sim: ', self._FindFiring(dIdt_CLIQ, self.SIMdata.TimeFrame))
        dIdt_CLIQ = np.gradient(signal.medfilt(self.TDMSdata.I_CLIQ, kernel_size = 11), self.TDMSdata.TimeFrame_MF)
        print('t_CLIQ_Meas: ', self._FindFiring(dIdt_CLIQ, self.TDMSdata.TimeFrame_MF, dI_tol = 5000))
        # # # Extract t_EE
        # # Extract t_Quench [if applicable]

        ## Extract electrical parameters
            # Extract correct, precise current level
            # Done # Extract f and C_CLIQ
            # Extract CLIQ direction
            # Extract R_Circuit
            # What about R_Crowbar/Ud_Crowbar/R_CLIQ/R_QH

        ## Extract further properties
            #To be seen if in this function
        return 0

    #############################################################################################################
    ## Domain: General Functions, meant to be used from outside
    def calculateQuenchIntegral_tQL(self, tQL):
        idxQuench = self.__FindQuenchSIM(tQL)
        if abs(sum(self.SIMdata.I_CLIQ)) > 0:
            idxC = np.argmax(self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC + 2, :])
            QL = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[idxQuench:, 0],
                                                              self.SIMdata.I_CoilSections[idxQuench:,
                                                              idxC])
        else:
            QL = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[idxQuench:, 0],
                                                              self.SIMdata.I_CoilSections[idxQuench:, 0])
        return QL

    def calculateAllQuenchIntegrals(self, SIM = 1, TDMS = 1):
        ## QL Integral 1 - from Quench
        ## QL Measured Data
        if TDMS:
            if not self.TDMSdata.Quenches.size > 0: self.FindQuenchTDMS(0.1, 0.007, Plot =0)
            idxQuench_TDMS = int(self.TDMSdata.Quenches[0][2])
            self.TDMSdata.QL1 = self.__calculateQuenchIntegral(self.TDMSdata.TimeFrame_MF[idxQuench_TDMS:],
                                                               self.TDMSdata.I_DCCT_MF[idxQuench_TDMS:])
        ## QL Sim Data
        if SIM:
            idxQuench_SIM = self.__FindQuenchSIM(self.SIMdata.Quenches[1])
            self.SIMdata.Quenches[2] = idxQuench_SIM
            if abs(sum(self.SIMdata.I_CLIQ)) > 0:
                idxC = np.argmax(self.SIMdata.I_CoilSections[idxQuench_SIM,:])
                self.SIMdata.QL1 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[idxQuench_SIM:, 0],
                                                                  self.SIMdata.I_CoilSections[idxQuench_SIM:,
                                                                  idxC])
            else:
                self.SIMdata.QL1 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[idxQuench_SIM:, 0],
                                                                  self.SIMdata.I_CoilSections[idxQuench_SIM, 0])
        ## QL Integral 2  - from tPC
        ## QL Measured Data
        if TDMS:
            self.TDMSdata.QL2 = self.__calculateQuenchIntegral(self.TDMSdata.TimeFrame_MF[self.TDMSdata.trigger_PC:],
                                                               self.TDMSdata.I_DCCT_MF[self.TDMSdata.trigger_PC:])
        ## QL Sim Data
        if SIM:
            if abs(sum(self.SIMdata.I_CLIQ)) > 0:
                idxC = np.argmax(self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC+2,:])
                self.SIMdata.QL2 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[self.SIMdata.trigger_PC:, 0],
                                                                  self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC:,
                                                                  idxC])
            else:
                self.SIMdata.QL2 = self.__calculateQuenchIntegral(self.SIMdata.TimeFrame[self.SIMdata.trigger_PC:, 0],
                                                                  self.SIMdata.I_CoilSections[self.SIMdata.trigger_PC:, 0])

    def QuenchPlanAnalysis(self, Plot = 0):
        # Plot current together
        if Plot:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            legend = []
            for i in range(self.SIMdata.I_CoilSections.shape[1]):
                legend.append("$I_{Sim, CoilSection " + str(i+1) + "}$")
                ax.plot(self.SIMdata.TimeFrame, self.SIMdata.I_CoilSections[:,i], color= self.Colors[i])
            if sum(self.SIMdata.I_CLIQ) != 0:
                ax.plot(self.SIMdata.TimeFrame, self.SIMdata.I_CLIQ, color= self.Colors[self.SIMdata.I_CoilSections.shape[1]+1])
                legend.append("$I_{Sim,CLIQ}$")
                ax.plot(self.TDMSdata.TimeFrame_MF, self.TDMSdata.I_CLIQ, color=self.Colors[self.SIMdata.I_CoilSections.shape[1]+2])
                legend.append("$I_{Meas,CLIQ}$")
            ax.plot(self.TDMSdata.TimeFrame_MF, self.TDMSdata.I_DCCT_MF, color= self.Colors[self.SIMdata.I_CoilSections.shape[1]+3])
            legend.append("$I_{Meas}$")
            ax.grid(True)
            ax.set_ylabel("Current [A]", fontsize=20)
            ax.set_xlabel("Time [s]", fontsize=20)
            #ax.set_ylim([np.amin([np.amin(self.SIMdata.I_CoilSections),np.amin(self.SIMdata.I_CLIQ), np.amin(self.TDMSdata.I_DCCT_MF)])*1.1,
            #             np.amax([np.amax(self.SIMdata.I_CoilSections),np.amax(self.SIMdata.I_CLIQ), np.amax(self.TDMSdata.I_DCCT_MF)])*1.1])
            #ax.set_xlim([0, np.amax([np.amax(self.TDMSdata.TimeFrame_MF), np.amax(self.SIMdata.TimeFrame)])])
            ax.legend(legend,fontsize=20)
            ax.set_title(self.TDMSdata.FileName[-13:])
        return [self.TDMSdata, self.SIMdata]

    def PlotVoltageTap(self, Coil = '', TapName = ''):
        if not Coil:
            if TapName:
                title = TapName
                Coil = [TapName]
            else:
                print('Please provide tap-name or coil to plot.')
                return
        elif Coil:
            title = 'Coil '+str(Coil)
            newC = []
            for l in range(len(self.TDMSdata.VoltageVertices)):
                if Coil == int(self.TDMSdata.VoltageVertices[l][1]):
                    newC.append(self.TDMSdata.VoltageVertices[l][6])
            Coil = newC
        fig = plt.figure(figsize=(12,12))
        ax = fig.add_subplot(111)
        ax.grid(True)
        leg = []
        for c in range(len(Coil)):
            TapName = Coil[c]
            realTapName = ''
            for i in range(len(self.TDMSdata.VoltageVertices)):
                if self.TDMSdata.VoltageVertices[i][6] ==  TapName or self.TDMSdata.VoltageVertices[i][7] == TapName:
                    realTapName = self.TDMSdata.VoltageVertices[i][8]
            if not realTapName:
                print('Voltage Tap not found.')
                return
            try:
                MVidx = list(self.MergedVoltages.keys()).index(realTapName)
            except:
                try:
                    _ = self.TDMSdata.groupMF[realTapName]
                    print('Skip Voltage-tap ', realTapName, ' as no turns are bound to it [E1: MagnetEnds]')
                    continue
                except:
                    print('Voltage tap ', realTapName, ' was not found in TDMS data.')
                    continue
            LEDET_U = np.sum(self.SIMdata.Uturn_half_turns[self.MergedVoltages[realTapName].astype(int)-1], axis=0)*self.MergedVoltagesPolarities[realTapName]
            TDMS_U = self.TDMSdata.groupMF[realTapName].data[self.TDMSdata.trigger_shoot:]
            print_rTN = realTapName.replace('_', '-')
            ax.plot(self.TDMSdata.TimeFrame_MF, TDMS_U, '-', color= self.Colors[c])
            leg.append('$U_{Meas,' + print_rTN + '}$')
            ax.plot(self.SIMdata.TimeFrame, LEDET_U, '--', color= self.Colors[c])
            leg.append('$U_{Sim,' + print_rTN + '}$')
            ax.grid(True)
        ax.legend(leg,fontsize=14)
        ax.set_title(title)
        ax.set_ylabel("Voltage [V]", fontsize=20)
        ax.set_xlabel("Time [s]", fontsize=20)
        return

    def SaveToCSV(self):
        # TODO
        return
