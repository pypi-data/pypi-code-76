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

"""Simulate impulse response of a simplified trumpet and plot it."""

import matplotlib.pyplot as plt

from openwind import simulate, Player
from openwind.temporal import utils

#%% Fairly long simulation (~2 minutes)

instrument = 'simplified-trumpet'
duration = 0.2
results = dict()

for N, style in [(2, ':'), (4, '-.'), (8, '--'), (16, '-')]:
    print('\n'+'*'*50)
    print("{:^50}".format("DIFFUSIVE REPRESENTATION --- N = %d" % N))
    print('*'*50)
    rec = simulate(duration,
                   instrument,
                   player=Player("IMPULSE_400us"),
                   losses='diffrepr'+str(N),
                   radiation_category='closed',
                   temperature=20,
                   l_ele=0.04, order=10, # Discretization parameters
                   spherical_waves=False,
                   )
    results[N] = rec

#%% Display the results

fig = plt.figure()
for N, style in [(2, ':'), (4, '-.'), (8, '-'), (16, '--')]:
    rec = results[N]
    signal = rec.values['source_pressure']

    plt.subplot(2, 1, 1)
    plt.plot(rec.ts, signal, style, label='N=%d'%N)
    plt.ylabel('pressure $p(x=0, t)$ (Pa)')
    plt.legend(loc='upper right')
    # plt.ylabel('pressure $p(x=0, t)$ (Pa)')
    plt.subplot(2, 1, 2)
    plt.plot(rec.ts, signal, style)
    plt.xlabel('time (s)')
    plt.ylabel('pressure $p(x=0, t)$ (Pa)')
    plt.xlim(0.13, 0.18)
    plt.ylim(-30, 80)

fig.align_labels()
fig.tight_layout()

#%%  Export the last one
utils.export_mono('impulse.wav', signal, rec.ts)
