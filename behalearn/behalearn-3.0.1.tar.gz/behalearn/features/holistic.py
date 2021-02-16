import numpy as np

from behalearn.config import config


def distance(data, columns):
    """Calculate the end-to-end distance from data containing point
    coordinates.
    
    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Data containing point coordinates in each row.
    
    Returns
    -------
    distance : float
        Distance of the first and the last point in ``data``. If ``data`` is
        empty, 0 is returned.
    """
    if data.shape[0] <= 1:
        return 0

    try:
        cols = data.loc[:, columns]
    except KeyError:
        return 0

    return np.linalg.norm(cols.iloc[0].values - cols.iloc[-1].values)


def length(data, columns):
    """Calculate the trajectory length from data containing point coordinates.
    
    The length is calculated as a sum of Euclidean distances of consecutive
    points.
    
    Parameters
    ----------
    data : :class:`pandas.DataFrame`
        Data containing point coordinates in each row.
    
    Returns
    -------
    length : float
        Trajectory length from the first to the last point in ``data``.
    """
    try:
        cols = data.loc[:, columns]
    except KeyError:
        return 0

    return np.sum(np.linalg.norm(np.diff(cols, axis=0), axis=1))


def duration(data, column=config['field_timestamp']):
    return data.iloc[-1][column] - data.iloc[0][column]


def start(data, columns):
    return data.iloc[0][columns]


def end(data, columns):
    return data.iloc[-1][columns]
