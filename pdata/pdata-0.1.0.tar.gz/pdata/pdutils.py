import pandas as pd
import numpy as np


def pd_isin_multiple_cols(df1, df2):
    """
    For all columns in df2 
    and columns of df1 having the same names,
    select a subset of df1 consisting of rows
    that exist in df2.
    """

    mask = np.ones(len(df1), dtype=bool)

    for colname in df2.columns:

        col_match = df1[colname].isin(df2[colname])
        mask = mask & col_match

    return mask


def pd_content_in_columns_is_identical(df1, df2, colnames):
    """
    Check whether data in the selected 
    identically-named columns in two dataframes
    is identical. 

    Will only work for the dataframes with a common index. 
    Otherwise, a ValueError is raised:
    "Can only compare identically-labeled DataFrame objects". 
    """

    common_colnames = set(df1.columns).intersection(df2.columns)
    assert set(colnames).issubset(common_colnames)

    return np.all(df1[colnames] == df2[colnames])


def pd_col_is_identical_no_index(df1, df2, colname):
    """
    Check whether an identically-named column in 
    two dataframes has the same data. 
    The function disregards dataframe index. 
    """

    c1 = np.array(df1[colname])
    c2 = np.array(df2[colname])

    return np.all(c1 == c2)
