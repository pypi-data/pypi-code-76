__version__ = '2019-08-08 12:00AM'

### data statistics ############################################
import numpy as np
import pandas as pd

def Data_Stat(df, n_row_view = 3):
    types = pd.Series({c:str(df[c].dtype) for c in df.columns}) # variable type
    total = df.isnull().sum() # the number of null values
    percent = 100 * total / df.isnull().count() # the percentage of null values
    n_unique = df.nunique() # the number of unique values
    
    tt = np.transpose(pd.concat([types, total, percent, n_unique], axis=1, keys=['Types', '# of nulls', '% of nulls', '# of uniques']))
    return pd.concat([df.head(n_row_view), tt], axis = 0)

### Evaludate Model Scores ###################################
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error

def Eval_Model_Scores(model, data, features, target, P_THRESHOLD = 0.5):
    num_cases = data.shape[0]; print('Total number of observations = %s'%num_cases)
    if ('Classifier' in str(model)) or ('LogisticRegression' in str(model)) or ('SVC' in str(model)):
        y_pred_prob = model.predict_proba(data[features])[:,1]
        y_pred = y_pred_prob >= P_THRESHOLD
        
        accuracy = accuracy_score(data[target], y_pred); print('Accuracy = %s'%accuracy)
        precision = precision_score(data[target], y_pred); print('Precision = %s'%precision)
        recall = recall_score(data[target], y_pred); print('Recall = %s'%recall)
        f1score = f1_score(data[target], y_pred); print('F1_Score = %s'%f1score)
        auc = roc_auc_score(data[target], y_pred_prob); print('AUC = %s'%auc)

        df_confusion = pd.crosstab(data[target].values.ravel(), y_pred, rownames=['Actual'], colnames=['Predicted']) # , margins=True)
        
        scores = (accuracy, precision, recall, f1score, auc, df_confusion, y_pred_prob)
    if 'Regressor' in str(model):
        y_pred = model.predict(data[features])

        mse = mean_squared_error(data[target], y_pred); print('MSE = %s'%mse)
        rmse = np.sqrt(mse); print('RMSE = %s'%rmse)

        scores = (mse, rmse, y_pred)
        
    return scores

### plot decision boundary for dataset with two feature variables #################
import matplotlib.pyplot as plt
import seaborn as sns

def Plot_2D_Decision_Bourndary(model, train, test, features, target):
    # update: 07/21/2019
    # ref) https://stackoverflow.com/questions/22294241/plotting-a-decision-boundary-separating-2-classes-using-matplotlibs-pyplot
    ft1 = features[0]; ft2 = features[1]

    # X, Y, Z for contour plot
    x0 = np.linspace(train[ft1].min(),  train[ft1].max(), num=1000)
    y0 = np.linspace(train[ft2].min(),  train[ft2].max(), num=1000)
    X, Y = np.meshgrid(x0, y0)
    zz = model.predict(pd.DataFrame({ft1:X.ravel(), ft2:Y.ravel()})) # Predict the transformed test documents
    Z = np.reshape(zz, X.shape)

    # plot
    fig, ax = plt.subplots(ncols=2, sharey=True, figsize=(12, 6))
    sns.scatterplot(x=ft1, y=ft2, data=train, hue=target[0], ax=ax[0]) # plot train dataset
    ax[0].contour(X, Y, Z, colors = 'black') # contour plot
    ax[0].legend(loc='upper right')
    sns.scatterplot(x=ft1, y=ft2, data=test, hue=target[0], ax=ax[1]) # plot test dataset
    ax[1].contour(X, Y, Z, colors = 'black') # contour plot
    ax[1].legend(loc='upper right')
    plt.show()
    
### feature importance for feature selection ##############################
import pandas as pd

def Feature_Importance_xgboost(features, xgmodel):
    # https://towardsdatascience.com/be-careful-when-interpreting-your-features-importance-in-xgboost-6e16132588e7
    xgmodel.get_booster().get_score(importance_type='gain') 
    # xgmodel.feature_importances_
    fi = pd.DataFrame(list(zip(features, xgmodel.feature_importances_)), columns = ['feature','importance']) # https://datascience.stackexchange.com/questions/48330/how-to-get-xgbregressor-feature-importance-by-column-name
    fi_sort = fi.sort_values(by='importance', ascending = False).reset_index(drop=True)
    fi_sort['cumsum'] = fi_sort['importance'].cumsum()
    return fi_sort

### Plot Hyperopt Resuls: (Score vs. Parameters), (Params vs. Time) ###########################
from hyperopt import Trials
import matplotlib.pyplot as plt

def Plot_Hyperopt_Score_vs_Params(param_names, trials): #ref) https://www.districtdatalabs.com/parameter-tuning-with-hyperopt
    f, axes = plt.subplots(nrows=1, ncols=len(param_names), figsize=(15,5))
    cmap = plt.cm.jet
    for i, val in enumerate(param_names):
        xs = [t['misc']['vals'][val] for t in trials.trials]
        ys = [-t['result']['loss'] for t in trials.trials]
    #     xs, ys = zip(sorted(zip(xs, ys)))
        ys = np.array(ys)
        if len(param_names) > 1:
            axes[i].scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75, c=cmap(float(i)/len(param_names)))
            axes[i].set_xlabel(val, fontsize=12)
            axes[i].set_ylabel('cross validation accuracy', fontsize=12)
        else:
            axes.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75, c=cmap(float(i)/len(param_names)))
            axes.set_title(val)
            axes.set_xlabel(val, fontsize=12)
            axes.set_ylabel('cross validation accuracy', fontsize=12)

def Plot_Hyperopt_Params_vs_Time(param_names, trials):
    f, axes = plt.subplots(nrows=1, ncols=len(param_names), figsize=(15,5))
    cmap = plt.cm.jet
    for i, val in enumerate(param_names):
        xs = [t['tid'] for t in trials.trials]
        ys = [t['misc']['vals'][val] for t in trials.trials]
        if len(param_names) > 1:
            axes[i].set_xlim(xs[0]-10, xs[-1]+10)
            axes[i].scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75, c=cmap(float(i)/len(param_names)))
            axes[i].set_xlabel('$t$', fontsize=16)
            axes[i].set_ylabel(val, fontsize=16)  
        else:
            axes.set_xlim(xs[0]-10, xs[-1]+10)
            axes.scatter(xs, ys, s=20, linewidth=0.01, alpha=0.75, c=cmap(float(i)/len(param_names)))
            axes.set_xlabel('$t$', fontsize=16)
            axes.set_ylabel(val, fontsize=16)  

### Find the Pattern of Characters #################################################            
# update 2019-08-07
def Find_Characters_Pattern(string, DICT_CH_TO_PATTERN = {
    'a':'A', 'b':'A', 'c':'A', 'd':'A', 'e':'A', 'f':'A', 'g':'A', 'h':'A', 'i':'A', 'j':'A', 'k':'A', 'l':'A', 'm':'A', 
    'n':'A', 'o':'A', 'p':'A', 'q':'A', 'r':'A', 's':'A', 't':'A', 'u':'A', 'v':'A', 'w':'A', 'x':'A', 'y':'A', 'z':'A',
    '0':'D', '1':'D', '2':'D', '3':'D', '4':'D', '5':'D', '6':'D', '7':'D', '8':'D', '9':'D',
}):
    dkeys = DICT_CH_TO_PATTERN.keys()
    pt = ''.join([DICT_CH_TO_PATTERN[c] if c in dkeys else c for c in string.lower()])
    return ''.join([c for i, c in enumerate(pt) if (i==0) | ((i != 0) & (pt[i-1] != pt[i]))])
# Find_Characters_Pattern('234 AB - 4 ((77B))??//') # 'D A - D (DA)?/'            