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
sys.path.append("..")
from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.frequential import FrequentialSolver

import numpy as np
import matplotlib.pyplot as plt


def l2error(z1, z2):
    return np.linalg.norm(z1.imped - z2.imped) / np.linalg.norm(z2.imped)


damping = False
F1 = 20
F2 = 2000
ordres = np.arange(1, 7, 1)
TESs = [1e-1, 5e-2, 3e-2, 2e-2, 1e-2, 5e-3, 3e-3, 2e-3, 1e-3]
fs = np.arange(F1, F2, 1)
temp = 25
print('param loaded')
##
player= Player()
mk_model = InstrumentGeometry('Tr_co_MP')
phy_model = InstrumentPhysics(mk_model, temp, player, damping)


zTMM = FrequentialSolver(phy_model, fs, compute_method='TMM', nb_sub=1)
zTMM.solve()
zFEM = []
Error = np.empty((len(TESs), len(ordres)))
for i, TES in enumerate(TESs):
    print("TES: " + str(TES))

    for j, r in enumerate(ordres):


        zFEM_tmp = FrequentialSolver(phy_model, fs, compute_method='FEM', l_ele=TES, order=r)
        zFEM_tmp.solve()
        zFEM.append(zFEM_tmp)
        print('----------ordre: ' + str(r))
        Error[i, j] = l2error(zFEM[-1], zTMM)


#%%
plt.figure(4)
plt.clf()
for i in ordres:
    plt.loglog(TESs,Error[:, i - ordres[0]])
plt.xlabel("Target element size")
plt.ylabel(r'$\frac{\left \|  Z_{FEM}- Z_{TMM} \right \|}{\left \|  Z_{TMM} \right \|} $')
plt.title("Lossless Trumpet")
plt.grid()
