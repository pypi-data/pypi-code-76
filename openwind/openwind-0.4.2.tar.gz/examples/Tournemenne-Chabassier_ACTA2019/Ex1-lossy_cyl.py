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

import numpy as np
import matplotlib.pyplot as plt

from openwind.technical import InstrumentGeometry, Player
from openwind import ImpedanceComputation
from openwind.frequential import FrequentialSolver
from openwind.continuous import Physics, InstrumentPhysics


def l2error(z1, z2):
    return np.linalg.norm(z1.imped - z2.imped) / np.linalg.norm(z2.imped)


damping = True
F1 = 20
F2 = 2000
ordres = np.arange(2, 11, 1)
fs = np.arange(F1, F2, 1)
temp = 25
physics = Physics(temp)

x, r = [0, 2e-1], [1e-2 / 2, 1e-2 / 2]
player = Player()
mk_model = InstrumentGeometry(list(zip(x, r)))
phy_model = InstrumentPhysics(mk_model,  temp, player, damping)


lbd = physics.c(0) / F2
N = np.ceil(2 * mk_model.get_main_bore_length() / lbd)
print("nombre d'elements requis: " + str(N))

lenEle = mk_model.get_main_bore_length() / N

zTMM = FrequentialSolver(phy_model, fs, damping=damping,
                                        compute_method='TMM', nb_sub=1)
zTMM.solve()

zFEM = []
ErrorTMM = np.empty(len(ordres))
ErrorFEM = np.empty(len(ordres) - 1)

for r in ordres:
    #discret_model = DiscretizedBoreModel(phy_model, lenEle, r,
    #                                     adim=True)
    zFEM_tmp = FrequentialSolver(phy_model, fs, damping=damping,
                                compute_method='FEM', l_ele = lenEle, order = r)
    zFEM_tmp.solve()
    # print("nombre d'elements produits: " + str(discret_model.meshes[0].nb_eles))
    zFEM.append(zFEM_tmp)
    ErrorTMM[r - ordres[0]] =  l2error(zFEM[-1], zTMM)
    if r > ordres[0]:
        ErrorFEM[r - ordres[0]-1] = l2error(zFEM[-1], zFEM[-2])

#%%
plt.figure(2)
plt.clf()
plt.semilogy(ordres, ErrorTMM,color='red',marker='o')
plt.semilogy(ordres[:-1],ErrorFEM, color='k',marker='+')
plt.xlabel("Finite elements order")
plt.ylabel(r'$\frac{\left \|  Z_{FEM}- Z_{TMM} \right \|}{\left \|  Z_{TMM} \right \|} $')
plt.legend(["TMM","FEM"])
plt.title("Cyl - Lossy, N = 3")
plt.grid()
