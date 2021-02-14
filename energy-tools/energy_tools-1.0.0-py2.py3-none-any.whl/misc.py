# Standard library
from math import pi
from collections.abc import Iterable

# Current module
from energy_tools.complex import EleComplex


def serie(*args):
    """Puts impedances in serie (yep, simple summation).

    Args:
        z: List of impedances (either complex or real or a combination of both).

    Returns:
        Serie impedance.
    """

    # Check if an iterable was supplied instead of multiple arguments
    if len(args) == 1 and isinstance(args[0], Iterable):
        args = args[0]

    return sum(args)


def parallel(*args):
    """Puts impedances in parallel.

    Args:
        z: List of impedances (either complex or real or a combination of both).

    Returns:
        Parallel impedance.
    """

    # Check if an iterable was supplied instead of multiple arguments
    if len(args) == 1 and isinstance(args[0], Iterable):
        args = args[0]

    try:
        return 1 / sum([1.0 / y for y in args])

    except ZeroDivisionError:
        return 0.0


def zCap(C, f=60):
    """Retourne l'impédance complexe d'un banc de condensateurs en fonction de
    la capacitance et de la fréquence (à 60Hz par défaut).
    """
    return EleComplex(1 / (2j * pi * f * C))


def zInd(L, f=60):
    """Retourne l'impédance complexe d'une inductance en fonction de
    l'inductance et de la fréquence (à 60Hz par défaut).
    """
    return EleComplex(2j * pi * f * L)
