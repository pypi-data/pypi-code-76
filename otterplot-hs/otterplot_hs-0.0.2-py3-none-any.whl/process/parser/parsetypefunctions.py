# -*- coding: utf-8 -*-
r"""
This module contains functions, which help to control the type conversion of command line parsing with argparse
"""
from pathlib import Path
from typing import Type
import argparse
import numpy as np


def pathtype(s: str) -> Path:
    r"""
    converts string to pathlib.Path object

    Args:
        s(str): string, which will be converted to Path

    Returns:
        converted Path-object
    """
    return Path(s)


def collect_as_tuple() -> Type[argparse.Action]:
    r"""
    Inner class CollectAsTuple inherits from argparse.Action and implements __call__. Control the correct reading of
    four range floats for defining rectangle range. Sets the attribute dest of CollectAsTuple to the tuple, which is
    accessible through argparse. For that purpose use the argparse action key.

    Returns:
        Object of CollectAsTuple, which is of Type argparse.Action
    """

    class CollectAsTuple(argparse.Action):
        def __call__(self, parser, namespace, values, options_string=None):
            if len(values) != 4:
                raise Exception('you have to provide four numbers as range for filtering to rectangle')
            if values[0] > values[1] or values[2] > values[3]:
                raise Exception('x2/y2 have to be greater than x1/y1')
            setattr(namespace, self.dest, (values[0], values[1], values[2], values[3]))

    return CollectAsTuple


def collect_as_nparray() -> Type[argparse.Action]:
    r"""
    Inner class CollectAsTuple inherits from argparse.Action and implements __call__. Control the correct reading of
    four range floats for defining rectangle range. Sets the attribute dest of CollectAsTuple to the numpy array,
    which is accessible through argparse. For that purpose use the argparse action key.

    Returns:
        Object of CollectAsTuple, which is of Type argparse.Action
    """

    class CollectAsNP(argparse.Action):
        def __call__(self, parser, namespace, values, options_string=None):
            setattr(namespace, self.dest, np.array([value for value in values]))

    return CollectAsNP


def boolean_string(s: str) -> bool:
    r"""
    boolean string conversion in argparse. If type=bool is provided every not empty string as argumented would be casted
    to True

    Args:
        s(str): string

    Returns:
        bool
    """
    if s not in ['False', 'True']:
        raise ValueError('Not a valid boolean string')
    return s == 'True'
