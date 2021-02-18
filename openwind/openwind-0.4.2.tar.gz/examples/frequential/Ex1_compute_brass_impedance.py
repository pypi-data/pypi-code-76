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
How to easily compute impedance of instrument without tone holes.
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation

# %% Basic computation

# Frequencies of interest: 20Hz to 2kHz by steps of 1Hz
fs = np.arange(20, 2000, 1)
geom_filename = 'Geom_trumpet.txt'

# Find file 'trumpet' describing the bore, and compute its impedance
result = ImpedanceComputation(fs, geom_filename)

# Plot the instrument geometry
result.plot_instrument()

# you can get the characteristic impedance at the entrance of the instrument
# which can be useful to normalize the impedance
Zc = result.Zc

# You can plot the impedance which is automatically normalized
fig = plt.figure()
result.plot_impedance(figure=fig, label='my label')
# here the option 'figure' specify on which window plot the impedance

# %% other useful features

# you can modify the frequency axis without redoing everything
freq_bis = np.arange(20, 2000, 100)
result.set_frequencies(freq_bis)
result.plot_impedance(figure=fig, label='few frequencies', marker='o', linestyle='')
# you can use any matplotlib keyword!

# you can print the computed impedance in a file.
# It is automatically normalized by Zc
result.write_impedance('computed_impedance.txt')



