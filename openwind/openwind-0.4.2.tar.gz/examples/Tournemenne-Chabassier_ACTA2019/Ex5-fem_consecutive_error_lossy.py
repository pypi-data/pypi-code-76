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
from openwind.continuous.physics import Physics
from openwind.frequential import FrequentialSolver

import numpy as np
import matplotlib.pyplot as plt


def l2error(z1, z2):
    return np.linalg.norm(z1.imped - z2.imped) / np.linalg.norm(z2.imped)

damping = True
ordres = np.arange(2, 13, 1)
temp = 25
params = [[1e-2, 1e-3, 45],  # cuvette d'embouchure
          [1e-1, 1e-3, 10],  # queue d'embouchure
          [1e-1, 1e-2, 1],  # leadpipe pieces
          [1, 1e-3, 1],  # conical instrument 1
          [1, 1e-2, 1],  # conical instrument 2
          5000,  # double cône discontinus
          1000,  # trompette
]

names = ["Cup", "Backbore", "Leadpipe", "ConicalIns1", "ConicalIns2",
         "discont", "Trumpet"]
subdivisions = np.hstack((np.arange(1, 20, 1), np.array([22, 26, 32, 40, 56, 82, 144])))
#subdivisions = [9, 20]
Ns = [24, 24, 24, 60, 60, 24, 72]
F1 = 20
F2 = 2000
fs = np.arange(F1, F2, 10)
print('param loaded')
physics = Physics(temp)
traceErr = []
Errors = []
player=Player()
##
for idx, param in enumerate(params):

    print(names[idx])
    if param == 1000:
        xr = np.loadtxt('Tr_co_MP')
        x = xr[:, 0].tolist()
        r = xr[:, 1].tolist()
        mk_model = InstrumentGeometry('Tr_co_MP')
    elif param == 5000:
        x = [0, 5e-2, 5e-2, 1e-1]
        r = [1e-2, 2e-2, 2.5e-2, 2.2e-2]
        mk_model = InstrumentGeometry(list(zip(x,r)))
    else:
        lgt = param[0]
        rd = param[1]
        alpha = param[2]
        x = [0, lgt]
        r = [rd, rd + lgt * np.tan(alpha * np.pi / 180)]
        if alpha == 45 and lgt == 1e-2 and rd == 1e-3:
            rinit = r[1]
            r[1] = r[0]
            r[0] = rinit
        mk_model = InstrumentGeometry(list(zip(x,r)))

    phy_model = InstrumentPhysics(mk_model, temp, player=player, losses=damping)


    N = Ns[idx]
    print("nombre d'elements requis: " + str(N))
    lEle = mk_model.get_main_bore_length() / N

    zFEM = []
    Error = np.empty(len(ordres) - 1)
    for r in ordres:

        zFEM_tmp = FrequentialSolver(phy_model, fs, compute_method='FEM', l_ele = lEle, order=r, adim=True)
        zFEM_tmp.solve()
        zFEM.append(zFEM_tmp)
        print('----------ordre: ' + str(r))
        if r > ordres[0]:
            Error[r - ordres[0]-1] = l2error(zFEM[-1], zFEM[-2])
    Errors.append(Error)

#%%
plt.figure(6)
plt.clf()
for idx, param in enumerate(params):
    plt.semilogy(ordres[:-1],Errors[idx], marker='o')
plt.ylabel(r'$\frac{\left \|  Z_{FEM}- Z_{TMM} \right \|}{\left \|  Z_{TMM} \right \|} $')
plt.xlabel('FEM order')
plt.grid()
plt.legend(names)
