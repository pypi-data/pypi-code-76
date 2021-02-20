"""
    Models
"""

import xgboost
import lightgbm


def light_gbm(tr_x, tr_y, te_x,
              params=None,
              num_boost_round=None):
    """
    LightGBM
    ----------------
    params = {'num_leaves':20, 'max_depth':5,
              'min_sum_hesian_in_leaf':1, 'min_data_in_leaf':13,
              'bagging_fraction':0.6, 'feature_fraction':0.7,
              'lambda_l1':0.3, 'lambda_l2':1.1,
              'min_gain_to_split':0.0002,
              'learning_rate':0.030,
              'objective':'regression', 'boosting_type':'gbdt'}
    """

    dtrain = lightgbm.Dataset(tr_x, label=tr_y)
    booster = lightgbm.train(params=params, train_set=dtrain,
                             num_boost_round=num_boost_round)
    pred_val = booster.predict(te_x)

    return booster, pred_val


def xg_boost(tr_x, tr_y, te_x,
             params=None,
             num_boost_round=None):
    """
    XGBoost
    ------------
    params = {'max_depth':7, 'min_child_weight':6,
              'subsample':0.6, 'colsample_bytree':0.8,
              'alpha':0.05, 'lambda':1,
              'gamma':0.03, 'eta':0.025,
              'objective':'reg:squarederror', 'booster':'gbtree', 'verbosity':0}
    """

    dtrain = xgboost.DMatrix(tr_x, label=tr_y)
    dtest = xgboost.DMatrix(te_x)
    booster = xgboost.train(params=params, dtrain=dtrain,
                            num_boost_round=num_boost_round)
    pred_val = booster.predict(dtest)

    return booster, pred_val
