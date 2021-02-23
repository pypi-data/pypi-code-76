import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import missingno as msno
from datetime import timedelta
from datetime import datetime
import time
from kowalsky.logs.utils import calc_percent


class ProgressTracker:

    def __init__(self, n):
        self.progress = 0
        self.n = n

        self.notify_n = n // 100

        self.last_time = None
        self.times = []

    def __call__(self):
        self.progress += 1
        if self.progress % self.notify_n == 0:
            if self.last_time is None:
                self.last_time = time.time()
            else:
                now = time.time()
                self.times.append(now - self.last_time)
                self.last_time = now

            if len(self.times) > 0:
                average_execution = timedelta(milliseconds=sum(self.times) / len(self.times) * 1000)
                notify_remain = (self.n - self.progress) / self.notify_n
                remain = average_execution * notify_remain
                estimated_finish = datetime.now() + remain
                print(
                    f"Completed: {calc_percent(self.progress, self.n)} [{datetime.now().strftime('%H:%M:%S')}, {remain}, {estimated_finish.strftime('%H:%M:%S')}]")
            else:
                print(
                    f"Completed: {calc_percent(self.progress, self.n)} [timestamp: {datetime.now().strftime('%H:%M:%S')}, remain, estimated_finish]")


def apply_with_progress(df, fn):
    tracker = ProgressTracker(df.shape[0])

    def track_fn(row):
        value = fn(row)
        tracker()
        return value

    return df.apply(track_fn, axis=1)


def corr(ds, y_col):
    return abs(ds.corr()[y_col]).sort_values()


def handle_outliers(df_raw, columns, drop=False, upper_quantile=.95,
                    lower_quantile=.05, verbose=False):
    df = df_raw.copy()

    for ix, column in enumerate(columns):
        if column not in df: continue

        upper_lim = df[column].quantile(upper_quantile)
        lower_lim = df[column].quantile(lower_quantile)

        if not drop:
            df.loc[(df[column] > upper_lim), column] = upper_lim
            df.loc[(df[column] < lower_lim), column] = lower_lim
        else:
            df = df.loc[(df[column] < upper_lim) & (df[column] > lower_lim)]

        if verbose: print(f"Completed: {column}, {calc_percent(ix + 1, len(columns))}")
    return df


def transform(df_raw, columns, fn=np.log1p, verbose=False):
    df = df_raw.copy()
    for ix, column in enumerate(columns):
        if column in df:
            df[column] = df[column].transform(fn)

        if verbose: print(f"Completed: {column}, {calc_percent(ix + 1, len(columns))}")

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


def read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols):
    if ds is None:
        ds = pd.read_csv(path)

    X, y = ds.drop(y_column, axis=1), ds[y_column]
    return X[X.columns[feature_selection_support] if feature_selection_support is not None else feature_selection_cols], y
