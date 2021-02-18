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

""" This example present how to compute sensitivities."""

import sys
sys.path.append("..")

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation
from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.inversion import InverseFrequentialResponse

# It is possible to observe the sensitivity of the observable with respect
# to any design variables for each fingering.

# We use again the problem of ex.4
frequencies = np.arange(100, 1000, 1)
temperature = 20
losses = True

# Targets definitions
geom = [[0, 0.5, 2e-3, 10e-3, 'linear']]
target_hole = [['label', 'position', 'radius', 'chimney'],
               ['hole1', .25, 3e-3, 5e-3],
               ['hole2', .35, 4e-3, 7e-3]]
fingerings = [['label', 'A', 'B', 'C', 'D'],
              ['hole1', 'x', 'x', 'o', 'o'],
              ['hole2', 'x', 'o', 'x', 'o']]
noise_ratio = 0.01
target_computation = ImpedanceComputation(frequencies, geom, target_hole,
                                          fingerings,
                                          temperature=temperature,
                                          losses=losses)
notes = target_computation.get_all_notes()
Ztargets = list()
for note in notes:
    target_computation.set_note(note)
    # normalize and noised impedance
    Ztargets.append(target_computation.impedance/target_computation.Zc
                    * (1 + noise_ratio*np.random.randn(len(frequencies))))

#  Construcion of the inverse problem
inverse_geom = [[0, '~0.5', 2e-3, '~10e-3', 'linear']]
inverse_hole = [['label', 'position', 'radius', 'chimney'],
                ['hole1', '~.25', '~3e-3', 5e-3],
                ['hole2', '~.35', '~4e-3', 7e-3]]
# The sensitivities being computed w.r. to the optimized parameters (and not
# necessary the geometric ones) it is better to chose them equal here

instru_geom = InstrumentGeometry(inverse_geom, inverse_hole, fingerings)
instru_phy = InstrumentPhysics(instru_geom, temperature, Player(), losses)
inverse = InverseFrequentialResponse(instru_phy, frequencies, Ztargets,
                                     notes=notes)

# %% Sensitivity computation
sensitivities, _ = inverse.compute_sensitivity_observable()
inverse.plot_sensitivities()

# it can be preferable to observe sensitivities for each variable type separatly
print(instru_geom.optim_params)
loc_indices = [0, 2, 4]
rad_indices = [1, 3, 5]

instru_geom.optim_params.set_active_parameters(loc_indices)
sens_loc, _ = inverse.compute_sensitivity_observable()
inverse.plot_sensitivities(logscale=True, param_order=[1, 2, 0],
                           text_on_map=False)
 # the 'param_order' option reorganizse the parameters on the plot
plt.suptitle('Sensitivities w.r. to locations')

instru_geom.optim_params.set_active_parameters(rad_indices)
sens_rad, _ = inverse.compute_sensitivity_observable()
inverse.plot_sensitivities(logscale=True, param_order=[1, 2, 0],
                           text_on_map=False)
plt.suptitle('Sensitivities w.r. to radii')

# until now all the frequency range was taking into account. It is possible to
# window it for each fingering
f_notes = 440*2**(np.array([0, 2, 3, 5])/12)
windows = [(f0, 10) for f0 in list(f_notes)]
# the first value of the tuple indicate the center of the window and the second
# the width in cents
sens_rad_wind, _ = inverse.compute_sensitivity_observable(windows=windows)
inverse.plot_sensitivities(logscale=True, param_order=[1, 2, 0],
                           text_on_map=False)
plt.suptitle('Windowed Sensitivities w.r. to radii')
















