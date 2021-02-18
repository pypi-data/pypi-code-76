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
How to fix the spatial discretization options (the mesh).
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation


# Frequencies of interest: 20Hz to 2kHz by steps of 1Hz
fs = np.arange(20, 2000, 1)
geom_filename = 'Geom_trumpet.txt'

#%% chosen fine discretisation
# choose a length for the finite elements 
length_FEM = 0.1
# choose an order for the finite elements
order_FEM = 10
# Find file 'trumpet' describing the bore, and compute its impedance with s
# pecified length and order for the finite elements
result = ImpedanceComputation(fs, geom_filename, l_ele = length_FEM, order = order_FEM)

# Plot the discretisation information
result.discretization_infos()

# Plot the impedance
fig = plt.figure()
result.plot_impedance(figure=fig, label=f"given fine discretization, nb dof = {result.get_nb_dof()}")


#%% chosen coars discretisation
# choose a length for the finite elements 
length_FEM = 0.1
# choose an order for the finite elements
order_FEM = 2
# Find file 'trumpet' describing the bore, and compute its impedance with s
# pecified length and order for the finite elements
result = ImpedanceComputation(fs, geom_filename, l_ele = length_FEM, order = order_FEM)

# Plot the discretisation information
result.discretization_infos()

# Plot the impedance
result.plot_impedance(figure=fig, label=f"given coarse discretization, nb dof = {result.get_nb_dof()}")

#%% default options
# default is an adaptative mesh that provides a reasonable solution with a 
# low computational cost
result_adapt = ImpedanceComputation(fs, geom_filename)
result_adapt.discretization_infos()
result_adapt.plot_impedance(figure=fig, label=f"adaptive discretization, nb dof = {result_adapt.get_nb_dof()}")

#%% modify the minimal order for automatic mesh
from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.frequential import FrequentialSolver
from openwind.discretization import Mesh

# Load and process the instrument geometrical file
instr_geom = InstrumentGeometry(geom_filename)
# Create a player using the default value : unitary flow for impedance computation
player = Player()
# Choose the physics of the instrument from its geometry. Default models are chosen when they are not specified. 
# Here losses = True means that Zwikker-Koster model is solved. 
instr_physics = InstrumentPhysics(instr_geom, temperature=25, player = player, losses=True)
Mesh.ORDER_MIN = 4

# Perform the discretisation of the pipes and put all parts together ready to be solved.
freq_model = FrequentialSolver(instr_physics, fs)
# Solve the linear system underlying the impedance computation.
freq_model.solve()
freq_model.discretization_infos()
freq_model.plot_impedance(figure=fig, label=f"adaptive discretization orders > 4, nb dof = {freq_model.n_tot}")


freq_model = FrequentialSolver(instr_physics, fs, order=2)
freq_model.solve()
freq_model.discretization_infos()
freq_model.plot_impedance(figure=fig, label=f"adaptive discretization orders > 4, nb dof = {freq_model.n_tot}")


