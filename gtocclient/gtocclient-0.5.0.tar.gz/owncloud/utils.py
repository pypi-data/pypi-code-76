# -*- coding: utf-8 -*-
#
# vim: expandtab shiftwidth=4 softtabstop=4
#
"""ownCloud util module

"""

import datetime
import os
import tempfile
import time

import six


def timedelta_to_seconds(delta):
    '''Convert a timedelta to seconds with the microseconds as fraction
    Note that this method has become largely obsolete with the
    `timedelta.total_seconds()` method introduced in Python 2.7.
    '''
    # Only convert to float if needed
    if delta.microseconds:
        total = delta.microseconds * 1e-6
    else:
        total = 0
    total += delta.seconds
    total += delta.days * 60 * 60 * 24
    return total


def format_time(timestamp, precision=datetime.timedelta(seconds=1)):
    '''Formats timedelta/datetime/seconds
    '''
    precision_seconds = precision.total_seconds()

    if isinstance(timestamp, six.string_types + six.integer_types + (float,)):
        try:
            castfunc = six.integer_types[-1]
            timestamp = datetime.timedelta(seconds=castfunc(timestamp))
        except OverflowError:  # pragma: no cover
            timestamp = None

    if isinstance(timestamp, datetime.timedelta):
        seconds = timestamp.total_seconds()
        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        return str(datetime.timedelta(seconds=seconds))
    elif isinstance(timestamp, datetime.datetime):  # pragma: no cover
        # Python 2 doesn't have the timestamp method
        if hasattr(timestamp, 'timestamp'):
            seconds = timestamp.timestamp()
        else:
            seconds = timedelta_to_seconds(timestamp - epoch)

        # Truncate the number to the given precision
        seconds = seconds - (seconds % precision_seconds)

        try:  # pragma: no cover
            if six.PY3:
                dt = datetime.datetime.fromtimestamp(seconds)
            else:
                dt = datetime.datetime.utcfromtimestamp(seconds)
        except ValueError:  # pragma: no cover
            dt = datetime.datetime.max
        return str(dt)
    elif isinstance(timestamp, datetime.date):
        return str(timestamp)
    elif timestamp is None:
        return '--:--:--'
    else:
        raise TypeError('Unknown type %s: %r' % (type(timestamp), timestamp))


def read_cache_file(cache_file_name: str, cache_validity: datetime.timedelta = datetime.timedelta(hours=8)):
    file_path = os.path.join(tempfile.gettempdir(), cache_file_name)
    if not os.path.exists(file_path):
        return None
    if datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime) + cache_validity < datetime.datetime.now():
        delete_cache_file(cache_file_name)
        return None
    with open(file_path, 'r') as fr:
        return fr.readline()


def write_cache_file(cache_file_name: str, data: str):
    file_path = os.path.join(tempfile.gettempdir(), cache_file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'w') as fw:
        fw.write(data)


def delete_cache_file(cache_file_name: str):
    file_path = os.path.join(tempfile.gettempdir(), cache_file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
