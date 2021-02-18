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
from openwind.technical import InstrumentGeometry, Player
from openwind import ImpedanceComputation
from openwind.continuous.physics import Physics
import matplotlib.pyplot as plt


def l2error(z1, z2):
    return np.linalg.norm(z1.impedance - z2.impedance) / np.linalg.norm(z2.impedance)

damping = False
F1 = 20
F2 = 2000
ordres = np.arange(1, 13, 1)
fs = np.arange(F1, F2, 1)
temp = 25
print('param loaded')
##
player = Player()
mk_model = InstrumentGeometry('Tr_co_MP')
physics = Physics(temp)


zTMM = ImpedanceComputation(fs, 'Tr_co_MP', player=player, temperature=temp, losses=damping, compute_method='TMM', nb_sub=1)

lbd = physics.c(0) / F2
N = np.ceil(6 * mk_model.get_main_bore_length() / lbd)
lenEle = 2.8e-2#mk_model.ltot / N
#print("nombre d'elements requis: " + str(N))

zFEM = []
Error = np.empty(len(ordres))
for r in ordres:

    zFEM_tmp = ImpedanceComputation(fs, 'Tr_co_MP', player=player, temperature=temp, losses=damping, compute_method='FEM', l_ele = lenEle, order=r)
    zFEM_tmp.discretization_infos()
    zFEM.append(zFEM_tmp)

    Error[r - ordres[0]] = l2error(zFEM[-1], zTMM)


#%%
plt.figure(3)
plt.clf()
plt.semilogy(ordres, Error,color='k',marker='o')
plt.xlabel("Finite elements order")
plt.ylabel(r'$\frac{\left \|  Z_{FEM}- Z_{TMM} \right \|}{\left \|  Z_{TMM} \right \|} $')
plt.title("Lossless Trumpet")
plt.grid()
