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

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt

from openwind import ImpedanceComputation

# Frequencies of interest: 20Hz to 2kHz by steps of 1Hz
fs = np.arange(20, 2000, 1)

fig = plt.figure("Impedance")

shape = [[0.0, 2e-3],
         [0.2, 8e-3]]

for loss_model in ['bessel',
                   'diffrepr2',
                   'diffrepr4',
                   'diffrepr6',
                   'diffrepr8',
                   'wl']:
    result = ImpedanceComputation(fs, shape, temperature=25, losses=loss_model)
    result.plot_impedance(figure=fig, label=loss_model)
