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
Plot energy exchanges during the impulse response of a cylindrical pipe.
"""

import matplotlib.pyplot as plt
import numpy as np

from openwind import simulate, Player

#%% Run simulation: ~1 minute, depending on your CPU

# It takes more time than a simple simulation
# because it needs to calculate energy at each time step.

shape = 'simplified-trumpet'
rec = simulate(0.05,
               shape,
               player=Player("IMPULSE_400us"),
               losses='diffrepr', temperature=20,
               l_ele=0.04, order=10,
               radiation_category='closed',
               record_energy=True)

# Result is stored in rec
print(rec)



#%% Display the results


# Plot energy exchanges
plt.figure("Energy exchanges")
ax = plt.axes()

dissip_bore = np.cumsum(rec.values['bore0_Q']+rec.values['bore1_Q'])
dissip_rad = np.cumsum(rec.values['bell_radiation_Q'])
dissip_cumul = dissip_bore + dissip_rad
source_cumul = np.cumsum(-rec.values['source_Q'])
e_bore = rec.values['bore0_E']+rec.values['bore1_E']
e_additional_vars = sum(rec.values['bore'+str(i)+'_E_'+var] for i in [0,1] for var in ['P0', 'Pi', 'Vi'])
e_tot = rec.values['bell_radiation_E']+e_bore

plt.plot(rec.ts, e_bore, label='$E_h^n$ (total energy in pipe)')
plt.plot(rec.ts, e_additional_vars, '-.', label='$\mu E_{h, visc}^n + E_{h, therm}^n$')
# plt.plot(rec.ts, rec.values['bell_radiation_E'], label='$E_{radiation}$')
plt.plot(rec.ts, dissip_bore, ':', color='xkcd:grey', label='$\int Q$ (viscothermal losses)')
# plt.plot(rec.ts, dissip_rad, label='$\int Q_{radiation}$ (radiated energy)')
plt.plot(rec.ts, e_tot+dissip_cumul, label='$E_{tot} + \int Q$',
         marker='+', markevery=0.1)
plt.plot(rec.ts, source_cumul, label="$\int S$ (source)",
         linestyle='--', color='k',
         marker='x', markevery=0.11)
plt.xlabel("$t$ (s)")
plt.ylabel("Numerical energy")
plt.grid()
plt.legend()
ax.ticklabel_format(axis='y', scilimits=(0, 0))


# Plot energy deviation
ref_energy = source_cumul[-1]

plt.figure("Energy balance")
dt = rec.ts[1] - rec.ts[0]
plt.plot(rec.ts[:-1], np.diff(e_tot + dissip_cumul - source_cumul)/dt/ref_energy, '.',
         label="$(\delta E_{tot} + Q - S) / E_{max}$")
plt.xlabel("$t$ (s)")
plt.ylabel("Relative error on energy balance")
plt.legend()


#%% Discretization information

t_pipes = rec.t_solver.t_pipes
elements = sum(len(tp.mesh.elements) for tp in t_pipes)
n_dof = sum(tp.nH1 + tp.nL2 for tp in t_pipes)
element_lengths = np.concatenate([tp.mesh.get_lengths() for tp in t_pipes])
print(elements, "elements")
print("Element length is between", min(element_lengths), "and", max(element_lengths))
print(n_dof, "degrees of freedom")
