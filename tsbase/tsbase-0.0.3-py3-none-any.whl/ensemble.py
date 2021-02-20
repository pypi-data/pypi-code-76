"""
    Ensemble Learning (EL)
"""

import numpy as np
from base.model import *


def blending(models, train_x=None, train_y=None,
             valid_x=None, valid_y=None,
             test_x=None, test_y=None):

    # Copy the initial input data
    tr_x, tr_y = train_x.copy(), train_y.copy()
    v_x, v_y = valid_x.copy(), valid_y.copy()
    te_x, te_y = test_x.copy(), test_y.copy()
    # Get the number of samples
    (n_samples_tr, n_timesteps, n_features) = tr_x.shape
    n_samples_v = v_x.shape[0]
    n_samples_te = te_x.shape[0]

    n_layers = len(models.keys())
    layers_ = list(models.keys())  # ['first', 'second']

    tr_x_meta, tr_y_meta = None, None
    te_x_meta, te_y_meta = None, None
    for k in range(n_layers):
        if k != n_layers-1:
            print(' The %s layers ...' % layers_[k])
            n_models = len(models[layers_[k]])
            tr_x_meta, tr_y_meta = np.zeros((n_samples_v, n_models)), None
            te_x_meta, te_y_meta = np.zeros((n_samples_te, n_models)), None
            for j in range(n_models):
                print('  Layer %d: %s' % (k+1, models[layers_[k]][j]['type']))
                pred_in_valid, pred_in_test = None, None
                if models[layers_[k]][j]['type'] in ['Bayesian', 'SGD', 'SVR', 'KNR', 'RF', 'GBDT']:
                    # Convert 3D X into 2D X
                    tr_x_ = tr_x.reshape(n_samples_tr, n_timesteps*n_features)
                    v_x_ = v_x.reshape(n_samples_v, n_timesteps*n_features)
                    te_x_ = te_x.reshape(n_samples_te, n_timesteps*n_features)
                    # Get the parameters of model
                    params = models[layers_[k]][j]['params']
                    if models[layers_[k]][j]['type'] == 'Bayesian':
                        # Fit model with training set and predict the validation set
                        bay_model, pred_in_valid = bayesian_ridge(tr_x_, tr_y, v_x_,
                                                                  is_default=params['is_default'])
                        # Predict the test set
                        pred_in_test = bay_model.predict(te_x_)
                    elif models[layers_[k]][j]['type'] == 'SGD':
                        sgd_model, pred_in_valid = sgd(tr_x_, tr_y, v_x_,
                                                       is_default=params['is_default'])
                        pred_in_test = sgd_model.predict(te_x_)
                    elif models[layers_[k]][j]['type'] == 'SVR':
                        svr_model, pred_in_valid = svr(tr_x_, tr_y, v_x_,
                                                       params['kernel'], params['gamma'],
                                                       params['C'], params['cache_size'],
                                                       params['is_default'])  # output: (n, )
                        pred_in_test = svr_model.predict(te_x_)  # output: (n, )
                    elif models[layers_[k]][j]['type'] == 'RF':
                        rf_model, pred_in_valid = rf(tr_x_, tr_y, v_x_,
                                                     n_estimators=params['n_estimators'],
                                                     is_default=params['is_default'])
                        pred_in_test = rf_model.predict(te_x_)
                    elif models[layers_[k]][j]['type'] == 'GBDT':
                        gbdt_model, pred_in_valid = gbdt(tr_x_, tr_y, v_x_,
                                                         n_estimators=params['n_estimators'],
                                                         is_default=params['is_default'])
                        pred_in_test = gbdt_model.predict(te_x_)
                elif models[layers_[k]][j]['type'] in ['LightGBM', 'lgb']:
                    pass
                elif models[layers_[k]][j]['type'] in ['LSTM', 'GRU']:
                    pass
                # Fusion the predicted results of validation set as the meta training set
                tr_x_meta[:, j] = pred_in_valid.copy()
                # Fusion the predicted results of test set as the meta test set
                te_x_meta[:, j] = pred_in_test.copy()
            # Copy the actual values of validation set and test set
            tr_y_meta = v_y.copy()
            te_y_meta = te_y.copy()
        else:
            print('--> The %s(final) layer ... ' % layers_[k])
            print('Meta training set:', tr_x_meta.shape, tr_y_meta.shape)
            print('Meta test set', te_x_meta.shape, te_y_meta.shape)
            # Get the parameters of model
            params = models[layers_[k]][0]['params']
            if models[layers_[k]][0]['type'] in ['LightGBM', 'lgb']:
                # Copy the meta training set and meta test set
                tr_x_ = tr_x_meta.copy()
                te_x_ = te_x_meta.copy()
                # Convert 2D Y into 1D Y
                tr_y_ = tr_y_meta.reshape(n_samples_v)
                te_y_ = te_y_meta.reshape(n_samples_te)
                # Get the special parameters of model
                num_boost_round = models[layers_[k]][0]['num_boost_round']
                # Fit model with meta training set and predict the test set
                booster, pred_val = light_gbm(tr_x_, tr_y_, te_x_,
                                              params=params,
                                              num_boost_round=num_boost_round)
                return pred_val, te_y_  # (n, ), (n, )
            elif models[layers_[k]][0]['type'] in ['XGBoost', 'xgb']:
                pass


