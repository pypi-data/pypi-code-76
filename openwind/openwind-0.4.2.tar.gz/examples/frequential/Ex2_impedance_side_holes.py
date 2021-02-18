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
How to compute impedances of instrument with side holes and so several
fingerings.
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation

# %% Basic computation

# Frequencies of interest: 20Hz to 2kHz by steps of 1Hz
fs = np.arange(20, 2000, 1)
temperature = 25

# The three files describing the geometry and the
geom = 'Geom_trumpet.txt'
holes = 'Geom_holes.txt'
fing_chart = 'Fingering_chart.txt'
# Find file 'trumpet' describing the bore, and compute its impedance
result = ImpedanceComputation(fs, geom, holes, fing_chart, temperature=temperature)
result.instrument_infos()

# Plot the instrument geometry
result.plot_instrument()

# Plot the impedance
result.plot_impedance(label='Default Fingering: all open')
plt.suptitle('Default Fingering: all open')
# without indication the impedance computed correspond to the one with all holes open

# %% Chose the fingering

# it is possible to fix the fingering when the object `ImpedanceComputation`
# is created with the option `note`
result_note = ImpedanceComputation(fs, geom, holes, fing_chart,
                                   temperature=temperature, note='A')

result_note.plot_impedance(label='A')


# or to modify it after the instanciation
fig = plt.figure()
notes = result_note.get_all_notes()
for note in notes:
    result_note.set_note(note)
    result_note.plot_impedance(figure=fig, label=note)

