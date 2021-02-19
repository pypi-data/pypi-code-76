import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import missingno as msno


def corr(ds):
    return abs(ds.corr()['count']).sort_values()


def handle_outliers(df_raw, columns, drop=False, upper_quantile=.95, lower_quantile=.05):
    df = df_raw.copy()

    for column in columns:
        if column not in df: continue

        upper_lim = df[column].quantile(upper_quantile)
        lower_lim = df[column].quantile(lower_quantile)

        if not drop:
            df.loc[(df[column] > upper_lim), column] = upper_lim
            df.loc[(df[column] < lower_lim), column] = lower_lim
        else:
            df = df.loc[(df[column] < upper_lim) & (df[column] > lower_lim)]

    return df


def transform(df_raw, columns, fn=np.log1p):
    df = df_raw.copy()
    for column in columns:
        if column in df:
            df[column] = df[column].transform(fn)

    return df


def drop(df_raw, columns):
    df = df_raw.copy()
    for column in columns:
        if column in df:
            df.drop(column, axis=1, inplace=True)

    return df


def group_by_mean(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].mean(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_mean'))
    return df


def group_by_max(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].max(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_max'))
    return df


def group_by_min(df_raw, pairs):
    df = df_raw.copy()
    for group_col, agr_col in pairs:
        if group_col in df and agr_col in df:
            df = pd.merge(df, df.groupby(group_col)[agr_col].min(),
                          left_on=group_col, right_on=group_col, suffixes=('', f'_{group_col}_min'))
    return df


def scale(df_raw, columns, minMax=False):
    df = df_raw.copy()

    if minMax:
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()

    for col in columns:
        if col in df_raw:
            df[col] = scaler.fit_transform(np.array(df[col]).reshape(-1, 1)).reshape(-1)
    return df


def describe_missing_values(df):
    msno.bar(df)
    msno.matrix(df)
    msno.heatmap(df)
