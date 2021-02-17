#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pybline module."""

from pkg_resources import get_distribution

from scipy import constants

# Gravity in cm/sec/sec
GRAV = constants.g / constants.centi

from . import (
    models,
    tools
)


__author__ = 'Albert Kottke'
__copyright__ = 'Copyright 2018 Albert Kottke'
__license__ = 'MIT'
__title__ = 'pybline'
__version__ = get_distribution('pybline').version

