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
How to compute with spherical wave front and compare to T.Helie study [1].
# --------------------------------------------------------------------------
# [1] Hélie, T., Hézard, T., Mignot, R., & Matignon, D. (2013).
# One-dimensional acoustic models of horns and comparison with measurements.
# Acta acustica united with Acustica, 99(6), 960-974.
# --------------------------------------------------------------------------

"""


import sys
sys.path.append("..") # ensure openwind is in the PYTHONPATH

import numpy as np
import matplotlib.pyplot as plt
from openwind import ImpedanceComputation


# %% Compare impedance computation for trumpet using planar waves
# or spherical waves

fs = np.arange(20, 2000, 1)

# Run ImpedanceComputation will automatically choose planar waves in the pipe
result_planar = ImpedanceComputation(fs, 'Geom_trumpet.txt', temperature=25)
# Use the option spherical_waves=True to force sphericity
result_sph = ImpedanceComputation(fs, 'Geom_trumpet.txt', temperature=25,
                                 spherical_waves=True)

# Display infos about the automatic adaptative discretization
result_planar.discretization_infos()

# Plot the impedances on the same figure
fig = plt.figure()
result_planar.plot_impedance(figure=fig, label='plane')
result_sph.plot_impedance(figure=fig, label='spherical')


# %% Compare impedance computation for trombone using planar waves
# or spherical waves

file = 'Geom_trombone_Helie.txt'

fs = np.arange(20, 2000, 1)

fig = plt.figure()

# We will store the computed impdances inside a dictionnary
results = dict()

for color, spherical in [('r', True),
                         ('b', False)
                         ]:
    # uncomment some radiation options if you want to test them
    for linestyle, rad in [#('--', 'unflanged'),
                           #('-', 'infinite_flanged'),
                           (':', 'pulsating_sphere')]:
        # uncomment some losses options if you want to test them
        for marker, losses in [#('x', False), ('o', 'bessel'),
                (None,'wl')]:
            result = ImpedanceComputation(fs, file, temperature=25.5,
                                            spherical_waves=spherical,
                                            radiation_category=rad,
                                            losses=losses)
            label = f'sph={spherical}; rad={rad}; losses={losses}'
            result.plot_impedance(figure=fig, label=label, color=color, marker=marker, linestyle=linestyle, markevery=200)
            results[label] = result

# A graph show you all the computed impedances along with their modelling
# options. The effect of spherical waves is major in this trombone. 

#%% Compare resonance and anti-resonance frequencies to measurements from [1]
rf_measured = [241.4, 517.2, 793.0, np.nan, 1484.2, 1779.6]
arf_measured = [368.3, 667.5, np.nan, 1347.2, 1615.2, 1905.1]

for name, result in results.items():
    rf = result.resonance_frequencies(6)
    arf = result.antiresonance_frequencies(6)
    error_percent = 100*(rf-rf_measured)/rf_measured
    error_percent2 = 100*(arf-arf_measured)/arf_measured
    data = ['\n      resonances'] + \
        [f'{v:7.1f} ({e:+4.1f})' for v,e in zip(rf, error_percent)] + \
        ['\n  antiresonances'] + \
        [f'{v:7.1f} ({e:+4.1f})' for v,e in zip(arf, error_percent2)]
    data = '    '.join(data)
    print(f'{name} : {data}')

