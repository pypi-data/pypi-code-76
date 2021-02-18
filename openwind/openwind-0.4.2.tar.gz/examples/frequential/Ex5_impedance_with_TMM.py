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

""" This example present how to compute with the Transfer Matrix Method (TMM).
"""

import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation


fs = np.arange(20, 500, 1)

# %% Purely TMM

# To use the TMM it is necessary to have a geometry with conical parts only
# (or cylinders)
geom_cone = 'Geom_trumpet_conical.txt'
res_tmm_low = ImpedanceComputation(fs, geom_cone, compute_method='TMM')

fig = plt.figure()
res_tmm_low.plot_impedance(figure=fig, label='TMM')

# To improve the quality of the computation it can be necessary to subdivide
# the conical part (cf. Tournemenne and Chabassier, ACTA 2019)
res_tmm_10 = ImpedanceComputation(fs, geom_cone, compute_method='TMM', nb_sub=5)
res_tmm_10.plot_impedance(figure=fig, label='TMM subdivided 5')

res_tmm = ImpedanceComputation(fs, geom_cone, compute_method='TMM', nb_sub=40)
res_tmm.plot_impedance(figure=fig, label='TMM subdivided 40')
# %% Hybrid method

# It is also possible to use hybrid method combining TMM and FEM, for which only
# the cylinders are computed with the TMM. This has the advantage to accelerate
# the computation w.r. to purely FEM if the cylinders are long without loss of
# precision

res_hydrid = ImpedanceComputation(fs, geom_cone, compute_method='hybrid')
res_hydrid.plot_impedance(figure=fig, label='Hybrid')

# the purely fem to compare
res_fem = ImpedanceComputation(fs, geom_cone)
res_fem.plot_impedance(figure=fig, label='FEM', linestyle=':')


# this time it is possible to use a complex shape containing cylinder(s)
geom_complex = 'Geom_trumpet.txt'
res_complex_hybrid = ImpedanceComputation(fs, geom_complex, compute_method='hybrid')
fig2 = plt.figure()
res_complex_hybrid.plot_impedance(figure=fig2, label='Hybrid')

res_complex_fem = ImpedanceComputation(fs, geom_complex)
res_complex_fem.plot_impedance(figure=fig2, label='FEM', linestyle=':')

