#!/usr/bin/env python
# coding: utf-8

# In[1]:


__version__ = '2019-07-27-beta'
__DEBUG_MODE__ = False


# In[2]:


# Copyright © 2018-2019 Bomsoo Brad Kim, All Rights Reserved.
# Last Update : 04/14/2019
import numpy as np
import pandas as pd

def xgrid_search(xgrid_search_target_function, params, 
                 MIN_MAX = 'min', SCORE_TOLERANCE = 1e-5,  MAX_GRID_LEVEL = 20, MAX_INNER_ROUND = 50, 
                 initialize_cross_grid = False):
    def generate_cgrid(ikeys): # make cross grids
        iparams2 = {k: [0,-1,1] for k in ikeys}
        cgrid = pd.DataFrame(columns = ikeys) # initialize cgrid with empty elements
        for k,i in iparams2.items():
            cgrid = pd.concat([cgrid, pd.DataFrame({k:i})], sort = False) # make cross grids
        cgrid.fillna(0, inplace = True)
        cgrid.drop_duplicates(keep = 'first', inplace = True)
        cgrid.reset_index(drop = True, inplace = True)
        return cgrid

    def trim_grid(grid, ikeys, min_grid, max_grid): # remove duplicate and out-of-range grid points
        i0 = grid[ikeys].duplicated(keep = 'first') # find out which are duplicate elements except the first elements
        i1 = (grid[ikeys] < min_grid[ikeys]).any(axis = 1) # find out rows with less than min indexes
        i2 = (grid[ikeys] > max_grid[ikeys]).any(axis = 1) # find out rows with greater than max indexes
        # grid = pd.concat([grid, i0, i1, i2], sort = False, ignore_index = True, axis = 1)
        grid = grid.loc[~(i0 | i1 | i2)] # remove duplicate and out-of-range grid points
        grid.reset_index(drop = True, inplace = True)
        return grid

    def fill_keys(params2, grid):
        for (k,i) in params2.items(): grid[k] = grid['i_'+k].map({i:value for i, value in enumerate(params2[k])}) # update index
        return grid

    def update_divide_intervals(partype, params2, grid):
        def divide_intervals(a, paramter_type = 'uni'):
            a = np.array(a)
            if paramter_type == 'uni': aa = np.sort(np.unique(np.append(a, (a[1:] + a[:-1])/2)))
            elif paramter_type == 'log': aa = np.sort(np.unique(np.append(a, np.sqrt(a[1:]*a[:-1]))))
            elif paramter_type == 'int': aa = np.sort(np.unique(np.around(np.append(a, (a[1:] + a[:-1])/2)).astype(int)))
            return aa
        for (k,i) in params2.items():
            params2[k] = divide_intervals(i, partype[k]) # divide intervals
            grid['i_'+k] = grid[k].map({value:i for i, value in enumerate(params2[k])}) # update index
        return params2, grid
    
    
    # initial preparation
    partype = {k:i[0] for (k,i) in params.items()} # pick up data type
    params2 = {k:np.sort(np.unique(i[1])) for (k,i) in params.items()} # pick up range
    iparams = {'i_'+k:range(len(i)) for (k,i) in params2.items()} # index for parameters
    pkeys = list(params2.keys())
    ikeys = list(iparams.keys()) # parameter key names
    cgrid = generate_cgrid(ikeys) # cross grid
    
    # initialize grid
    grid = pd.DataFrame(index = pd.MultiIndex.from_product(iparams.values(), names = iparams.keys())).reset_index() # https://stackoverflow.com/questions/13269890/cartesian-product-in-pandas
    grid['func_value'] = np.nan
    grid = fill_keys(params2, grid)
    
    # cross grid setting in the first place
    if initialize_cross_grid:
        params2, grid = update_divide_intervals(partype, params2, grid)
        grid = grid[ikeys].mean(axis = 0).astype(int) + cgrid
        grid[ikeys].astype(int)
        grid['func_value'] = np.nan
        grid = fill_keys(params2, grid)

    # search for the best
    best_fval = pd.DataFrame()
    len_prev_grid = 0
    for nn in range(MAX_GRID_LEVEL):
        for kk in range(MAX_INNER_ROUND):
            # evaluate function
            for i in range(len(grid)):
                if np.isnan(grid.loc[i,'func_value']): # if func_value = nan, then evaluate
                    grid.loc[i,'func_value'] = xgrid_search_target_function(**grid.astype(object).loc[i, pkeys].to_dict())
                    print('> i=%s (level=%s, group=%s); '%(i+1,nn+1,kk+1), grid.astype(object).loc[i, pkeys+['func_value']].to_dict())
            # find best score
            if MIN_MAX == 'max': idx = grid['func_value'].idxmax()
            elif MIN_MAX == 'min': idx = grid['func_value'].idxmin()
            best_grid = grid.loc[idx, ikeys].astype('int') # ensure that the index is integer
            print('  best so far =', grid.astype(object).loc[idx, pkeys+['func_value']].to_dict())
            # explore new grid points
            min_grid = grid.min(axis = 0) # order matters!
            max_grid = grid.max(axis = 0) # order matters!
            grid = pd.concat([grid, best_grid + cgrid], sort = False, ignore_index = True) # attach new rows
            grid = trim_grid(grid, ikeys, min_grid, max_grid) # remove duplicate and out-of-range rows
            grid = fill_keys(params2, grid)
            # stop if there is no NAN value
            if ~grid['func_value'].isna().any(): break

        # stop condition
        if len_prev_grid == len(grid):
            break
        else:
            if MIN_MAX == 'max': 
                idx = grid.loc[len_prev_grid:, 'func_value'].idxmax() # find the best at the latest level
                best_fval = best_fval.append(grid.loc[idx, pkeys+['func_value']]) # save the best row
                best_fval.sort_values(by = 'func_value', ascending  = False, inplace = True)
            elif MIN_MAX == 'min': 
                idx = grid.loc[len_prev_grid:, 'func_value'].idxmin() # find the best at the latest level
                best_fval = best_fval.append(grid.loc[idx, pkeys+['func_value']]) # save the best row
                best_fval.sort_values(by = 'func_value', ascending  = True, inplace = True)
            best_fval.drop_duplicates(keep = 'first', inplace = True)
            if len(best_fval) >= 2:
                best_fval_values = best_fval['func_value'].values
                if abs((best_fval_values[0] - best_fval_values[1])/best_fval_values[0]) < SCORE_TOLERANCE:
                    print('cross grid search completed...'); break;
        len_prev_grid = len(grid)

        # devide intervals
        if nn < MAX_GRID_LEVEL - 1: params2, grid = update_divide_intervals(partype, params2, grid)
                
    if MIN_MAX == 'max': idx = grid['func_value'].idxmax()
    elif MIN_MAX == 'min': idx = grid['func_value'].idxmin()
    best_param = grid.astype(object).loc[idx, pkeys].to_dict()
    
    grid.drop(columns = ikeys, inplace = True)
    return best_param, best_fval, grid

