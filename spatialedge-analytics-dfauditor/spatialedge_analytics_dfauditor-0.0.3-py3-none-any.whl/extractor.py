import logging
import dfauditor.metrics
import dfauditor.response
import pandas as pd
import numpy as np

import dfauditor.app_logger

log = dfauditor.app_logger.get(log_level=logging.INFO)

class BinConfigException(Exception):
    pass


"""
take a pandas series and extract stats according to column type
"""


# def _get_strings_array(sdf: SparkDataFrame) -> list:
#     """
#     Get an array of column names for columns that are strings in a Spark DataFrame
#     :param sdf: A Spark DataFrame
#     :return: A list of string attributes
#     """
#     attribute_list = list()
#     for elem in sdf.schema:
#         if elem.jsonValue()['type'] == 'string':
#             attribute_list.append(elem.name)
#     attribute_list = [x.lower() for x in attribute_list]
#     attribute_list.sort()
#     return attribute_list
#
#
# def _get_numbers_array(sdf: SparkDataFrame) -> list:
#     """
#     Get an array of column names for columns that are numbers in a Spark DataFrame
#     :param sdf: A Spark DataFrame
#     :return: A list of numerical attributes
#     """
#     attribute_list = list()
#     for elem in sdf.schema:
#         if elem.jsonValue()['type'] in {'byte', 'short', 'integer', 'long', 'bigint', 'float', 'double'} or elem.jsonValue()['type'].startswith('decimal'):
#             attribute_list.append(elem.name)
#     attribute_list = [x.lower() for x in attribute_list]
#     attribute_list.sort()
#     return attribute_list


def numeric(series):
    stats = dfauditor.response.Numeric()
    stats.attr = series.name
    stats.mean = series.mean()
    stats.std = series.std()
    stats.variance = series.var()
    stats.min = series.min()
    stats.max = series.max()
    stats.range = stats.max - stats.min
    stats.median, stats.iqr = dfauditor.metrics.median_iqr(series)
    stats.kurtosis = series.kurt()
    stats.skewness = series.skew()
    # todo change responses object after first order solution to contain this logic - how it computes itself
    # stats['kl_divergence'] = measures.kullback_leibler_divergence()
    # the mean absolute deviation is around the mean here
    stats.mad = series.mad()
    stats.p_zeros = float(series[series == 0].count()) / len(series.index) * 100
    stats.p_nan = float(series.isna().sum()) / len(series.index) * 100
    # todo - leave this here for __str__ of the eventual object
    # stats.p_zeros = '{0:.2f}'.format()
    # stats.p_nan = '{0:.2f}'.format()

    return stats


def string(series, head=3):
    # Only run if at least 1 non-missing value
    stats = dfauditor.response.String()
    stats.attr = series.name
    value_counts = series.value_counts(dropna=False)
    distinct = value_counts.count()
    stats.distinct = distinct
    for n, v in zip(value_counts.index[0:head], value_counts.iloc[0:head].values):
        stats.freq.append({'name': n, 'value': v})
    return stats


def bins(series, lower_bound=0, upper_bound=1, size=10):
    """
    apply binning to a domain (x)
    :param series:
    :param lower_bound: The lower boundary to use for bin size calc, default: 0.
    :param upper_bound: The upper boundary to use for bin size calc, default: 1
    :param size: number of bins
    :return:size
    """

    series_min = series.min()
    series_max = series.max()
    if lower_bound == 0 and upper_bound == 1 and (series_min < lower_bound or series_max > upper_bound):
        raise BinConfigException("The series bounds fall outside the supplied lower/upper bounds of 0 and 1")

    resp_data = dfauditor.response.Bins(size=size, lower_bound=lower_bound, upper_bound=upper_bound)
    resp_data.attr = series.name

    vc = pd.cut(series, bins=resp_data.bin_config, include_lowest=True).value_counts()
    resp_data.load(counts=vc)

    return resp_data
