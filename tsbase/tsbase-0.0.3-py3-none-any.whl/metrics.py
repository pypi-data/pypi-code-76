"""
    Metrics for regression tasks
    --------------------------------------------
    - Mean Squared Error, MSE
    - Root Mean Squared Error, RMSE
    - Mean Absolute Error, MAE
    - Mean Absolute Percentage Error, MAPE
    - R2 score
"""

import numpy as np


def re_standardize(x, _mean, _std):
    """
    Reverse standardization
    Args:
        x (array_like):      (m, ) or (m, 1)
        _mean (float):       Mean
        _std (float):        Std
    Returns:
        value (array_like):  (m, )
    """

    if isinstance(x, np.ndarray):
        value = x.copy()
        value = value * _std + _mean
        return np.reshape(value, (value.shape[0], ))
    else:
        print('The format x is: array_like')


def re_standardize_2d(x, _mean, _std):
    x = x*_std
    x = x+_mean
    return x


def re_normalize(x, min_value, max_value):
    """
    Reverse normalization
    Args:
        x (array_like):      (m, ) or (m, 1)
        min_value (float):   Minimal value
        max_value (float):   Maximum value
    Returns:
        value (array_like):  (m, )
    """

    if isinstance(x, np.ndarray):
        value = x.copy()
        value = value * (max_value - min_value) + min_value
        return np.reshape(value, (value.shape[0], ))
    else:
        print('The format x is: array_like')


def mean_squared_error(y_true, y_pred):
    """
    Mean Squared Error, MSE
    Args:
        y_true (array_like):    (m, ) or (m, 1)
        y_pred (array_like):    (m, ) or (m, 1)
    Returns:
        value (float):          Value of MSE
    """

    value = np.mean((y_true-y_pred)**2, axis=0)
    if isinstance(value, np.ndarray):
        return value[0]
    else:
        return value


def root_mean_squared_error(y_true, y_pred):
    """
    Root Mean Squared Error, RMSE
    Args:
        y_true (array_like):    (m, ) or (m, 1)
        y_pred (array_like):    (m, ) or (m, 1)
    Returns:
        value (float):          Value of RMSE
    """

    return np.sqrt(mean_squared_error(y_true, y_pred))


def mean_absolute_error(y_true, y_pred):
    """
    Mean Absolute Error, MAE
    Args:
        y_true (array_like):    (m, ) or (m, 1)
        y_pred (array_like):    (m, ) or (m, 1)
    Returns:
        value (float):          Value of MAE
    """

    value = np.mean(np.abs(y_true-y_pred), axis=0)
    if isinstance(value, np.ndarray):
        return value[0]
    else:
        return value


def mean_absolute_percentage_error(y_true, y_pred):
    """
    Mean Absolute Percentage Error, MAPE
    Args:
        y_true (array_like):    (m, ) or (m, 1)
        y_pred (array_like):    (m, ) or (m, 1)
    Returns:
        value (float):          Value of MAPE
    """

    value = np.mean(np.abs(y_true-y_pred)/y_true, axis=0) * 100
    if isinstance(value, np.ndarray):
        return value[0]
    else:
        return value


def r2_score(y_true, y_pred):
    """
    R2 Score, R2
    Args:
        y_true (array_like):    (m, ) or (m, 1)
        y_pred (array_like):    (m, ) or (m, 1)
    Returns:
        value (float):          Value of MAPE
    """

    num = np.sum((y_true-y_pred)**2, axis=0)
    den = np.sum((y_true-np.mean(y_true, axis=0))**2, axis=0)
    value = 1 - num / den
    if isinstance(value, np.ndarray):
        return value[0]
    else:
        return value


def get_metrics(y_true=None, y_pred=None, metrics='all',
                pre_deal=None, pre_a=None, pre_b=None,
                points=3, is_display=True):
    """
    Calculate the metrics between real value and predicted value
    Args:
        y_true (array_like):     Real value, (m, ) or (m, 1)
        y_pred (array_like):     Predicted value, (m, ) or (m, 1)
        metrics (str):           Name of metrics, e.g. 'all', 'rmse', 'mae', 'mape', 'r2'
        pre_deal (str):          Normalize or standardize, 'min_max' or 'std'
        pre_a (float):           Minimal value or mean value
        pre_b (float):           Maximum value or standard deviation
        points (inf):
        is_display (bool):
    """

    act_y_true, act_y_pred = None, None
    if pre_a is not None and pre_b is not None:
        if pre_deal == 'std':
            # 反标准化
            act_y_true = re_standardize(y_true, pre_a, pre_b)
            act_y_pred = re_standardize(y_pred, pre_a, pre_b)
        elif pre_deal == 'min_max':
            # 反Min-Max归一化
            act_y_true = re_normalize(y_true, pre_a, pre_b)
            act_y_pred = re_normalize(y_pred, pre_a, pre_b)
    else:
        act_y_true = y_true
        act_y_pred = y_pred

    _rmse = root_mean_squared_error(act_y_true, act_y_pred)
    _mae = mean_absolute_error(act_y_true, act_y_pred)
    _mape = mean_absolute_percentage_error(act_y_true, act_y_pred)
    _r2 = r2_score(act_y_true, act_y_pred)

    _rmse = round(_rmse, points)
    _mae = round(_mae, points)
    _mape = round(_mape, points)
    _r2 = round(_r2, points)

    if metrics == 'all':
        if is_display:
            print(' -> Metrics: ')
            print(' - RMSE: {}  - MAE: {}  - MAPE: {}  - R2: {}'
                  .format(_rmse, _mae, _mape, _r2))
        return _rmse, _mae, _mape, _r2
    elif metrics == 'rmse':
        return _rmse
    elif metrics == 'mae':
        return _mae
    elif metrics == 'mape':
        return _mape
    elif metrics == 'r2':
        return _r2
