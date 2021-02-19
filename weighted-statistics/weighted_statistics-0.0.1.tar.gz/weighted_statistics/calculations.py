import numpy as np
import pandas as pd

def median(df, values_col, weights_col, dropna = True):
    _df = df[[values_col, weights_col]]
    _df.dropna(subset=[values_col], inplace = dropna)
    _df = _df.sort_values(values_col).reset_index()
    _df['cumsum'] = _df[weights_col].cumsum()
    median_cumsum = _df[weights_col].sum() / 2
    median_iloc = np.searchsorted(_df['cumsum'], median_cumsum)
    return _df[values_col].iloc[median_iloc]
    
    
# def median2(df, values_col, weights_col, dropna = True):
#     _df = df[[values_col, weights_col]]
#     _df.dropna(subset=[values_col], inplace = dropna)
#     values = _df[values_col].to_numpy()
#     weights = _df[weights_col].to_numpy()
#     sort_index = values.argsort()
#     cumsum_arr = np.cumsum([weights[i] for i in sort_index])
#     median_iloc = np.searchsorted(cumsum_arr, cumsum_arr[-1]/2)
#     return np.array([values[i] for i in sort_index])[median_iloc]

def quantile(df, values_col, weights_col, q, dropna = True):
    _df = df[[values_col, weights_col]]
    _df.dropna(subset=[values_col], inplace = dropna)
    _df = _df.sort_values(values_col).reset_index()
    # _df['cumsum'] = _df[weights_col].cumsum()
    # quantile_cumsum = np.quantile(_df['cumsum'], q)
    cumsum = _df[weights_col].cumsum().to_numpy()
    quantile_iloc = np.searchsorted(cumsum, np.quantile(cumsum, q))
    return _df[values_col].iloc[quantile_iloc]
