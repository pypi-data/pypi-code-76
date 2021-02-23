# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""Convenience functions for the handling of time stamps.

In getML, time stamps are always expressed as a floating point value. This float
measures the number of seconds since UNIX time (January 1, 1970, 00:00:00).
Smaller units of time are expressed as fractions of a second.

To make this a bit easier to handle, this module contains simple convenience
functions that express other time units in terms of seconds."""

import numpy as np

# --------------------------------------------------------------------------


def seconds(num):
    """
    Transforms *num* into a float64.

    Args:
        num (float): The number of seconds.

    Returns:
        float: *num* as a float64.
    """
    return np.float64(num)


# --------------------------------------------------------------------------


def minutes(num):
    """
    Expresses *num* minutes in terms of seconds.

    Args:
        num (float): The number of minutes.

    Returns:
        float: *num* minutes expressed in terms of seconds.
    """
    return seconds(num) * 60.0


# --------------------------------------------------------------------------


def hours(num):
    """
    Expresses *num* hours in terms of seconds.

    Args:
        num (float): The number of hours.

    Returns:
        float: *num* hours expressed in terms of seconds.
    """
    return minutes(num) * 60.0


# --------------------------------------------------------------------------


def days(num):
    """
    Expresses *num* days in terms of seconds.

    Args:
        num(float): The number of days.

    Returns:
        float: *num* days expressed in terms of seconds.
    """
    return hours(num) * 24.0


# --------------------------------------------------------------------------


def weeks(num):
    """
    Expresses *num* weeks in terms of seconds.

    Args:
        num (float): The number of weeks.

    Returns:
        float: *num* weeks expressed in terms of seconds.
    """
    return days(num) * 7.0


# --------------------------------------------------------------------------


def milliseconds(num):
    """
    Expresses *num* milliseconds in terms of fractions of a second.

    Args:
        num (float): The number of milliseconds.

    Returns:
        float: *num* milliseconds expressed in terms of seconds.
    """
    return seconds(num) / 1000.0


# --------------------------------------------------------------------------


def microseconds(num):
    """
    Expresses *num* microseconds in terms of fractions of a second.

    Args:
        num (float): The number of microseconds.

    Returns:
        float: *num* microseconds expressed in terms of seconds.
    """
    return milliseconds(num) / 1000.0


# --------------------------------------------------------------------------

__all__ = (
    "seconds",
    "minutes",
    "hours",
    "days",
    "weeks",
    "milliseconds",
    "microseconds",
)
