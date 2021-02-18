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
How to chose the radiation impedance imposed at the open boundaries.
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation



fs = np.arange(20, 1000, 1)
temp = 25
geom = 'Geom_trumpet.txt'
holes = 'Geom_holes.txt'

fig = plt.figure()

# You can modify the model used to compute the radiation impedance by using
# the optional keyword 'radiation_category'
# In this version, this model is applied to all radiating opening: you can not
# treat separatly the holes and the "bell"

# WARNING: do not use this to open/close holes!

# %% Default
# by default the radiation category is "unflanged" corresponding to the
# radiation of a pipe with inifinite thin wall.

result = ImpedanceComputation(fs, geom, holes, temperature=temp)
result.plot_impedance(figure=fig, label='Default: unflanged')

# %% Available options
# - 'planar_piston': radiation of planar piston
# - 'unflanged': radiation of an unflanged pipe (default)
# - 'infinite_flanged': radiation of en infinite flanged pipe
# - 'pulsating_sphere': take into account the final conicity to compute the
#                       radiation of the final portion of sphere (use it with
#                       spherical waves cf. Ex6)
# - 'perfectly_open': imposed a zero pressure
# - 'total_transmission': reflection  = 0 (Zrad=Zc)
# - 'closed': perfectly close (do not use that to close hole, it close also
#    the main pipe)

rad_cats = ['planar_piston', 'unflanged', 'infinite_flanged','pulsating_sphere',
           'perfectly_open', 'total_transmission', 'closed']

for rad_cat in rad_cats:
    result = ImpedanceComputation(fs, geom, holes, temperature=temp,
                                  radiation_category=rad_cat)
    result.plot_impedance(figure=fig, label=rad_cat)

