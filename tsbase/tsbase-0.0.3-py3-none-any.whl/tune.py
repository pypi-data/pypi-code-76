
from itertools import product
from model import *
from metrics import *


def tune_svr(tr_x, tr_y, te_x, te_y, mean, std, 
             kernel='rbf', para_gamma=None, para_C=None, cache_size=2000):
    
    for gamma in para_gamma:
        for C in para_C:
            svr_model, pred = svr(tr_x, tr_y, te_x, te_y, 
                                  kernel=kernel, gamma=gamma, C=C, cache_size=cache_size)
            rmse, mape = eval(te_y, pred, mean, std)
            print('==> ', 'gamma=', gamma, '  C=', C, '  RMSE=', rmse, ' MAPE=', mape)
            


def tune_lgb_xgb(tr_x, tr_y, te_x, te_y, mean, std, 
                 params_range=None, model='LightGBM'):
    '''
    LightGBM
    params_range = {'num_leaves':[26,27], 'max_depth':[6,7,8], 
                    'min_sum_hesian_in_leaf':[1], 'min_data_in_leaf':[10, 11],
                    'bagging_fraction':[0.6], 'feature_fraction':[0.7],
                    'lambda_l1':[0.3], 'lambda_l2':[1.1],
                    'min_gain_to_split':[0.0007], 
                    'learning_rate':[0.030], 
                    'objective':['regression'], 'boosting_type':['gbdt'], 
                    'num_boost_round':[3000]}
    --------------------------------------------
    XGBoost
    params_range = {'max_depth':[7], 'min_child_weight':[6], 
                    'subsample':[0.6], 'colsample_bytree':[0.8], 
                    'alpha':[0.05], 'lambda':[1],
                    'gamma':[0.03], 'eta':[0.050], 
                    'objective':['reg:squarederror'], 'booster':['gbtree'], 'verbosity':[0], 
                    'num_boost_round':[500]}
    '''
    
    search_keys, no_search_keys = list(), list()
    for key in params_range.keys():
        if key != 'num_boost_round':
            if len(params_range[key]) > 1:
                search_keys.append(key)      # 有多个参数
            else:
                no_search_keys.append(key)   # 只有一个参数
            
    # parameters of model        
    params = dict()
    # ---------
    for key in no_search_keys:
        if key != 'num_boost_round':
            params[key] = params_range[key][0]     # 
    # ---------
    if len(search_keys) > 0:
        loop_key = [params_range[key] for key in search_keys]
        combs = product(*loop_key)    # 参数值所有组合
        for val in combs:
            if len(search_keys) > 0:
                for i in range(len(search_keys)):
                    # params
                    params[search_keys[i]] = val[i]    #

            for num_boost_round in params_range['num_boost_round']:
                # call model
                if model=='Lightgbm' or model=='LightGBM':
                    rmse, mape, pred = light_gbm(tr_x, tr_y, te_x, te_y, mean, std, 
                                                 params=params, num_boost_round=num_boost_round)
                    print('==> RMSE=', rmse, '  params:', list(params.values()), '  num_boost:', num_boost_round)
                elif model=='xgboost' or model=='XGBoost':
                    rmse, mape, pred = xgb(tr_x, tr_y, te_x, te_y, mean, std, 
                                           params=params, num_boost_round=num_boost_round)
                    print('==> RMSE=', rmse, '  params:', list(params.values()), '  num_boost:', num_boost_round)
                else:
                    print('error...')
    else:
        for num_boost_round in params_range['num_boost_round']:
            # call model
            if model=='Lightgbm' or model=='LightGBM':
                rmse, mape, pred = light_gbm(tr_x, tr_y, te_x, te_y, mean, std, 
                                             params=params, num_boost_round=num_boost_round)
                print('==> RMSE=', rmse, '  params:', list(params.values()), '  num_boost:', num_boost_round)
            elif model=='xgboost' or model=='XGBoost':
                    rmse, mape, pred = xgb(tr_x, tr_y, te_x, te_y, mean, std, 
                                           params=params, num_boost_round=num_boost_round)
                    print('==> RMSE=', rmse, '  params:', list(params.values()), '  num_boost:', num_boost_round) 
            else:
                print('error...')


