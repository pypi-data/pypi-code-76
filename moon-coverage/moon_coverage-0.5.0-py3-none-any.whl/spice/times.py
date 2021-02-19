"""SPICE times module."""

import re

import numpy as np

import spiceypy as sp


def et(utc, *times):
    """Convert utc time to ephemeris time.

    Parametes
    ---------
    utc: str
        Input UTC time. All SPICE time formats are accepted.

        For example:
            - YYYY-MM-DDThh:mm:ss[.ms][Z]
            - YYYY-MON-DD hh:mm:ss

    *times: str
        Addition input UTC time(s) to parse.

    """
    if times:
        return [et(t) for t in [utc, *times]]

    if isinstance(utc, (tuple, list, np.ndarray)):
        return [et(t) for t in utc]

    return sp.utc2et(utc[:-1] if utc.endswith('Z') else utc)


def utc(et, *ets):
    """Convert ephemeris time to UTC time(s) in ISOC format.

    Parametes
    ---------
    et: str
        Input Ephemeris time.
    *ets: str
        Addition input ET time(s) to parse.

    Returns
    -------
    str or list
        Parsed time in ISOC format: ``YYYY-MM-DDThh:mm:ss.ms``

    """
    if ets:
        return [utc(t) for t in [et, *ets]]

    if isinstance(et, (tuple, list, np.ndarray)):
        return [utc(t) for t in et]

    return sp.et2utc(et, 'ISOC', 3)


STEPS = re.compile(
    r'(?P<value>\d+(?:\.\d+)?)\s?(?P<unit>millisecond|month|ms|[smhdDMyY])s?'
)


DURATIONS = {
    'ms': 0.001,
    'millisecond': 0.001,
    's': 1,
    'sec': 1,
    'm': 60,
    'h': 3_600,          # 60 x 60
    'D': 86_400,         # 60 x 60 x 24
    'd': 86_400,         # 60 x 60 x 24
    'M': 2_635_200,      # 60 x 60 x 24 x 61 // 2
    'month': 2_635_200,  # 60 x 60 x 24 x 61 // 2
    'Y': 31_536_000,     # 60 x 60 x 24 x 365
    'y': 31_536_000,     # 60 x 60 x 24 x 365
}


def parse_step(step):
    """Parse temporal step in secondes.

    The value must be a `int` or a `float`
    followed by an optional space and
    a valid unit.

    Examples of valid units:

        - ms, msec, millisecond
        - s, sec, second
        - m, min, minute
        - h, hour
        - D, day
        - M, month
        - Y, year

    Short unit version are accepted, but
    `H` and `S` are not accepted to avoid
    the confusion between `m = minute`
    and `M = month`.

    Plural units are also valid.

    Note
    ----
    Month step is based on the average month duration (30.5 days).
    No parsing of the initial date is performed.

    Parameters
    ----------
    step: str
        Step to parse.

    Returns
    -------
    int or float
        Duration step parsed in secondes

    Raises
    ------
    ValueError
        If the provided step format or unit is invalid.

    """
    match = STEPS.match(step)

    if not match:
        raise ValueError(f'Invalid step format: `{step}`')

    value, unit = match.group('value', 'unit')
    return (float(value) if '.' in value else int(value)) * DURATIONS[unit]


def et_range(start, stop, step='1s', endpoint=True):
    """Ephemeris temporal range.

    Parameters
    ----------
    start: str
        Initial start UTC time.

    stop: str
        Stop UTC time.

    step: int or str, optional
        Temporal step to apply between the start
        and stop UTC times (default: `1s`).
        If the :py:attr:`step` provided is an `int ≥ 2`
        it will correspond to the number of samples
        to generate.

    endpoint: bool, optional
        If True, :py:attr:`stop` is the last sample.
        Otherwise, it is not included (default: `True`).

    Raises
    ------
    TypeError
        If the provided step is invalid.

    """
    et_start, et_stop = et(start, stop)

    if isinstance(step, str):
        ets = np.arange(et_start, et_stop, parse_step(step))

        if endpoint and abs(ets[-1] - et_stop) > 1e-3:
            ets = np.append(ets, et_stop)

        return ets

    if isinstance(step, int) and step >= 2:
        return np.linspace(et_start, et_stop, step, endpoint=endpoint)

    raise TypeError('Step must be a `str` or a `int ≥ 2`')
