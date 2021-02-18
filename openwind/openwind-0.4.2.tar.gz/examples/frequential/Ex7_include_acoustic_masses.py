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
Present the option relative to inclusion or not of acoustic masses
(discontinuity and matching volume).
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation, InstrumentGeometry

fs = np.arange(20, 2000, 1)
temp = 25
# %% Mass due to cross section discontinuity

# We chose an instrument with a cross section discontinuity
geom = 'Oboe_instrument.txt'
holes = 'Oboe_holes.txt'
fing_chart = 'Oboe_fingering_chart.txt'

instru_geom = InstrumentGeometry(geom, holes)
instru_geom.plot_InstrumentGeometry()
# there is a discontinuity at 0.45m before the "bell"

# It is possible to chose to include or not the supplementary acoustic mass
# due to this discontinuity (by default it is included)
result_with_masses = ImpedanceComputation(fs, geom, holes, fing_chart,
                                          note='C', temperature=temp,
                                          discontinuity_mass=True)

fig = plt.figure()
result_with_masses.plot_impedance(figure=fig, label='with discontinuity mass')

# or to exclude it
result_wo_masses = ImpedanceComputation(fs, geom, holes, fing_chart,
                                        note='C',temperature=temp,
                                        discontinuity_mass=False)
result_wo_masses.plot_impedance(figure=fig, label='without discontinuity mass')


# %% Matching Volume

# it is possible to include the masses due to the matching volume between the
# circular pipe of  the main bore and the circular pipe of the side hole

# by default these masses are excluded, it can be including throug the keyword
# 'matching_volume'
result_with_matching_volume = ImpedanceComputation(fs, geom, holes, fing_chart,
                                                 note='C', temperature=temp,
                                                 matching_volume=True)
result_with_matching_volume.plot_impedance(figure=fig, label='with matching volume')


