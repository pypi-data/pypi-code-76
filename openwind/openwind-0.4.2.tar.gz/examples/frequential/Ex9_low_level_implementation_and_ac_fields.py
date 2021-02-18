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
This presents low level implementation giving access to the acoustic fields
in the entire instrument.
It presents also how to interpolate data to a specific grid.
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.frequential import FrequentialSolver

fs = np.arange(20, 2000, 1) # frequencies of interest: 20Hz to 2kHz by steps of 1Hz
# Load and process the instrument geometrical file
instr_geom = InstrumentGeometry('Oboe_instrument.txt','Oboe_holes.txt')
# Create a player using the default value : unitary flow for impedance computation
player = Player()
# Choose the physics of the instrument from its geometry. Default models are chosen when they are not specified.
# Here losses = True means that Zwikker-Koster model is solved.
instr_physics = InstrumentPhysics(instr_geom, temperature=25, player = player, losses=True)

# Perform the discretisation of the pipes and put all parts together ready to be solved.
freq_model = FrequentialSolver(instr_physics, fs)
# Solve the linear system underlying the impedance computation.

# interp_grid allows to interpolate the data on a uniform grid with a given spacing.
freq_model.solve(interp=True, interp_grid=0.01)

# you need to install the module plotly and create an account on their site to
# get these 3D plots.
# They will open in a web browser.
import plotly.graph_objs as go
import plotly.offline as py

# Display the pressure for all interpolated spatial points and all frequencies.
freq_model.plot_var3D(var='pressure')
# Display the flow for all interpolated spatial points and all frequencies.
freq_model.plot_var3D(var='flow')
# now you can go to your web browser and dig in the 3D representations. 

# by default, only the main bore pipes are observed and plotted.
freq_model.solve(interp=True, interp_grid=0.01, pipes_label='main_bore')

# you can observe also a given hole by giving the right pipe label obtained in
print(instr_physics.netlist)
freq_model.solve(interp=True, interp_grid=0.001, pipes_label='hole1')
freq_model.plot_var3D(var='pressure')

# or a series of pipe labels
freq_model.solve(interp=True, interp_grid=0.001,
                     pipes_label=['bore0', 'bore1_slice0'])
freq_model.plot_var3D(var='pressure')
