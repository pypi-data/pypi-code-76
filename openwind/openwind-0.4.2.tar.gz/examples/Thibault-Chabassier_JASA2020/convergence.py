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

import numpy as np
import matplotlib.pyplot as plt

from openwind import simulate, InstrumentGeometry, Player

instrument = 'simplified-trumpet'
mm = InstrumentGeometry(instrument)

duration = 0.03

res = dict()
for n_ele in [64, 128, 256, 512, 1024, 2048]:
    print("\n", "*"*50)
    print("Simulation with n_ele =", n_ele)
    rec = simulate(duration,
                   instrument,
                   player=Player("IMPULSE_400us"),
                   losses='diffrepr4',
                   radiation_category='closed',
                   temperature=20, # Impulse response
                   l_ele=mm.get_main_bore_length()/n_ele, order=4, # Discretization parameters
                   spherical_waves=False,
                   verbosity=1,
                   )
    res[n_ele] = rec


#%% Post-processing

ts_post = np.linspace(0, duration, 200, endpoint=False)  # Times at which to compare solutions
def interp(rec):
    # Interpolate solution at times ts_post
    return np.interp(ts_post, rec.ts, rec.values['source_pressure'])

converged = interp(rec)

err = dict()

for n_ele, rec in res.items():
    signal = interp(rec)
    errsq = np.max(np.abs(signal - converged)) / np.max(np.abs(converged))
    err[n_ele] = errsq

keys = np.array(list(err.keys()))
values = np.array(list(err.values()))
plt.loglog(keys, values, 'ok', label="Largest error on impulse response")
plt.xlabel('Number of elements')
plt.ylabel(r"$\frac{\sup_{t} |p_h(x=0, t) - p(x=0, t)|}{\sup_{t} |p(x=0, t)|}$")
plt.grid('both')

# order2 = [1/n_ele**2 for n_ele in err.keys()]
#order2 = keys[2:4]**-2.0
#order2 *= values[2]/order2[0]
order2x = [keys[1], keys[2], keys[1], keys[1]]
order2y = [x**2*1e-7 for x in order2x[::-1]]
#plt.loglog(keys[2:4], order2, ':')
plt.loglog(order2x, order2y, 'k-')

plt.annotate("1", xy=(np.sqrt(order2x[0]*order2x[1]), order2y[0] * 0.9),
             horizontalalignment='center', verticalalignment='top')
plt.annotate("2 ", xy=(order2x[0], np.sqrt(order2y[0]*order2y[2])),
             horizontalalignment='right', verticalalignment='center')

plt.legend()
