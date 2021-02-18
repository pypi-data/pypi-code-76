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
In this example in which two holes are optimized it is presented how to activate
desactivate design variables and how to change the targets
"""

import sys
sys.path.append("..")

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation
from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.inversion import InverseFrequentialResponse


frequencies = np.linspace(50, 500, 100)
temperature = 20
losses = True

# %% Targets definitions
# For this example we use simulated data
# The geometry is 0.5m conical part with 2 side holes.
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
                   *(1 + noise_ratio*np.random.randn(len(frequencies))))

# %% Construcion of the inverse problem

# Here we want to adjust:
# - the main bore length and conicity
# - the holes location and radius

inverse_geom = [[0, '0.05<~0.3', 2e-3, '0<~2e-3', 'linear']]
inverse_hole = [['label', 'position', 'radius', 'chimney'],
               ['hole1', '~0.1%', '~1.75e-3%', 5e-3],
               ['hole2', '~0.2%', '~1.75e-3%', 7e-3]]


instru_geom = InstrumentGeometry(inverse_geom, inverse_hole, fingerings)
print(instru_geom.optim_params)

# We can compare the two bore at the initial state
fig_geom = plt.figure()
target_computation.plot_instrument(figure=fig_geom, label='Target',
                                   color='black')
instru_geom.plot_InstrumentGeometry(figure=fig_geom, label='Initial Geometry')
fig_geom.get_axes()[0].legend()

instru_phy = InstrumentPhysics(instru_geom, temperature, Player(), losses)
inverse = InverseFrequentialResponse(instru_phy, frequencies, Ztargets,
                                     notes=notes)

# %% fix the target

# by default:
# - all the notes and target are taken into account
# - all the design variables are optimized together

# it can be smart to adjust first the main bore geometry by taking into
# account only the 'A' for which all the holes are closed
# active only the main bore design variables
instru_geom.optim_params.set_active_parameters([0, 1])
print(instru_geom.optim_params)

# Include only the 'A' and the corresponding target
inverse.set_targets_list(Ztargets[0], notes[0])

# we perform the optimization
params_evol, cost_evol = inverse.optimize_freq_model(iter_detailed=True)

# and now, the hole 2 location on 'B' for which it is the only one open hole
instru_geom.optim_params.set_active_parameters(4)
inverse.set_targets_list(Ztargets[1], notes[1])
params_evol, cost_evol = inverse.optimize_freq_model(iter_detailed=True)

# then, the hole 1 location on 'C' for which it is the only one open hole
instru_geom.optim_params.set_active_parameters(2)
inverse.set_targets_list(Ztargets[2], notes[2])
params_evol, cost_evol = inverse.optimize_freq_model(iter_detailed=True)

# %% Include everything

# We finally re-active all the design variables
instru_geom.optim_params.set_active_parameters('all')
print(instru_geom.optim_params)

# and all the notes and the target impedances
inverse.set_targets_list(Ztargets, notes)

params_evol, cost_evol = inverse.optimize_freq_model(algorithm='GN',
                                                     iter_detailed=True)
# The algorithm is fixed here to 'GN' for "Gauss-Newton" which is more robust
# than the default one 'LM' fore "Levenberg-Marquart"

instru_geom.plot_InstrumentGeometry(figure=fig_geom, label='Final Geometry',
                                    linestyle=':')
fig_geom.get_axes()[0].legend()
