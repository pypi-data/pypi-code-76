import numpy as np
import pandas as pd

DF = pd.DataFrame
ARRAY = np.array


def __weighted_mean(x: ARRAY, weight: ARRAY) -> float:
    """Takes weighted mean on `values_column` by `weighted_column`.

    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param x: Column to take weighted mean.
    :type x: ``np.array``
    :param weight: Column with weight.
    :type weight: ``np.array``
    :return: Weighted mean.
    :rtype: ``float``
    """
    return np.vdot(x, weight) / weight.sum()


def resolution_metric(daily_resolution_rate: ARRAY, DAU: ARRAY) -> float:
    """Return resolution metric for given time frame.
    
    The resolution rate of given time frame is defined as the weighted mean of daily_resolution with DAUs as weight.
    
    :param daily_resolution_rate: Variable array.
    :type daily_resolution_rate: ``numpy.ndarray``
    :param DAU: Array with DAU to act as weight.
    :type DAU: ``numpy.ndarray``
    :return: Geometric mean of weighted metrics.
    :rtype: ``numpy.float64``
    """
    if len(DAU) != len(daily_resolution_rate):
        raise ValueError("`daily_resolution_rate` and `DAU` arrays must have same length.")
        
    if any(DAU[i] == 0 for i in range(len(DAU))
           if daily_resolution_rate[i]>0):
        raise ValueError("Every DAU cannot be `0` when there is resolution in the same day.")
    
    try:
        return __weighted_mean(x=daily_resolution_rate, weight=DAU)
    except ValueError:
        raise TypeError("`np.ndarray` from input must contain only numbers.")


def daily_resolution(dataframe: DF, amount: str, dau_column: str) -> ARRAY:
    """Return daily resolution metric for given array.
    
    The daily resolution metric is calculated as the unique user amount on the resolution nodes divided by DAU.
    
    :param dataframe: A dataframe containing daily resolution and DAUs.
    :type: ``pandas.DataFrame``
    :param amount: Name of column that contains amount unique users per resolution node.
    :type amount: ``str``
    :param dau_column: Name of the column that contains DAUs
    :type dau_column: ``str``
    :return: Array with daily resolution.
    :rtype: ``numpy.ndarray``
    """
    if any(dataframe[dau_column][i]==0 for i in range(len(dataframe))
           if dataframe[amount][i]>0):
        raise ValueError("Every DAU cannot be `0` when there is resolution in the same day.")
    
    r = np.array(dataframe[amount] / dataframe[dau_column])
    
    if any(np.isinf(r)):
        raise ArithmeticError("Method generated `inf` values. Please check if inputs are correct.")
    return r
