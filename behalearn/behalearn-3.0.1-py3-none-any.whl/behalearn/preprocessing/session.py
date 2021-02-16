import pandas as pd


def get_session_ids(data, threshold_func, **kwargs):
    """Return a list of session IDs for each row in ``data`` such that a new ID
    is assigned to a row each time ``threshold_func`` returns ``True``.

    Parameters
    ----------
    data : iterable
        Rows to determine session IDs from according to ``threshold``.

    threshold_func : function
        Function determining if a threshold was exceeded. If the function
        returns ``True``, a new session ID is assigned to the current and
        subsequent rows.
    
    Returns
    -------
    session_ids : list
        List of identified session IDs.

    Examples
    --------
    >>> time_deltas = [10, 20, 100, 60, 200]
    >>> session_ids(time_deltas, lambda element: element > 80)
    [0, 0, 1, 1, 2]
    """
    current_session_id = 0
    session_ids = []

    for row in data:
        if threshold_func(row, **kwargs):
            current_session_id += 1

        session_ids.append(current_session_id)

    return session_ids


def timespan_exceeds_threshold(time_delta, threshold):
    """Return ``True`` if the specified time delta is greater than
    ``threshold`` or is not specified, ``False`` otherwise.

    Parameters
    ----------
    time_delta : :class:`pandas.Timedelta`
        Time delta.

    threshold : :class:`pandas.Timedelta`
        Time delta threshold.

    Returns
    -------
    result : boolean
    """
    if threshold is None:
        threshold = pd.Timedelta(0)

    return pd.isnull(time_delta) or time_delta > threshold
