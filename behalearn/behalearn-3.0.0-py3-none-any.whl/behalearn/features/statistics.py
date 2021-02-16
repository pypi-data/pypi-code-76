from collections import OrderedDict

import numpy as np


def abs_max(series):
    abs_values = series.dropna().abs()
    if abs_values.size != 0:
        return series[abs_values.idxmax()]
    else:
        return np.nan


def abs_min(series):
    abs_values = series.dropna().abs()
    if abs_values.size != 0:
        return series[abs_values.idxmin()]
    else:
        return np.nan


def lower_q(series):
    return series.quantile(.25)


def upper_q(series):
    return series.quantile(.75)


def iqr(series):
    return series.quantile(.75) - series.quantile(.25)


STATISTICS_MAP = OrderedDict([
    ('mean', 'mean'),
    ('std', 'std'),
    ('min', min),
    ('max', max),
    ('abs_min', abs_min),
    ('abs_max', abs_max),
    ('median', 'median'),
    ('lower_q', lower_q),
    ('upper_q', upper_q),
    ('iqr', iqr),
])

STATISTICS = tuple(STATISTICS_MAP.values())
