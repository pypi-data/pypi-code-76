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
How to fix the temperature.
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation

fs = np.arange(20, 2000, 1)
geom = 'Geom_trumpet.txt'
holes = 'Geom_holes.txt'
# %% Default computation

# by default the temperature is 25°C
result = ImpedanceComputation(fs, geom, holes)
result.plot_instrument()

fig = plt.figure()
result.plot_impedance(figure=fig, label='Default Temp.: 25°C')

# %% if you want you can also fix a uniform temperature
result_30 = ImpedanceComputation(fs, geom, holes, temperature=30)
result_30.plot_impedance(figure=fig, label='30°C')

# %% you can also apply a variable temperature by defining a function

# In this case, the temperature variation is along the main axes.
# In the holes the temperature is uniform and equals the one in the main bore
# at their location.
total_length = result.get_bore().get_main_bore_length()
def grad_temp(x):
    T0 = 37
    T1 = 21
    return 37 + x*(T1 - T0)/total_length
result_var = ImpedanceComputation(fs, geom, holes, temperature=grad_temp)
result_var.plot_impedance(figure=fig, label='Variable Temp.')





