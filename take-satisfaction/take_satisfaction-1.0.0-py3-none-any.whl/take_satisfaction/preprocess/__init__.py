"""Pre-process given input to create the necessary data to calculate the satisfaction rate.

Methods:
____________
    * remove_manual - Checks for a manual entry row in the scale and removes it.
    * convert_scale - Converts df column answers to its satisfaction levels.
"""

__all__ = ["remove_manual",
           "convert_scale"]

from .remove_manual import remove_manual
from .scale_conversion import convert_scale
