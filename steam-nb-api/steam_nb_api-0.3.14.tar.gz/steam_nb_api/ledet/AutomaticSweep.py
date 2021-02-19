from steam_nb_api.ledet.ParameterSweep import *
from steam_nb_api.ledet.ParametersLEDET import ParametersLEDET
import pandas as pd
from steam_nb_api.ledet.Simulation import RunSimulations
from steam_nb_api.ledet.SimulationEvaluation import EvaluateSimulations
from copy import deepcopy
import pandas as pd
from tqdm import trange
from scipy.interpolate import interp1d
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import QuantileTransformer
from sklearn.compose import TransformedTargetRegressor
import matplotlib.pyplot as plt
import time
import csv
from sklearn.linear_model import RidgeCV

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, cross_val_predict, KFold
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline

class AutomaticSweep():
    def __init__(self, gridPoints, SetUpFile, LEDETFolder, LEDETExe, MagnetName, ExpDataFile):
        #const:
        self.Parameters = ParametersLEDET()
        self.Parameters.readLEDETExcel(SetUpFile)
        self.__PrepareXLSXForAutomatic()
        self.Sweeper = MinMaxSweep(self.Parameters, gridPoints)
        self.LEDETFolder = LEDETFolder
        self.LEDETInput = LEDETFolder + "\\LEDET\\" + MagnetName + "\\Input\\"
        self.LEDETOutput = "C:\\cernbox\\Validation_MO\\Validation\\LEDET\\FullB2\\"
        #self.LEDETOutput = LEDETFolder + "\\LEDET\\" + MagnetName + "\\Output\\Txt Files\\"
        self.LEDETExe = LEDETExe
        self.MagnetName = MagnetName

        #once changed:
        self.Expdata = self.__readExpData(ExpDataFile)
        self.gridPoints = gridPoints
        self.grid = np.array([])
        self.MSEGrid = np.array([])
        self.CovGrid = np.array([])
        self.max_x = np.array([])
        self.min_x = np.array([])
        self.xbar = np.array([])
        self.MLP = None

        #changeable:
        self.currentCount = 0
        self.MSEValues = np.array([])
        self.ParameterData = np.array([])

        self.TestData = np.array([])
        self.TestMSE = np.array([])

        self.bootStrapMLP = []

        self.StartIteration = 0
        self.EndIteration = 0

        self.XScaler = None

    def __readExpData(self, file):
        mat = pd.read_csv(file)
        Tmeas = np.array(mat.iloc[:, 0])
        try:
            Imeas = mat["IAB.I_A"].values
        except:
            try:
                Imeas = mat["STATUS.I_MEAS"].values
            except:
                print("Measured Data is unknown. Neither I_A nor I_MEAS")
        return np.vstack((Tmeas, Imeas))
    
    def __PrepareXLSXForAutomatic(self):
        self.Parameters.setAttribute("Options", "flag_saveMatFile", 0)
        self.Parameters.setAttribute("Options", "flag_saveTxtFiles", 1)
        self.Parameters.setAttribute("Options", "flag_generateReport", 0)
        variableToSaveTxt = np.array(["time_vector", "R_CoilSections", "U_inductive_dynamic_CoilSections", "I_CoilSections"])
        typeVariableToSaveTxt = np.array([1,1,1,1])
        self.Parameters.setAttribute("Variables", "variableToSaveTxt", variableToSaveTxt)
        self.Parameters.setAttribute("Variables", "typeVariableToSaveTxt", typeVariableToSaveTxt)

    def addParameterToSweep(self, Parameter, Min, Max):
        self.Sweeper.addParameterToSweep(Parameter, Min, Max, basePoints = 2)

    def __PrepareExpData(self, FirstSimDataValues, FirstSimDataTime):
        Time_Zone = np.array([FirstSimDataTime[0], FirstSimDataTime[-1]])
        Tmeas = self.Expdata[0,:]
        Imeas = self.Expdata[1,:]
        # Find Start-IDX
        idx_up = np.argmin(abs(Tmeas - (Time_Zone[1] - Time_Zone[0])))
        dImeas = np.gradient(Imeas, Tmeas)
        dImeas[abs(dImeas) < 200] = 0
        tshift = Tmeas[np.nonzero(dImeas)[0][0]]
        dImeas = np.gradient(FirstSimDataValues, FirstSimDataTime)
        dImeas[abs(dImeas) < 200] = 0
        tshift_Sim = FirstSimDataTime[np.nonzero(dImeas)[0][0]]
        tshift = tshift - tshift_Sim
        idx_low = np.argmin(abs(Tmeas - tshift - Time_Zone[0])) + 1
        FirstSimDataTime = FirstSimDataTime - Time_Zone[0]

        # Start Evaluation
        FImeas = interp1d(Tmeas[idx_low:idx_up] + abs(Tmeas[idx_low]), Imeas[idx_low:idx_up], kind='cubic')
        newExpData = FirstSimDataTime
        Imeas = FImeas(FirstSimDataTime)
        newExpData = np.vstack((newExpData, Imeas))
        self.Expdata = newExpData

    def __calcMSE(self, Simulation, PrepareData = False):
        ISim = np.array([])
        T = np.array([])
        items = os.listdir(self.LEDETOutput)
        for item in items:
            if item.endswith(str(Simulation)+'.txt') and 'VariableHistory' in item:
                if ".sys" not in item:
                     with open(self.LEDETOutput + item, 'r') as file:
                        k = file.readline().split(',')[:-1]
                        idxT = k.index('time_vector')
                        idxI = k.index(' I_CoilSections_1')
                        rows = [[float(x) for x in line.split(',')[:-1]] for line in file]
                        cols = [list(col) for col in zip(*rows)]
                        T = np.array(cols[idxT])
                        ISim = np.array(cols[idxI])
                     break

        if PrepareData:
            self.__PrepareExpData(ISim, T)
        MSE = (np.square(ISim - self.Expdata[1, :])).mean(axis=0)
        return MSE

    def __setMSEInGrid(self, ParamVec, Value):
        idx = np.argwhere(np.all((self.grid - ParamVec) == 0, axis=1))
        self.MSEGrid[idx] = Value
        self.MSEValues = np.append(self.MSEValues, Value)

    def __handleNewSimulation(self, ParamVec, Simulation):
        MSE = self.__calcMSE(Simulation)
        self.__setMSEInGrid(ParamVec, MSE)
        self.ParameterData = np.vstack((self.ParameterData, ParamVec))
        self.currentCount = self.currentCount +1

    def __SetGrid(self):
        CopyParameters = deepcopy(self.Sweeper.ParametersToSweep)
        CopyMatrix = deepcopy(self.Sweeper.ParameterMatrix)
        CopySweepMatrix = deepcopy(self.Sweeper.SweepMatrix)
        self.Sweeper.cleanParameterMatrix()
        for i in range(len(CopyParameters)):
            self.Sweeper.addParameterToSweep(CopyParameters[i], CopyMatrix[i,0], CopyMatrix[i,1], basePoints = self.gridPoints)
        self.Sweeper.generatePermutations()
        self.grid = self.Sweeper.SweepMatrix
        self.MSEGrid = np.ones((self.Sweeper.SweepMatrix.shape[0]))*-1.0

        # MSE = self.__calcMSE(0, PrepareData = True)
        # self.__setMSEInGrid(CopySweepMatrix[0,:], MSE)
        # self.currentCount = self.currentCount +1
        # for j in range(1, CopySweepMatrix.shape[0]):
        #     MSE = self.__calcMSE(self.currentCount)
        #     self.__setMSEInGrid(CopySweepMatrix[j, :], MSE)
        #     self.currentCount = self.currentCount + 1

    def __TrainNetwork(self, x_train, y_train, n_splits = 2, FastMode = False):
        #Standardize data to zero mean and variance 1
        start_time = time.time()
        scaler = StandardScaler().fit(x_train)
        X_train = scaler.transform(x_train)
        transformer = QuantileTransformer(output_distribution='normal', n_quantiles = int(x_train.shape[0]/4))
        Y_train = y_train.reshape(-1,1)
        if(y_train.shape[0] < 25):
            n_splits = 2

        # Create model and fit
        regressor = MLPRegressor(hidden_layer_sizes=(100,50), activation='relu', solver='lbfgs',
                                 learning_rate='adaptive', alpha=0.01, max_iter=1000, warm_start=False)
        regr = TransformedTargetRegressor(regressor=regressor, transformer = transformer)
        regr.fit(X_train, np.ravel(Y_train, order='C'))
        if FastMode:
            return regr

        # Nested CV to find conservative guess + find model parameters
        NestedTrials = 1
        p_grid = {"regressor__alpha": 10.0 ** -np.arange(3, 7), "regressor__hidden_layer_sizes": [(100,50), (50,25), (25,10)]}
        nested_scores = np.zeros(NestedTrials)

        for i in range(NestedTrials):
            inner_cv = KFold(n_splits=n_splits, shuffle=True, random_state=i)
            outer_cv = KFold(n_splits=n_splits, shuffle=True, random_state=i)

            clf = GridSearchCV(estimator=regr, param_grid=p_grid, cv=inner_cv)
            clf.fit(x_train, np.ravel(Y_train,order='C'))
            nested_score = cross_val_score(clf, X=X_train, y=np.ravel(Y_train, order='C'), cv=outer_cv)
            nested_scores[i] = nested_score.mean()
        end_time = time.time()
        print("Time needed to train:", np.round(end_time-start_time), "s")
        print("Actual error: ", nested_scores.mean())
        self.MLP = regr
        self.XScaler = scaler

    def __DeepTrainNetwork(self, x_train, y_train):
        # Standardize data to zero mean and variance 1
        start_time = time.time()
        scaler = StandardScaler().fit(x_train)
        X_train = scaler.transform(x_train)
        transformer = QuantileTransformer(output_distribution='normal', n_quantiles=int(x_train.shape[0] / 4))
        Y_train = y_train.reshape(-1, 1)
        if (y_train.shape[0] < 25):
            n_splits = 2

        # Create model and fit
        regressor = MLPRegressor(hidden_layer_sizes=(500, 250, 50), activation='relu', solver='lbfgs',
                                 learning_rate='adaptive', alpha=0.01, max_iter=1000, warm_start=False)
        regr = TransformedTargetRegressor(regressor=regressor, transformer=transformer)
        regr.fit(X_train, np.ravel(Y_train, order='C'))

        # Nested CV to find conservative guess + find model parameters
        NestedTrials = 1
        p_grid = {"regressor__alpha": 10.0 ** -np.arange(3, 7),
                  "regressor__hidden_layer_sizes": [(500, 250, 50), (800, 500, 100), (100, 500, 10)]}
        nested_scores = np.zeros(NestedTrials)

        n_splits = 4

        for i in range(NestedTrials):
            inner_cv = KFold(n_splits=n_splits, shuffle=True, random_state=i)
            outer_cv = KFold(n_splits=n_splits, shuffle=True, random_state=i)

            clf = GridSearchCV(estimator=regr, param_grid=p_grid, cv=inner_cv)
            clf.fit(x_train, np.ravel(Y_train, order='C'))
            nested_score = cross_val_score(clf, X=X_train, y=np.ravel(Y_train, order='C'), cv=outer_cv)
            nested_scores[i] = nested_score.mean()
        end_time = time.time()
        print("Time needed to train:", np.round(end_time - start_time), "s")
        print("Actual error: ", nested_scores.mean())
        self.MLP = regr
        self.XScaler = scaler

    def __calcCovariance(self, x1, x2):
        x1 = (x1-self.min_x) / (self.max_x-self.min_x)
        x2 = (x2-self.min_x) / (self.max_x-self.min_x)
        return np.sum((x1 - self.xbar) * (x2 - self.xbar)) / (len(x1) - 1)

    def __calcCovGrid(self):
        copyGrid = np.zeros(self.grid.shape)
        self.max_x = np.max(self.grid, axis=0)
        self.min_x = np.min(self.grid, axis=0)
        for i in range(self.grid.shape[0]):
            copyGrid[i] = (self.grid[i]-self.min_x) / (self.max_x-self.min_x)
        self.xbar = copyGrid.mean(axis=0)

        self.CovGrid = np.zeros((self.grid.shape[0], self.grid.shape[0]))
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[0]):
                self.CovGrid[i, j] = self.__calcCovariance(self.grid[i], self.grid[j])

    def __calcComplement(self):
        compGrid = deepcopy(self.grid)
        compCovGrid = deepcopy(self.CovGrid)
        idx = []
        for i in range(self.ParameterData.shape[0]):
            idx.append(np.argwhere(np.all((self.grid - self.ParameterData[i]) == 0, axis=1)))
        compGrid = np.delete(compGrid, idx, axis=0)
        compCovGrid = np.delete(compCovGrid, idx, axis=0)
        compCovGrid = np.delete(compCovGrid, idx, axis=1)
        return [compGrid, compCovGrid]

    def __setUpBootStrapMLP(self, Iterations = 6):
        self.bootStrapMLP = []
        factor = np.log10(self.max_x)
        for i in range(Iterations):
            newX = deepcopy(self.ParameterData)
            newY = deepcopy(self.MSEValues)
            for k in range(self.ParameterData.shape[0]):
                for j in range(self.ParameterData.shape[1]):
                    newX[k, j] = newX[k, j] + 10 ** (factor[j] - 2) * np.random.normal()
                newY[k] = newY[k] + 10 ** ((np.log10(np.max(self.MSEValues))) - 1.5) * np.random.normal()

            newMLP = self.__TrainNetwork(newX, newY, FastMode=True)
            self.bootStrapMLP.append(newMLP)

    def __bootstrapVariance(self, x, mu, Iterations = 6):
        start_time = time.time()
        confValues = np.zeros((Iterations,1))
        factor = np.log10(self.max_x)
        x = x.reshape(-1, x.shape[0])
        scaledX = self.XScaler.transform(x)
        for i in range(Iterations):
            newMLP = self.bootStrapMLP[i]
            confValues[i] = newMLP.predict(scaledX)
        confValues = sum((confValues-mu)**2)/len(confValues)
        end_time = time.time()
        #print("Time needed Bootstrap:", np.round(end_time - start_time), "s")
        return confValues

    def __calcCovVec(self, xn, L):
        N = L.shape[0]
        k = np.zeros((1, N))
        for i in range(N):
            k[0, i] = self.__calcCovariance(xn, L[i])
        return k

    def __calcModelCovMatrix(self):
        CovModel = np.zeros((self.ParameterData.shape[0], self.ParameterData.shape[0]))
        for i in range(self.ParameterData.shape[0]):
            for j in range(self.ParameterData.shape[0]):
                CovModel[i, j] = self.__calcCovariance(self.ParameterData[i], self.ParameterData[j])
        return CovModel

    def __NOSA(self):
        y_possible = []
        [compGrid, compCovGrid] = self.__calcComplement()
        CovModel = self.__calcModelCovMatrix()
        self.__setUpBootStrapMLP()
        for i in trange(compGrid.shape[0], file=sys.stdout, desc='NOSA'):
            try:
                mean_y = self.__Predict(compGrid[i].reshape(-1,compGrid.shape[1]))
                sigma_y = self.__bootstrapVariance(compGrid[i], mean_y)
                k_comp = self.__calcCovVec(compGrid[i], compGrid)
                k_new = self.__calcCovVec(compGrid[i], self.ParameterData)
                delta_y = np.asscalar((sigma_y - np.dot(np.dot(k_new, np.linalg.inv(CovModel)), k_new.T)) /
                                        (sigma_y - np.dot(np.dot(k_comp, np.linalg.inv(compCovGrid)), k_comp.T)))
                y_possible = np.r_[y_possible, delta_y]
            except np.linalg.LinAlgError as err:
                print('Caught Error in NOSPA, break')
                if 'Singular matrix' in str(err):
                    print('Error occured, Singularmatrix')
                elif 'not positive definite, even with jitter.' in str(err):
                    print('Error occured, Not positive definite')
                else:
                    raise
        if len(y_possible)==0:
            i = np.random.random_integers(0,compGrid.shape[0])
            A = compGrid[np.argmax(i)]
        else:
            A = compGrid[np.argmax(y_possible)]
        return A

    def __SetUpNewSimulation(self, Params, ParamVec):
        file_name = self.LEDETInput + self.MagnetName + "_" + str(self.currentCount) + ".xlsx"
        for j in range(len(Params)):
            SetClass = self.Sweeper._checkSetClass(Params[j])
            setValue = self.Sweeper._generateImitate(self.Sweeper.ParametersLEDET.getAttribute(
                getattr(self.Sweeper.ParametersLEDET, SetClass), Params[j]),ParamVec[j])
            self.Sweeper.ParametersLEDET.setAttribute(
                getattr(self.Sweeper.ParametersLEDET, SetClass), Params[j],setValue)
            if (Params[j] == "overwrite_f_internalVoids_inGroup"):
                exValue = self.Sweeper.VoidRatio - ParamVec[j]
                setVal = self.Sweeper._generateImitate(
                    self.Sweeper.ParametersLEDET.getAttribute(getattr(self.Sweeper.ParametersLEDET, "Inputs"),
                                                      "overwrite_f_externalVoids_inGroup"), exValue)
                self.Sweeper.ParametersLEDET.setAttribute(getattr(self.Sweeper.ParametersLEDET, "Inputs"),
                                                  "overwrite_f_externalVoids_inGroup", setVal)
        self.Sweeper.ParametersLEDET.writeFileLEDET(file_name)

    def __findGlobalMinimum(self):
        write = []

        MinVec = np.array([])
        MinMSE = 0
        for i in trange(self.grid.shape[0], file=sys.stdout, desc='Final Eval:'):
            mean_y = self.__Predict(self.grid[i].reshape(-1, self.grid.shape[1]))
            if i==0:
                MinMSE = mean_y
                MinVec = self.grid[i]
            if abs(MinMSE) >= abs(mean_y):
                MinVec = self.grid[i]
                MinMSE = mean_y

            write.append([i, mean_y])

        f = open('C:\cernbox\AutoAnalysis\AutoWrite.csv', 'w')
        with f:
            writer = csv.writer(f)
            for row in write:
                writer.writerow(row)
        return [MinVec, MinMSE]

    def __Predict(self, x_test):
        X_test = x_test#self.XScaler.transform(x_test)
        y = self.MLP.predict(X_test)
        return y

    def AutomaticRun(self, NOSA):
        self.PREPARETEST()
        print("** Start Automatic Run **")
        print("o Set Up Starting Simulations")
        # 1. Produce training data to start on
        # 1a. Setup Sweeper + Run Simulations
        self.Sweeper.generatePermutations()
        self.ParameterData = self.Sweeper.SweepMatrix
        self.Sweeper.prepareSimulation(self.MagnetName, self.LEDETInput)
        # RunSimulations(self.LEDETFolder, self.LEDETExe, self.MagnetName, RunSimulations= False)
        # 1b. Set Up grid for Automatic Sweep
        self.__SetGrid()
        #2. fit model onto data
        print("o Integrate Training Data and Create Model")
        self.__TrainNetwork(self.ParameterData, self.MSEValues)
        self.__calcCovGrid()
        print("x First Training Data produced and integrated.")
        print("o Start ML Pipeline")
        # 3. Find next Data point --> HERE MUST COME SOME CRITERIA TO BREAK
        for i in range(NOSA):
            self.StartIteration = time.time()
            print("- Iteration:", i)
            newX = self.__NOSA()
            print("Next Data-Point to check:", newX)
            #3c. Set up next data point and run
            self.__SetUpNewSimulation(self.Sweeper.ParametersToSweep, newX)
            # RunSimulations(self.LEDETFolder, self.LEDETExe, self.MagnetName, Simulations = [self.currentCount],
                           # RunSimulations=False)

            self.runDummySimulation(newX)
            #self.__handleNewSimulation(newX, self.currentCount)

            self.__TrainNetwork(self.ParameterData, self.MSEValues)
            self.EndIteration = time.time()
            if i%10 == 0:
                [MinVec, MinMSE] = self.__findGlobalMinimum()
                print("Break-Point Evaluation:")
                print("Best Data-Point Found:")
                print(self.Sweeper.ParametersToSweep)
                print(MinVec)
                print("MSE:", MinMSE)

            print("Time needed for Iteration: ", self.EndIteration - self.StartIteration)
        print("x Pipeline finished")
        print("o Prepare all data and tune")
        self.__DeepTrainNetwork(self.ParameterData, self.MSEValues)
        [MinVec, MinMSE] = self.__findGlobalMinimum()
        print("Final Evaluation:")
        print("Best Data-Point Found:")
        print(self.Sweeper.ParametersToSweep)
        print(MinVec)
        print("MSE:", MinMSE)



    def PREPARETEST(self):
        f = open('C:\cernbox\AutoAnalysis\TestData.csv', 'r')
        count = 0
        with f:
            writer = csv.reader(f, delimiter=',')
            for row in writer:
                if len(row) != 0:
                    r = np.array([float(row[1]), float(row[2]), float(row[3])])
                    mse = float(row[4])
                    if count == 0:
                        self.TestData = r
                        count = 1
                    else:
                        self.TestData = np.vstack((self.TestData, r))
                    self.TestMSE = np.append(self.TestMSE, mse)

    def runDummySimulation(self, ParamVec):
        idx = np.argwhere(np.all((self.grid - ParamVec) == 0, axis=1))
        MSE = self.TestMSE[idx]
        self.__setMSEInGrid(ParamVec, MSE)
        self.ParameterData = np.vstack((self.ParameterData, ParamVec))
        self.currentCount = self.currentCount + 1

    def __NewTrain(self, x_train, y_train):

        transformer = QuantileTransformer(output_distribution='normal',
                                          n_quantiles=int(x_train.shape[0]/4))
        y_train = y_train.reshape(-1, 1)

        pipeline = Pipeline([('scl', StandardScaler()),
                               ('clf', MLPRegressor(activation='tanh', solver='lbfgs', max_iter = 1500))])
        parameters = {'regressor__clf__alpha': [0.01, 0.001, 0.0001, 0.1, 1, 10],
                      "regressor__clf__hidden_layer_sizes": [(50,), (25,), (10,), (8,)]
                      }
        regr = TransformedTargetRegressor(regressor=pipeline, transformer=transformer)
        grid_obj = GridSearchCV(estimator=regr, param_grid=parameters, cv=3,
                                scoring='r2', verbose=False, n_jobs=1, refit=True)
        grid_obj.fit(x_train, y_train)
        estimator = grid_obj.best_estimator_
        print(grid_obj.best_score_)
        print(grid_obj.best_params_)

        shuffle = KFold(n_splits=5, shuffle=True, random_state=0)

        X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.33, random_state=0)

        cv_scores = cross_val_score(estimator, X_test, y_test.ravel(), cv=shuffle, scoring='r2')
        y_pred = cross_val_predict(estimator, X_test, y_test, cv=shuffle)

        self.MLP = estimator

    def NestedCVAll(self):

        def model(pipeline, parameters, X_train, y_train, X, y, name):

            grid_obj = GridSearchCV(estimator=pipeline,
                                    param_grid=parameters,
                                    cv=3,
                                    scoring='r2',
                                    verbose=False,
                                    n_jobs=1,
                                    refit=True)
            grid_obj.fit(X_train, y_train)
            results = pd.DataFrame(pd.DataFrame(grid_obj.cv_results_))
            results_sorted = results.sort_values(by=['mean_test_score'], ascending=False)

            print("##### Results")
            print(results_sorted)

            print("best_index", grid_obj.best_index_)
            print("best_score", grid_obj.best_score_)
            print("best_params", grid_obj.best_params_)
            estimator = grid_obj.best_estimator_

            shuffle = KFold(n_splits=5,
                            shuffle=True,
                            random_state=0)
            cv_scores = cross_val_score(estimator,
                                        X,
                                        y.ravel(),
                                        cv=shuffle,
                                        scoring='r2')
            print("##### CV Results")
            print("mean_score", cv_scores.mean())

            y_pred = cross_val_predict(estimator, X, y, cv=shuffle)

            plt.scatter(y, y_pred, label=name)
            xmin, xmax = plt.xlim()
            ymin, ymax = plt.ylim()
            plt.plot([0, xmax], [ymin, ymax], lw=1, alpha=0.4, label=name)
            plt.xlabel("True MSE")
            plt.ylabel("Predicted MSE")
            plt.annotate(' R-squared CV = {}'.format(round(float(cv_scores.mean()), 3)), size=9,
                         xy=(xmin, ymax), xytext=(10, -15), textcoords='offset points')
            plt.title('Predicted MSE vs Real MSE')
            plt.legend()
            plt.show()

        # Pipeline and Parameters - Linear Regression

        pipe_ols = Pipeline([('scl', StandardScaler()),
                             ('clf', LinearRegression())])
        param_ols = {}

        # Pipeline and Parameters - KNN
        pipe_knn = Pipeline([('clf', KNeighborsRegressor())])
        param_knn = {'clf__n_neighbors': [5, 10, 15, 25, 30]}

        # Pipeline and Parameters - Lasso
        pipe_lasso = Pipeline([('scl', StandardScaler()),
                               ('clf', Lasso(max_iter=1500))])
        param_lasso = {'clf__alpha': [0.01, 0.1, 1, 10]}

        # Pipeline and Parameters - Ridge
        pipe_ridge = Pipeline([('scl', StandardScaler()),
                               ('clf', Ridge())])
        param_ridge = {'clf__alpha': [0.01, 0.1, 1, 10]}

        # Pipeline and Parameters - Polynomial Regression
        pipe_poly = Pipeline([('scl', StandardScaler()),
                              ('polynomial', PolynomialFeatures()),
                              ('clf', LinearRegression())])
        param_poly = {'polynomial__degree': [2, 4, 6]}

        # Pipeline and Parameters - Decision Tree Regression
        pipe_tree = Pipeline([('clf', DecisionTreeRegressor())])
        param_tree = {'clf__max_depth': [2, 5, 10],
                      'clf__min_samples_leaf': [5, 10, 50, 100]}

        # Pipeline and Parameters - Random Forest
        pipe_forest = Pipeline([('clf', RandomForestRegressor())])
        param_forest = {'clf__n_estimators': [10, 20, 50],
                        'clf__max_features': [None, 1, 2],
                        'clf__max_depth': [1, 2, 5]}

        # Pipeline and Parameters - MLP Regression
        pipe_neural = Pipeline([('scl', StandardScaler()),
                                ('clf', MLPRegressor())])
        param_neural = {'clf__alpha': [0.001, 0.01, 0.1, 1, 10, 100],
                        'clf__hidden_layer_sizes': [(5), (10, 10), (7, 7, 7)],
                        'clf__solver': ['lbfgs'],
                        'clf__activation': ['relu', 'tanh'],
                        'clf__learning_rate': ['constant', 'invscaling']}

        # Execute preprocessing & train/test split
        X = self.ParameterData
        y = self.MSEValues
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

        # Execute model hyperparameter tuning and crossvalidation
        print("OLS")
        model(pipe_ols, param_ols, X_train, y_train, X, y, "OLS")
        print("Knn")
        model(pipe_knn, param_knn, X_train, y_train, X, y,"KNN")
        print(Lasso)
        model(pipe_lasso, param_lasso, X_train, y_train, X, y, "Lasso")
        print("Ridge")
        model(pipe_ridge, param_ridge, X_train, y_train, X, y, "Ridge")
        print("poly")
        model(pipe_poly, param_poly, X_train, y_train, X, y, "Poly")
        print("Tree")
        model(pipe_tree, param_tree, X_train, y_train, X, y, "Decision Tree")
        print("Forest")
        model(pipe_forest, param_forest, X_train, y_train, X, y, "RF")
        print("Neural")
        model(pipe_neural, param_neural, X_train, y_train, X, y, "NN")


    def LearnAndTrainAll(self):
        self.PREPARETEST()
        self.Sweeper.generatePermutations()
        self.__SetGrid()


        self.ParameterData = self.TestData
        self.MSEValues = self.TestMSE

        self.__NewTrain(self.ParameterData, self.MSEValues)
        # self.NestedCVAll()

        [MinVec, MinMSE] = self.__findGlobalMinimum()
        print("Final Evaluation:")
        print("Best Data-Point Found:")
        print(self.Sweeper.ParametersToSweep)
        print(MinVec)
        print("MSE:", MinMSE)
