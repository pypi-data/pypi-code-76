#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plot energy exchanges during the impulse response of a cylindrical pipe.

Three plots are created:
    - pressure and flow at mouth end as functions of time,
    - amount of numerical energy stored in each part of the model
    as a function of time,
    - relative error on the energy balance at each time step.
"""
__author__ = ("Juliette Chabassier, Augustin Ernoult, Olivier Geber,"
              " Alexis Thibault, Tobias Van Baarsel")
__copyright__ = "Copyright 2020, Inria"
__credits__ = ["Juliette Chabassier", "Augustin Ernoult", "Olivier Geber",
               "Alexis Thibault", "Tobias Van Baarsel"]
__license__ = "GPL 3.0"
__version__ = "0.4.2"
__email__ = "openwind-contact@inria.fr"
__status__ = "Dev"

import matplotlib.pyplot as plt
import numpy as np

from openwind import simulate

#%% Run temporal simulation
# with record_enery = True to store energy and dissipated work
shape = [[0.0, 5e-3],
         [0.2, 5e-3]]
rec = simulate(0.02, shape, losses='diffrepr', temperature=20,
               l_ele=0.01, order=4,
               radiation_category='planar_piston',
               record_energy=True)

# Result is stored in rec
print(rec)



#%% Display the results


# Plot flow and pressure
fig = plt.figure("Signal at mouth end")
ax1 = fig.add_subplot(2, 1, 1)
ax1.plot(rec.ts, -rec.values['source_flow'], label="v(x=0)")
ax1.set_xlabel("$t$")
ax1.set_ylabel("Flow")
ax1.legend()
ax2 = fig.add_subplot(2, 1, 2, sharex=ax1)
ax2.plot(rec.ts, rec.values['source_pressure'], label="p(x=0)")
ax2.set_xlabel("$t$")
ax2.set_ylabel("Pressure")
ax2.legend()


# Plot energy exchanges
plt.figure("Energy exchanges")
dissip_bore = np.cumsum(rec.values['bore0_Q'])
dissip_rad = np.cumsum(rec.values['bell_radiation_Q'])
dissip_cumul = dissip_bore + dissip_rad
source_cumul = np.cumsum(-rec.values['source_Q'])
e_tot = rec.values['bell_radiation_E']+rec.values['bore0_E']

plt.plot(rec.ts, rec.values['bore0_E'], label='$E_{pipe}$')
plt.plot(rec.ts, rec.values['bell_radiation_E'], label='$E_{radiation}$')
plt.plot(rec.ts, dissip_bore, label='$\int Q_{bore}$ (viscothermal losses)')
plt.plot(rec.ts, dissip_rad, label='$\int Q_{radiation}$ (radiated energy)')
plt.plot(rec.ts, e_tot+dissip_cumul, label='$E_{tot} + \int Q$',
         marker='+', markevery=0.1)
plt.plot(rec.ts, source_cumul, label="$\int S$ (source)",
         marker='x', markevery=0.1)
plt.xlabel("$t$")
plt.ylabel("Numerical energy")
plt.legend()


# Plot energy balance
plt.figure("Energy balance")
dt = rec.ts[1] - rec.ts[0]
plt.plot(rec.ts[:-1], np.diff(e_tot + dissip_cumul - source_cumul)/dt, '.',
         label="$\delta E_{tot} + Q - S$")
plt.xlabel("$t$")
plt.ylabel("Error on energy balance")
plt.legend()
