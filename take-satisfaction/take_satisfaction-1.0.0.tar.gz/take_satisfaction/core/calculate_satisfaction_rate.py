import typing as tp

import numpy as np
import pandas as pd

NUMBER = tp.Union[float, int]
ARRAY = tp.Union[pd.Series, np.ndarray]
DF = pd.DataFrame
S = pd.Series


def __weighted_mean(x: ARRAY, w: ARRAY) -> float:
    """Takes weighted mean.

    :param x: Values to be averaged.
    :type x: ``pd.Series`` or ``np.ndarray``
    :param w: Weights to be applied.
    :type w: ``pd.Series`` or ``np.ndarray``
    :return: Weighted mean.
    :rtype: ``float``
    """
    return np.vdot(x, w) / np.sum(w)


def __scale(x: NUMBER, min_: NUMBER, max_: NUMBER) -> NUMBER:
    """Transform a value x to a scale between min_ and max_.

    :param x: Value to be converted.
    :type x: ``float`` or ``int``
    :param min_: Minimum value on scale.
    :type min_: ``float`` or ``int``
    :param max_: Maximum value on scale.
    :type max_: ``float`` or ``int``
    :return: Scaled value.
    :rtype: ``float`` or ``int``
    """
    return (x - min_) / (max_ - min_)


def calculate_satisfaction_rate(df: DF, scale_column: str, amount_column: str) -> float:
    """ Calculates the satisfaction rate based on the bot scale.

    :param df: Treated dataframe containing `CSR` scales as numeric and the `amount` per scale.
    :type df: ``pandas.DataFrame``
    :param scale_column: Name of the scale column.
    :type scale_column: ``str``
    :param amount_column: Name of column with amount per scale.
    :type amount_column: ``str``
    :return: Satisfaction rate.
    :rtype: ``float``
    """
    mean = __weighted_mean(df[scale_column], df[amount_column])
    return __scale(mean, min(df[scale_column]), max(df[scale_column]))
