# Built-in Modules
import os
from datetime import datetime, timedelta
from pathlib import Path

# Third Party Modules
import pandas as pd
import pytz
import numpy as np
from dotenv import load_dotenv


def get_db_client_kwargs():
    if os.environ.get('host') is None:
        __load_env()

    return {
        'dbname': os.environ.get('PGDATABASE'),
        'user': os.environ.get('PGUSER'),
        'password': os.environ.get('PGPASSWORD'),
        'host': os.environ.get('PGHOST'),
        'port': os.environ.get('PGPORT'),
    }


def __load_env():
    env_path = Path('./') / '.env'
    load_dotenv(dotenv_path=env_path)


def offset_df(df, offset=10):
    """
    :param df: Dataframe to be updated
    :param offset: Offset in milliseconds
    """
    for index, row in df.iterrows():
        dt = datetime.strptime(row["measurement_date"],
                               "%Y-%m-%d %H:%M:%S +10:00") + \
             timedelta(milliseconds=offset)
        row["measurement_date"] = "{0} {1}".format(
            dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "+10:00")


def generate_sample_df(dates, device_metrics, schema='narrow'):
    flatten = lambda l: [item for sublist in l for item in sublist]
    if schema == 'narrow':
        cardinality = len(dates) * \
                      sum([len(v) for v in device_metrics.values()])
        df_data = {
            'measurement_date': dates * int(cardinality / len(dates)),
            'device_id': flatten([[k] * len(dates) * len(v)
                                  for k, v in device_metrics.items()]),
            'device_metric_type_id': flatten([
                [item for item in val for _ in range(len(dates))]
                for val in device_metrics.values()]),
            'value': np.random.uniform(low=-10.0, high=10.0,
                                       size=(cardinality,)),
            'received_date': dates * int(cardinality / len(dates))
        }
        return pd.DataFrame(data=df_data)
    elif schema == 'json':
        cardinality = len(dates) * len(device_metrics)
        df_data = {
            'measurement_date': dates * int(cardinality / len(dates)),
            'device_id': [key for key in device_metrics.keys()
                          for _ in range(len(dates))],
            'metrics': [dict.fromkeys(
                metrics, np.random.uniform(low=-10.0, high=10.0))
                for _ in range(len(dates))
                for metrics in device_metrics.values()]
        }
        return pd.DataFrame(data=df_data)
    else:
        return None


def apply_standard_index(df):
    idx = ['device_id', 'device_metric_type_id', 'measurement_date']
    # Convert datetime columns to brisbane local time
    df.set_index(idx, inplace=True)
    # Only need the value column
    df.drop(df.columns.difference(['value']), 1, inplace=True)
    df.dropna(inplace=True)
    df.index = df.index.set_levels(
        [df.index.levels[0],
         df.index.levels[1],
         pd.to_datetime(df.index.levels[2])])
    # Have time displayed from least recent to most recent.
    # Still grouped by device_id, metric_type first
    df.sort_index(inplace=True, ascending=True)


def apply_forecast_index(df):
    idx = ['device_id', 'device_metric_type_id',
           'measurement_date', 'forecast_date']
    # Convert datetime columns to brisbane local time
    df.set_index(idx, inplace=True)
    df.dropna(inplace=True)
    df.index = df.index.set_levels(
        [df.index.levels[0],
         df.index.levels[1],
         pd.to_datetime(df.index.levels[2]),
         pd.to_datetime(df.index.levels[3])])
