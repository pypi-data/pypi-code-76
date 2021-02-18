#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
              "Alexis Thibault", "Tobias Van Baarsel"]
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"
"""
Slice a temperature function and change its variable
"""

def slice_temperature(temperature, pos_min, pos_max):
    """
    Extract the temperature evolution allong a portion of pipe.

    Return a temperature function which verifies

    .. math::
        y(0) = T(x_{min}) \\\\
        y(1) = T(x_{max})

    with

    - \(T(x)\) : the temperature evolution with respect to the position
    - \(x_{min}, x_{max}\) the two endpoints position of the slice.

    It is used to associate a temperature evolution for each part of the
    instrument.

    Parameters
    ----------
    temperature : float or callable
        The temperature with respect to the position.
    pos_min : float
        The minimal position used for the change of variable.
    pos_max : float
        The maximal position used for the change of variable..

    Returns
    -------
    float or callable
        The sliced temperature function.

    """
    if callable(temperature):
        slice_temp = lambda x: temperature(x*(pos_max - pos_min) + pos_min)
        return slice_temp
    else:
        return temperature