def left_join_crossgridparams_params(xgrid_params, params):
    for (k,i) in xgrid_params.items(): 
        xgrid_params[k][1] = np.sort(np.unique(np.append(xgrid_params[k][1], params[k])))
    return xgrid_params

#### Getting Started! ##############################################
if __DEBUG_MODE__:
    def xgrid_search_target_function(**param):
        #--- STRAT user definition ---
        def any_user_function(x,y,z):
            return ((x-2.7)**2) + ((y-3.3)**2) + ((z+2.6)**2) + 1.0
        output = any_user_function(**param)
        #--- END user definition ---
        return output

    params = { # define the data type and input varaible range
        'x': ['int', [-10, 10]], # uni / log / int
        'y': ['log', [0, 0.01, 10]], # uni / log / int
        'z': ['uni', [-10, -1, 10]]  # uni / log / int
    }

    param = {'x': 3, 'y': 4, 'z': 5, 'a': 6, 'b': 7} # sample code for how to use left_join_crossgridparams_params
    params = left_join_crossgridparams_params(params, param) # sample code for how to use left_join_crossgridparams_params

    best_param, best_fval, grid = xgrid_search(xgrid_search_target_function, params, MIN_MAX = 'min', SCORE_TOLERANCE = 1e-5) # decide on min/max problem and then run!
    print('best param = ',best_param)
    print(best_fval)


# In[3]:


import pandas as pd
import numpy as np
import time
import xgboost as xgb
from xgboost.sklearn import XGBClassifier, XGBRegressor
import lightgbm as lgb
from lightgbm.sklearn import LGBMClassifier, LGBMRegressor
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split
from sklearn import metrics   #Additional scklearn functions

