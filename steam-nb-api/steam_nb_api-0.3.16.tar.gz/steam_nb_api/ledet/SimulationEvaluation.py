from scipy.interpolate import interp1d
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.collections import PolyCollection
import h5py
from steam_nb_api.ledet.ParameterSweep import *

def EvaluateSimulations(MatFolder, MagnetName, MeasFile, SweepObject, Mat = True, Plots = True, SkipAlign = False, SetdITol = 200, showBestFit = 10):
    print("Reading Data and evaluate")
    #Collect Simulated Data
    flag_BasePoints = 0
    BasePoints = 0
    SimData = np.array([])
    RData = np.array([])
    items = os.listdir(MatFolder)
    with tqdm(total=len(items)/2) as pbar:
        for item in items:
            try:
                if Mat:
                    if item.endswith('.mat'):
                        if ".sys" not in item:
                            num = item.replace('SimulationResults_LEDET_', '')
                            num = num.replace(".mat", '')
                            f = h5py.File(MatFolder+"//" + item, 'r')
                            T = np.array(f.get("time_vector"))
                            if not flag_BasePoints:
                                BasePoints = T.shape[0]
                                SimData = np.zeros((1, BasePoints + 1))
                                SimData[0, :] = np.append([0], T.astype(float))
                                flag_BasePoints = 1
                            data = f.get("I_CoilSections")
                            ILedet = np.append([num], np.array(data[0]))
                            try:
                                data = f.get("R_CoilSections")
                                RLedet = np.append([num], np.array(data))
                                RData = np.vstack((RData, RLedet.astype(float)))
                            except:
                                pass
                            SimData = np.vstack((SimData, ILedet.astype(float)))

                if not Mat:
                    if item.endswith('.txt') and 'VariableHistory' in item:
                        if ".sys" not in item:
                            num = item.replace(MagnetName + '_VariableHistory_', '')
                            num = num.replace(".txt", '')
                            try:
                                x = int(num)
                            except:
                                print("Magnetname does not fit to file names. Please check!")
                                return
                            with open(MatFolder+"//" + item, 'r') as file:
                                k = file.readline().split(',')[:-1]
                                try:
                                    idxT = k.index('time_vector')
                                except:
                                    idxT = k.index(' time_vector')
                                idxI = k.index(' I_CoilSections_1')
                                rows = [[float(x) for x in line.split(',')[:-1]] for line in file]
                                cols = [list(col) for col in zip(*rows)]
                                try:
                                    idxR = k.index(' R_CoilSections_1')
                                    R = np.array(cols[idxR])
                                    T  = np.array(cols[idxT])
                                    RLedet = np.append([num], np.array(R))
                                    if RData.size == 0:
                                        RData = RLedet.astype(float)
                                    elif not T.size == SimData[0, :].size:
                                        RL = interp1d(T, np.array(RLedet[1:]), kind='cubic')
                                        RLedet = RL(SimData[0, :])
                                        RData = np.vstack((RData, RLedet.astype(float)))
                                except:
                                    print("Error reading R, no abort")
                                    pass
                                T = np.array(cols[idxT])
                                ISim = np.array(cols[idxI])
                            if not flag_BasePoints:
                                BasePoints = T.shape[0]
                                SimData = np.append([0], T)
                            #Check if size is the same
                            if flag_BasePoints:
                                if not T.size == SimData[0,:].size:
                                    IL = interp1d(T, np.array(ISim), kind='cubic')
                                    ISim = IL(SimData[0,1:])
                            ILedet = np.append([num], np.array(ISim))
                            SimData = np.vstack((SimData, ILedet.astype(float)))
                            flag_BasePoints = 1
            except:
                 print("Reading of " + item + " was not successful")
                 continue
            pbar.update(1)
    if SimData.size != 0:
        print("Reading Data was successful")
    else:
        print("Error while reading. Please check files")
        return

    Time_Zone = [float(T[0]), float(T[-1])]

    #Prepare Measured Data
    mat = pd.read_csv(MeasFile)
    Tmeas = np.array(mat.iloc[:, 0])
    try:
        Imeas = mat["IAB.I_A"].values
    except:
        try:
            Imeas = mat["STATUS.I_MEAS"].values
        except:
            try:
                Imeas = mat["IABI_A"].values
            except:
                print("Measured Data is unknown. Neither I_A nor I_MEAS")
                return

    if not SkipAlign:
        #Find Start-IDX
        idx_up = np.argmin(abs(Tmeas - (Time_Zone[1]-Time_Zone[0])))
        dImeas1 = np.gradient(Imeas, Tmeas)
        dImeas1[abs(dImeas1) < SetdITol] = 0
        tshift = Tmeas[np.nonzero(dImeas1)[0][0]]
        dImeas = np.gradient(SimData[1, 1:], SimData[0, 1:])
        dImeas[abs(dImeas) < SetdITol] = 0
        tshift_Sim = SimData[0, 1:][np.nonzero(dImeas)[0][0]]
        tshift = tshift - tshift_Sim
        idx_low = np.argmin(abs(Tmeas - tshift - Time_Zone[0]))
    else:
        idx_low = 0
        idx_up = -1

    #Start Evaluation
    SimData[0, 1:] = SimData[0, 1:] - Time_Zone[0]
    MSESims = np.ones((SimData.shape[0] - 1, 2)) * 9999
    LDSims = np.ones((SimData.shape[0] - 1, 2)) * 9999
    FImeas = interp1d(Tmeas[idx_low:idx_up]+abs(Tmeas[idx_low]), Imeas[idx_low:idx_up], kind='cubic')
    Tmeas2 = SimData[0, 1:]
    try:
        Imeas2 = FImeas(Tmeas2)
    except:
        try:
            Tmeas2[Tmeas2 > Tmeas[idx_low]+abs(Tmeas[idx_low])+ 1E-8] = Tmeas2[Tmeas2 > Tmeas[idx_low]+abs(Tmeas[idx_low])+ 1E-8]- 1E-8
            Imeas2 = FImeas(Tmeas2[1:-9])
            Imeas2 = np.append(np.append(np.array([Imeas2[0]]), Imeas2), np.array([Imeas2[-1]]*9))
        except:
            print("Interpolating Data was not sucessful.")
            print("Start-Point of Tmeas", (Tmeas[idx_low]+abs(Tmeas[idx_low])), ", Start-Point of Tsim:", SimData[0, 1])
            print("End-Point of Tmeas", (Tmeas[idx_up] + abs(Tmeas[idx_low])), ", End-Point of Tsim:", (SimData[0, -1]))
            return

    SweepMatrix = SweepObject.SweepMatrix
    #Calculate MSE
    for i in range(1, SimData.shape[0]):
        MSESims[i-1, 0] = SimData[i, 0]-SimData[1, 0]
        MSESims[i-1, 1] = (np.square(SimData[i, 1:] - Imeas2[:])).mean(axis=0)
    # Calculate largest Deviation
    for i in range(1, SimData.shape[0]):
         LDSims[i - 1, 0] = SimData[i, 0]-SimData[1, 0]
         LDSims[i - 1, 1] = np.amax(abs(SimData[i, 1:].astype(float) - Imeas2[:]))

    print("Best Fit for Meas-StartIDX: ", idx_low)
    BestFit = np.argsort(MSESims[:, 1])
    print("Best fitting simulations for MSE: ")
    print(MSESims[BestFit[:showBestFit], 0])
    print(MSESims[BestFit[:showBestFit], 1])
    BestFit = np.argsort(LDSims[:, 1])
    print("Best fitting simulations based on smallest, largest Deviation: ")
    print(LDSims[BestFit[:showBestFit], 0])
    print(LDSims[BestFit[:showBestFit], 1])

    SweepMatrix = SweepObject.SweepMatrix
    ParametersToSweep = SweepObject.ParametersToSweep

    #Parameter Importance Study -- Ablation Analysis
    # 1. Extract best 10% of the Simulations
    NumberBest = int(np.floor(SimData.shape[0]/1))
    if SimData.shape[0]<10: NumberBest = SimData.shape[0]-3
    BestFit = np.argsort(MSESims[:, 1])[0:NumberBest]
    SweepedParameters = SweepMatrix.shape[1]
    AbMatrix = np.zeros((SweepedParameters, NumberBest))
    MaxVar = np.zeros((SweepedParameters,))
    Var = np.zeros((SweepedParameters,))
    for i in range(SweepedParameters):
        for j in range(len(BestFit)):
            AbMatrix[i, j] = SweepMatrix[BestFit[j],i]
        MaxVar[i] = np.var(SweepMatrix[:, i])
        Var[i] = np.var(AbMatrix[i, :])/MaxVar[i]

    print("Ordered Importance of Parameters: ")
    Order = np.argsort(Var)
    for i in range(SweepedParameters):
        print(ParametersToSweep[Order[i]]+", ", end = '')
    print("\n Corresponding Variances: ")
    for i in range(SweepedParameters):
        print(Var[Order[i]])
    print("\n")

    #Make fancy plot
    if Plots:
        ##Plot1
        fig = plt.figure()
        ax = fig.add_subplot(111)
        opacity = 0.5
        dec = 0.4/NumberBest
        colors = cm.spring
        TotLength = int(len(SimData[0,:])/2)
        LengthStep = int(TotLength/len(BestFit))
        ax.plot(SimData[0, 1:].astype(float), SimData[BestFit[0]+1, 1:].astype(float), color=colors(2*opacity),
                alpha=opacity, label='_nolegend_')
        # ax.text(SimData[0, TotLength].astype(float),SimData[BestFit[0]+1, TotLength].astype(float), str(0), alpha = opacity)
        for i in range(1,len(BestFit)):
            opacity = (opacity - dec)
            ax.plot(SimData[0, 1:].astype(float), SimData[BestFit[i]+1, 1:].astype(float), color=colors(2*opacity),
                    alpha=opacity, label='_nolegend_')
            # ax.text(SimData[0, TotLength+i*LengthStep].astype(float), SimData[BestFit[i]+1, TotLength+i*LengthStep].astype(float), str(i),
            #         alpha=opacity)
        sm = plt.cm.ScalarMappable(cmap=colors)
        cbar = plt.colorbar(sm)
        cbar.set_ticks([1])
        cbar.set_ticklabels(["Best Fit"])
        meas = ax.plot(Tmeas2, Imeas2, color='black', label='Measurement')
        ax.set_xlabel('t [s]', fontsize =20)
        ax.set_ylabel('I [A]', fontsize =20)
        ax.legend(fontsize =20)
        ax.grid(True)

        flag_No3Dplots = 0
        try:
            #Plot two most important parameters together on MSE
            Vals1 = SweepObject.ParameterMatrix[Order[0], :][SweepObject.ParameterMatrix[Order[0], :] != 0]
            Vals2 = SweepObject.ParameterMatrix[Order[1], :][SweepObject.ParameterMatrix[Order[1], :] != 0]
            Vals3 = SweepObject.ParameterMatrix[Order[2], :][SweepObject.ParameterMatrix[Order[2], :] != 0]
        except:
            print("No 3D Data Found. Following Plots are not plottable.")
            flag_No3Dplots = 1
        InitVals = SweepMatrix[0, :]
        D1 = np.zeros((Vals1.shape[0]))
        try:
            D2 = np.zeros((Vals2.shape[0]))
            D3 = np.zeros((Vals3.shape[0]))
        except:
            pass
        for i in range(Vals1.shape[0]):
            for j in range(SweepMatrix.shape[0]):
                if SweepMatrix[j, Order[0]] == Vals1[i]:
                    Cp = np.delete(SweepMatrix[j, :], Order[0])
                    Cp2 = np.delete(InitVals[:], Order[0])
                    if np.allclose(Cp, Cp2):
                        Idx = MSESims[:, 0]
                        Idx = Idx[Idx == j]
                        D1[i] = int(Idx[0])
        try:
            for i in range(Vals2.shape[0]):
                for j in range(SweepMatrix.shape[0]):
                    if SweepMatrix[j, Order[1]] == Vals2[i]:
                        Cp = np.delete(SweepMatrix[j, :], Order[1])
                        Cp2 = np.delete(InitVals[:], Order[1])
                        if np.allclose(Cp, Cp2):
                            Idx = MSESims[:, 0]
                            Idx = Idx[Idx == j]
                            D2[i] = int(Idx[0])
            for i in range(Vals3.shape[0]):
                for j in range(SweepMatrix.shape[0]):
                    if SweepMatrix[j, Order[2]] == Vals3[i]:
                        Cp = np.delete(SweepMatrix[j, :], Order[2])
                        Cp2 = np.delete(InitVals[:], Order[2])
                        if np.allclose(Cp, Cp2):
                            Idx = MSESims[:, 0]
                            Idx = Idx[Idx == j]
                            D3[i] = int(Idx[0])
        except:
            pass

        x = SweepMatrix[D1.astype(int), Order[0]]
        try:
            y = SweepMatrix[D2.astype(int), Order[1]]
            k = SweepMatrix[D3.astype(int), Order[2]]
        except:
            pass

        if flag_No3Dplots==1: return
        ##Plot 2
        verts = []
        zs = [1.0, 2.0, 3.0]
        xs = (np.concatenate([[x[0]], x[:], [x[-1]]])-x[0])/(x[-1]-x[0])
        xb = SweepMatrix[BestFit[0]+1,0]
        ys = (np.concatenate([[y[0]], y[:], [y[-1]]])-y[0])/(y[-1]-y[0])
        yb = SweepMatrix[BestFit[0]+1,1]
        ks = (np.concatenate([[k[0]], k[:], [k[-1]]])-k[0])/(k[-1]-k[0])
        kb = SweepMatrix[BestFit[0]+1,2]
        xMS = np.concatenate([[0], 1/MSESims[D1.astype(int), 1], [0]])
        yMS = np.concatenate([[0], 1/MSESims[D2.astype(int), 1], [0]])
        kMS = np.concatenate([[0], 1/MSESims[D3.astype(int), 1], [0]])
        verts.append(list(zip(xs, xMS)))
        verts.append(list(zip(ys, yMS)))
        verts.append(list(zip(ks, kMS)))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        poly = PolyCollection(verts, facecolors=['r', 'g', 'y'])
        poly.set_alpha(0.7)
        zs = [1.0, 2.0, 3.0]
        ax.add_collection3d(poly, zs=zs, zdir='y')
        ax.set_xlabel('Values [0=Min, 1=Max Value]', fontsize =14, labelpad=10)
        ax.set_xlim3d(0, 1)
        ax.set_ylabel('Parameters', fontsize = 14,labelpad=20)
        ax.set_ylim3d(0, 4)
        ax.set_zlabel('Inverse MSE', fontsize = 14,labelpad=10)
        ax.set_zlim3d(0, 1/MSESims[BestFit[0], 1])
        plt.yticks(zs, ParametersToSweep, fontsize =14)
        plt.plot([xb/np.max(SweepMatrix[:,0])],[1.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4, alpha=0.6, label="Best fit")
        plt.plot([yb/np.max(SweepMatrix[:,1])], [2.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4,
                 alpha=0.6)
        plt.plot([kb/np.max(SweepMatrix[:,2])], [3.], 1/MSESims[BestFit[0], 1], markerfacecolor='k', markeredgecolor='k', marker='o', markersize=4,
                 alpha=0.6)
        plt.plot([xb/np.max(SweepMatrix[:,0]),yb/np.max(SweepMatrix[:,1]),kb/np.max(SweepMatrix[:,2])],[1.,2.,3.],[1/MSESims[BestFit[0], 1],
                                            1/MSESims[BestFit[0], 1],1/MSESims[BestFit[0], 1]],'--',color='black')
        plt.plot([xb / np.max(SweepMatrix[:, 0]),xb / np.max(SweepMatrix[:, 0])], [1.,1.], [0.,1/MSESims[BestFit[0], 1]],'--',color='r')
        plt.plot([yb / np.max(SweepMatrix[:, 1]),yb / np.max(SweepMatrix[:, 1])], [2.,2.], [0.,1/MSESims[BestFit[0], 1]],'--',color='g')
        plt.plot([kb / np.max(SweepMatrix[:, 2]),kb / np.max(SweepMatrix[:, 2])], [3.,3.], [0.,1/MSESims[BestFit[0], 1]],'--',color='y')
        plt.legend(fontsize =14)
        plt.show()

        ##Plot 3
        LastSim = SweepMatrix.shape[0]-D2.shape[0]*Order[1]-1
        D = np.ceil(np.linspace(0, LastSim, D1.shape[0]*D2.shape[0]))
        D_mesh = D.reshape(D1.shape[0], D2.shape[0])
        X, Y = np.meshgrid(x, y)
        Z = 1./MSESims[D_mesh.astype(int), 1]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, np.transpose(Z), color='white', edgecolors='grey', alpha=0.5)
        ax.scatter(X.flatten(), Y.flatten(), np.transpose(Z).flatten(), c='red')
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel('Inverse MSE', fontsize =16)
        plt.show()

        # # Plot4
        RData = np.max(RData, axis=1)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, RData[D_mesh.astype(int)], color='white', edgecolors='grey', alpha=0.5)
        ax.scatter(X.flatten(), Y.flatten(), RData[D_mesh.astype(int)].flatten(), c='red')
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel('R_CoilSections', fontsize =16)
        plt.show()

        ##Plot 5
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(SweepMatrix[BestFit, Order[0]], SweepMatrix[BestFit, Order[1]], SweepMatrix[BestFit, Order[2]],
                    c='red', marker='^', label = 'Low Error')
        ax.scatter(np.delete(SweepMatrix[:, Order[0]], BestFit),
                   np.delete(SweepMatrix[:, Order[1]], BestFit),
                   np.delete(SweepMatrix[:, Order[2]], BestFit),
                   c='blue', marker='o', label='High error')
        ax.legend(fontsize =11)
        ax.set_xlabel(ParametersToSweep[Order[0]], fontsize =11)
        ax.set_ylabel(ParametersToSweep[Order[1]], fontsize =11)
        ax.set_zlabel(ParametersToSweep[Order[2]], fontsize =11)
        plt.show()