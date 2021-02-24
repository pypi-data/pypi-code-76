import numpy as np
import pandas as pd
from typing import Tuple

def train_cal_test_split(df: pd.DataFrame,
                         target_column_name: str,
                         train_percentage: float,
                         cal_percentage: float,
                         random: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    r"""Function used for splitting the dataset in training, calibration and test subsets

    This fuction splits the data in `df` in three sets acording to the percentajes given as input:
    `train_percentage` and `cal_percentage`. The Tuple returned has 6 elements: the training data, the training
    target values, the calibration data, the calibration target values, the test data and target values.

    Parameters
    ----------
    df: pandas.DataFrame
        Data we want to split in training, calibration and test sets
    target_columns_name: str
        The name of the target feature
    train_percentage: float
        Fraction of the data we want to use for the training process
    cal_percentage: float
        Fraction of the data we want to use to calibrate the inductive
        conformal predictor
    random: bool
        Variable that defines if the dataset is shuffled before the split.
        True -> shuffle and False -> don't shuffle.

    Returns
    -------
    split_data: Tuple[ndarray, ndarray, ndarray, ndarray, ndarray, ndarray]
        Tuple with 6 elements: the trainign data, the training target feature,
        the calibration data and target, the test data and, finally, the test target values.

    Notes
    -----
    This fuction only works when there's only one target feature.
    """
    if random:
        df = df.sample(frac=1).reset_index(drop=True)
    X = df.drop(columns=target_column_name).to_numpy()
    Y = df[target_column_name].to_numpy()
    n_total = X.shape[0]
    n_train = int(train_percentage*n_total)
    n_cal = int(cal_percentage*n_total) + n_train
    train_data = X[:n_train, :]
    train_target = Y[:n_train]
    cal_data = X[n_train:n_cal, :]
    cal_target = Y[n_train:n_cal]
    test_data = X[n_cal:, :]
    test_target = Y[n_cal:]
    return train_data, train_target, cal_data, cal_target, test_data, test_target