def xgrid_search_boosting(train, test, features, target, params_schedule, model, eval_metric, MIN_MAX, 
                          CV_MODE = 'cross validation 1', N_FOLD = 5, N_BOOST_ROUND = 10000, EARLY_STOPPING = 50, RAND_SEED = 123): 
    #--- user_defined_eval_function --------------------------------------------------------------
    def user_defined_eval_function(train, test, features, target, model, eval_metric, MIN_MAX, predict_test_output = False):
        if CV_MODE == 'validation': # validatoin approach: XGBoost
            X_train, X_valid, y_train, y_valid = train_test_split(train[features], train[target], test_size=1/N_FOLD, random_state=RAND_SEED)
            model.set_params(n_estimators = N_BOOST_ROUND) # initialize n_estimators
            model.fit(X_train, y_train, eval_set = [(X_train, y_train), (X_valid, y_valid)], eval_metric = eval_metric, 
                        early_stopping_rounds = EARLY_STOPPING, verbose = False) #Fit the algorithm on the data
            if MIN_MAX == 'max': idx = np.array(list(model.evals_result()['validation_1'].values())).argmax()
            elif MIN_MAX == 'min': idx = np.array(list(model.evals_result()['validation_1'].values())).argmin()
            model.set_params(n_estimators = idx + 1) # update n_estimators
            train_score = np.array(list(model.evals_result()['validation_0'].values())).squeeze()[idx]
            valid_score = np.array(list(model.evals_result()['validation_1'].values())).squeeze()[idx]
            test_pred = model.predict(test[features])     # computationally not expensive
        elif (CV_MODE == 'cross validation 1') and ('XGB' in str(model)): # cross validation 1: XGBoost
            dtrain = xgb.DMatrix(train[features], label=train[target], missing=np.nan) # missing value handling: https://www.youtube.com/watch?v=cVqDguNWh4M
            cvoutp = xgb.cv(model.get_xgb_params(), dtrain, num_boost_round=N_BOOST_ROUND, verbose_eval=False,
                              nfold=N_FOLD, metrics=eval_metric, early_stopping_rounds=EARLY_STOPPING, seed=RAND_SEED) 
            model.set_params(n_estimators = cvoutp.shape[0]) # update n_estimator 
            train_score = cvoutp.tail(1)[cvoutp.columns[cvoutp.columns.str.contains('train-.+-mean', regex=True)]].squeeze()
            valid_score = cvoutp.tail(1)[cvoutp.columns[cvoutp.columns.str.contains('test-.+-mean', regex=True)]].squeeze()

            if predict_test_output == True:
                model.fit(train[features], train[target].values.ravel(), eval_metric = eval_metric) #Fit the algorithm on the data
                test_pred = model.predict(test[features])    
            else: 
                test_pred = []
        elif (CV_MODE == 'cross validation 1') and ('LGB' in str(model)): # cross validation 1: LightGBM
            dtrain = lgb.Dataset(train[features], label=train[target])

            cvoutp = lgb.cv({k:v for k,v in model.get_params().items() if k not in ['n_estimators', 'silent']}, # exclude n_estimators because of the argument, 'num_boost_round'
                            dtrain, num_boost_round=N_BOOST_ROUND, verbose_eval=False, 
                            nfold=N_FOLD, metrics=eval_metric, early_stopping_rounds=EARLY_STOPPING, seed=RAND_SEED)
            model.set_params(n_estimators = len(cvoutp[eval_metric+'-mean'])) # update n_estimator with the best num_boost_round
            valid_score = cvoutp[eval_metric+'-mean'][-1] # best CV score

            if predict_test_output == True:
                model.fit(train[features], train[target].values.ravel(), eval_metric = eval_metric) #Fit the algorithm on the data
                test_pred = model.predict(test[features])    
            else: 
                test_pred = []
        elif CV_MODE == 'cross validation 2': # cross validation 2: XGBoost, LightGBM