def stacking(models, k_fold=4,
             train_x=None, train_y=None,
             test_x=None, test_y=None):
    """
    shape=(samples, timesteps, features)
    """

    tr_x, tr_y = train_x.copy(), train_y.copy()
    te_x, te_y = test_x.copy(), test_y.copy()
    n = len(tr_x) // k_fold
    (n_samples_tr, n_timesteps, n_features) = tr_x.shape
    n_samples_te = test_x.shape[0]
    n_samples_tr_fold = n * k_fold

    n_layers = len(models.keys())
    layers_ = list(models.keys())  # ['first', 'second']

    print('=' * 50)
    print('  Ensemble Learning: Stacking')
    print('  - Number of original train data: %d' % n_samples_tr)
    print('  - Number of original test data: %d' % n_samples_te)
    print('  - Number of layers: %d' % n_layers)
    print('  - Number of train data in k-fold: %d' % n_samples_tr_fold)
    print('=' * 50, '\n')

    tr_x_meta, tr_y_meta = None, None
    te_x_meta, te_y_meta = None, None
    for i in range(n_layers):
        if i != n_layers - 1:
            print(' The %s layers ...' % layers_[i])
            n_models = len(models[layers_[i]])
            tr_x_meta, tr_y_meta = np.zeros((n_samples_tr_fold, n_models)), None
            te_x_meta, te_y_meta = np.zeros((n_samples_te, n_models)), None
            for j in range(n_models):
                print('  Layer %d: %s' % (i + 1, models[layers_[i]][j]['type']))
                temp_pred_in_fold, temp_pred_in_test = list(), list()
                if models[layers_[i]][j]['type'] in ['Bayesian', 'SGD', 'SVR',
                                                     'KNR', 'RF', 'GBDT', 'XGBoost', 'xgb']:
                    # 3-D to 2-D
                    tr_x_ = tr_x.reshape(n_samples_tr, n_timesteps * n_features)
                    tr_y_ = tr_y.copy()
                    te_x_ = te_x.reshape(n_samples_te, n_timesteps * n_features)
                    # k-fold CV
                    for k in range(k_fold):
                        tr_x_fold = np.concatenate([tr_x_[0:n * k, :],
                                                    tr_x_[n * (k + 1):n * k_fold, :]], axis=0)
                        tr_y_fold = np.concatenate([tr_y_[0:n * k, :],
                                                    tr_y_[n * (k + 1):n * k_fold, :]], axis=0)
                        te_x_fold = tr_x_[n * k:n * (k + 1), :]
                        te_y_fold = tr_y_[n * k:n * (k + 1), :]
                        pred_in_fold, pred_in_test = None, None
                        params = models[layers_[i]][j]['params']
                        if models[layers_[i]][j]['type'] == 'Bayesian':
                            bay_model, pred_in_fold = bayesian_ridge(tr_x_fold, tr_y_fold, te_x_fold,
                                                                     n_iter=params['n_iter'],
                                                                     is_default=params['is_default'])
                            pred_in_test = bay_model.predict(te_x_)
                        elif models[layers_[i]][j]['type'] == 'SGD':
                            sgd_model, pred_in_fold = sgd(tr_x_fold, tr_y_fold, te_x_fold,
                                                          is_default=params['is_default'])
                            pred_in_test = sgd_model.predict(te_x_)
                        elif models[layers_[i]][j]['type'] == 'SVR':
                            svr_model, pred_in_fold = svr(tr_x_fold, tr_y_fold, te_x_fold,
                                                          params['kernel'], params['gamma'],
                                                          params['C'], params['cache_size'],
                                                          params['is_default'])  # output: (n, )
                            pred_in_test = svr_model.predict(te_x_)  # output: (n, )
                            pred_in_test = pred_in_test.reshape(len(pred_in_test), 1)  # (n, 1)
                        elif models[layers_[i]][j]['type'] == 'KNR':
                            knr_model, pred_in_fold = knr(tr_x_fold, tr_y_fold, te_x_fold,
                                                          n_neighbors=params['n_neighbors'],
                                                          p=params['p'],
                                                          leaf_size=params['leaf_size'],
                                                          is_default=params['is_default'])
                            pred_in_test = knr_model.predict(te_x_)
                        elif models[layers_[i]][j]['type'] == 'RF':
                            rf_model, pred_in_fold = rf(tr_x_fold, tr_y_fold, te_x_fold,
                                                        n_estimators=params['n_estimators'],
                                                        is_default=params['is_default'])
                            pred_in_test = rf_model.predict(te_x_)
                        elif models[layers_[i]][j]['type'] == 'GBDT':
                            gbdt_model, pred_in_fold = gbdt(tr_x_fold, tr_y_fold, te_x_fold,
                                                            n_estimators=params['n_estimators'],
                                                            is_default=params['is_default'])
                            pred_in_test = gbdt_model.predict(te_x_)
                        elif models[layers_[i]][j]['type'] in ['XGBoost', 'xgb']:
                            num_boost_round = models[layers_[i]][j]['num_boost_round']
                            booster, pred_in_fold = xg_boost(tr_x_fold, tr_y_fold, te_x_fold,
                                                             params=params,
                                                             num_boost_round=num_boost_round)
                            dtest = xgboost.DMatrix(te_x_)
                            pred_in_test = booster.predict(dtest)
                        # single model results in K-fold
                        pred_in_test = pred_in_test.reshape(len(pred_in_test), 1)  # (n, 1)
                        temp_pred_in_fold.append(pred_in_fold)
                        temp_pred_in_test.append(pred_in_test)
                elif models[layers_[i]][j]['type'] in ['LSTM', 'GRU']:
                    tr_x_, tr_y_ = tr_x.copy(), tr_y.copy()
                    te_x_ = te_x.copy()
                    for k in range(k_fold):
                        print('    K-fold CV:', k + 1)
                        tr_x_fold = np.concatenate([tr_x_[0:n * k, :, :],
                                                    tr_x_[n * (k + 1):n * k_fold, :, :]], axis=0)
                        tr_y_fold = np.concatenate([tr_y_[0:n * k, :],
                                                    tr_y_[n * (k + 1):n * k_fold, :]], axis=0)
                        te_x_fold = tr_x_[n * k:n * (k + 1), :, :]

                        params = models[layers_[i]][j]['params']
                        model = models[layers_[i]][j]['model']
                        model.fit(tr_x_fold, tr_y_fold,
                                  epochs=params['epochs'],
                                  batch_size=params['batch_size'], verbose=0)
                        pred_in_fold = model.predict(te_x_fold)
                        pred_in_test = model.predict(te_x_)

                        temp_pred_in_fold.append(pred_in_fold)
                        temp_pred_in_test.append(pred_in_test)
                elif models[layers_[i]][j]['type'] in ['lgb', 'ligbhgbm']:
                    pass
                # For
                temp_pred_in_fold = np.concatenate(temp_pred_in_fold, axis=0)  # (n, )
                temp_pred_in_fold = temp_pred_in_fold.reshape(len(temp_pred_in_fold))
                temp_pred_in_test = np.concatenate(temp_pred_in_test, axis=1)  # (n, m)
                tr_x_meta[:, j] = temp_pred_in_fold.copy()
                te_x_meta[:, j] = temp_pred_in_test.mean(axis=1)
            # Copy the actual values of training set which are used to CV and test set
            tr_y_meta = tr_y[0: n_samples_tr_fold, :].copy()
            te_y_meta = te_y.copy()
        else:
            # The final layer
            print(' The %s(final) layer ... ' % layers_[i])
            print('  Meta training set:', tr_x_meta.shape, tr_y_meta.shape)
            print('  Meta test set', te_x_meta.shape, te_y_meta.shape)
            params = models[layers_[i]][0]['params']
            if models[layers_[i]][0]['type'] in ['LightGBM', 'lgb']:
                # Copy the meta training set and meta test set
                tr_x_ = tr_x_meta.copy()
                te_x_ = te_x_meta.copy()
                # 2-D to 1-D
                tr_y_ = tr_y_meta.reshape(n_samples_tr_fold)
                te_y_ = te_y_meta.reshape(n_samples_te)
                # train model
                num_boost_round = models[layers_[i]][0]['num_boost_round']
                booster, pred_val = light_gbm(tr_x_, tr_y_, te_x_,
                                              params=params,
                                              num_boost_round=num_boost_round)
                return pred_val, tr_x_, tr_y_, te_x_, te_y_  # (n, ), (n, )
            elif models[layers_[i]][0]['type'] in ['XGBoost', 'xgb']:
                tr_x_ = tr_x.copy()
                tr_y_ = tr_y.copy()
                te_x_ = te_x.copy()
                te_y_ = te_y.copy()
                num_boost_round = models[layers_[i]][0]['num_boost_round']
                booster, pred_val = xg_boost(tr_x_, tr_y_, te_x_,
                                             params=params,
                                             num_boost_round=num_boost_round)
                return pred_val, tr_x_, tr_y_, te_x_, te_y_  # (n, ), (n, )