#             folds = StratifiedKFold(n_splits=N_FOLD, shuffle=False, random_state=RAND_SEED) # cv n-fold
            folds = KFold(n_splits=N_FOLD, shuffle=False, random_state=RAND_SEED) # cv n-fold
            oof = np.zeros(len(train))
            test_pred = np.zeros(len(test))
            for n, (trn_idx, val_idx) in enumerate(folds.split(train[features].values, train[target].values)):
                X_train, y_train = train.iloc[trn_idx][features], train.iloc[trn_idx][target].values.ravel()
                X_valid, y_valid = train.iloc[val_idx][features], train.iloc[val_idx][target].values.ravel()

                model.set_params(n_estimators = N_BOOST_ROUND) # initialize n_estimators
                model.fit(X_train, y_train, eval_set = [(X_train, y_train), (X_valid, y_valid)], eval_metric = eval_metric, 
                            early_stopping_rounds = EARLY_STOPPING, verbose = False) #Fit the algorithm on the data

                if eval_metric == 'auc': 
                    oof[val_idx] = model.predict_proba(X_valid)[:,1]
                    test_pred += model.predict_proba(test[features])[:,1] / folds.n_splits
                if eval_metric == 'rmse': 
                    oof[val_idx] = model.predict(X_valid)
                    test_pred += model.predict(test[features]) / folds.n_splits

            if eval_metric == 'auc': 
                valid_score = metrics.roc_auc_score(train[target], oof)
            if eval_metric == 'rmse': 
                valid_score = np.sqrt(metrics.mean_squared_error(train[target], oof))
        return test_pred, valid_score    
    
    #--- evaluation function with xgboost, ligthgbm ------------------------------
    def xgrid_search_target_function(**param): # define user function with all the input variables
        #--- START: user defined function -----------------------------
        model.set_params(**param) # update some parameters
        test_pred, valid_score = user_defined_eval_function(train, test, features, target, model, eval_metric, MIN_MAX)
        #--- END ------------------------------------------------------
        return valid_score

    #-----------------------------------------------------------------------
    tic = time.time()
    for params in params_schedule:
    #     params = left_join_crossgridparams_params(params, model.get_xgb_params()) # ensure that the latest xgmodel values are included
        best_param, best_fval, grid = xgrid_search(xgrid_search_target_function, params, MIN_MAX = MIN_MAX, SCORE_TOLERANCE = 1e-5) # decide on min/max problem and then run!
        model.set_params(**best_param) # update some parameters with the best so far
        print('Best Param = ',best_param)
        print(best_fval)    
        print(model)
    
    test_pred, valid_score = user_defined_eval_function(train, test, features, target, model, eval_metric, MIN_MAX, predict_test_output = True)
    toc = time.time()
    print('Time Elapsed = %s sec'%(toc - tic))
    print('Final Validatoin Score = ',valid_score)
    print(model) # final model confirmation
    
    return model, test_pred


# In[5]:


if __DEBUG_MODE__:
    import sys
    sys.path.append("../")
    import utils

    # test dataset
    if True:
        #--- dataset for classification ------------
        np.random.seed(seed = 123)

        NN = 1000 # the number of data points
        x1 = np.random.uniform(0, 1, NN)
        x2 = np.random.uniform(0, 1, NN)
        # y = 2*(x1 - 0.5) - (x2 - 0.5) > 0 # line
        # y = x1**2 - x2 > 0 # parabolic 1
        y = 2*x1*(1-x1) - x2 > 0 # parabolic 2
        # y = ((x1 - 0.5)**2 + (x2 - 0.5)**2 - 0.3**2) > 0 # circle

        # dataset
        df = pd.DataFrame({'x1':x1, 'x2':x2, 'y':y})
        for n in range(1,0): # add uncorrelated features for test
            df['r%s'%n] = np.random.uniform(0, 1, NN)

        # train, test
        train, test = train_test_split(df, test_size = 0.2)
        target = ['y']
        features = [f for f in df.columns if f not in target]
        print(len(features))
        features
    else:
        #--- dataset for regression ----------------
        np.random.seed(seed = 123)
        x_0 = np.linspace(0,  5, num=1000, endpoint=False); r_0 = np.random.normal(0, 0.3, len(x_0))
        x_1 = np.linspace(5, 10, num=1000, endpoint=False); r_1 = np.random.normal(0, 0.3, len(x_1))
        y0 = np.concatenate((np.sin(x_0)+5, np.sin(4*x_1)))
        # y0 = np.concatenate((np.sin(x_0), np.sin(1*x_1)))

        x = np.concatenate((x_0, x_1))
        y = y0 + np.concatenate((r_0, r_1))

        df = pd.DataFrame({'x':x, 'y0':y0, 'y':y})

        # train, test
        train, test = train_test_split(df, test_size = 0.2)
        features = ['x']
        target = ['y']

    #--- LigthGBM -----------------------------------------------------------------
    eval_metric = 'auc'; MIN_MAX = 'max'; lgbmodel = LGBMClassifier(learning_rate = 0.1, n_jobs = 4, random_state = 123) # classification 
    # eval_metric = 'rmse'; MIN_MAX = 'min'; lgbmodel = LGBMRegressor(learning_rate = 0.1, n_jobs = 4, random_state = 123) # regression

    params_schedule = [
        #ref) https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
        #ref) https://lightgbm.readthedocs.io/en/latest/Parameters.html
        #ref) https://www.reddit.com/r/MachineLearning/comments/aspx8x/d_methods_for_hyperparameter_tuning_with_lightgbm/
        {'learning_rate': ['log', [0.1]]},

        {'num_leaves': ['int', [8, 31, 128, 1000]],  # uni / log / int
    #      'min_child_samples': ['int', [0, 20, 200]]}, # min_data_in_leaf (uni / log / int)
#          'min_child_samples': ['int', [0, 10, 20, 50, 100, 200, 500, 1000]]}, # min_data_in_leaf (uni / log / int)
         'min_child_samples': ['int', [0, 10, 20, 50, 100, 200]]}, # min_data_in_leaf (uni / log / int)
    #          'min_child_weight': ['log', [0.001, 1000]]}, # min_sum_hessian_in_leaf (uni / log / int)
        {'min_split_gain': ['uni', [0, 1, 3, 10, 30, 100, 300, 1000]]}, #min_gain_to_split (uni / log / int)
        {'subsample': ['uni', [0.2,0.4,0.6,0.8,1.0]], # bagging_fraction
    #      'subsample_freq': ['int', [0,10,100]], # bagging_freq
         'colsample_bytree': ['uni', [0.2, 0.4, 0.6, 0.8, 1.0]]},  # feature_fraction (uni / log / int)
        {'reg_alpha': ['uni', [0, 1, 10, 100, 500]], # lambda_l1 
         'reg_lambda': ['uni', [0, 1, 10, 100, 500]]}, # lambda_l2 (uni / log / int)

        {'learning_rate': ['log', [0.005, 0.1, 0.2]]} # uni / log / int
    ]
    lgbmodel, test_pred_lgb = xgrid_search_boosting(train, test, features, target, params_schedule, lgbmodel, eval_metric, MIN_MAX,
                                CV_MODE = 'cross validation 1', N_FOLD = 5, N_BOOST_ROUND = 10000, EARLY_STOPPING = 50, RAND_SEED = 123)
    print('Train'); utils.eval_model_scores(lgbmodel, train, features, target)
    print('Test'); utils.eval_model_scores(lgbmodel, test, features, target)
    
    #--- XGBoost -----------------------------------------------------------------
    eval_metric = 'auc'; MIN_MAX = 'max'; xgbmodel = XGBClassifier(learning_rate = 0.1, n_jobs = 4, random_state = 123) # classification 
#     eval_metric = 'rmse'; MIN_MAX = 'min'; xgbmodel = XGBRegressor(learning_rate = 0.1, n_jobs = 4, random_state = 123) # regression

    params_schedule = [
#         #ref) https://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/
#         {'learning_rate': ['log', [0.1]]},

#         {'max_depth': ['int', [3, 5, 7, 9, 11]], # uni / log / int
#          'min_child_weight': ['log', [1, 10, 100, 1000]]}, # uni / log / int
#         {'gamma': ['log', [0, 0.001, 1, 1000]]}, # uni / log / int
#         {'subsample': ['uni', [0.2, 0.4, 0.6, 0.8, 1.0]],  # uni / log / int
#          'colsample_bytree': ['uni', [0.2, 0.4, 0.6, 0.8, 1.0]]},  # uni / log / int
#         {'reg_alpha': ['log', [0, 0.001, 1, 1000]],
#          'reg_lambda': ['log', [1, 10, 100, 1000]]},  # uni / log / int

#         {'learning_rate': ['log', [0.005, 0.1, 0.2]]} # uni / log / int
    ]

    xgbmodel, test_pred_xgb = xgrid_search_boosting(train, test, features, target, params_schedule, xgbmodel, eval_metric, MIN_MAX,
                                CV_MODE = 'cross validation 1', N_FOLD = 5, N_BOOST_ROUND = 10000, EARLY_STOPPING = 50, RAND_SEED = 123)
    print('Train'); utils.eval_model_scores(xgbmodel, train, features, target)
    print('Test'); utils.eval_model_scores(xgbmodel, test, features, target)
    print(utils.feature_importance_xgboost(features, xgbmodel))


# In[ ]:





# In[ ]:




