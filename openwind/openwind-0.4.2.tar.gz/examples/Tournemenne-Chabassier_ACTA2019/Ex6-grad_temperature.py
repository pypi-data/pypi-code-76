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
sys.path.append("../..")

from openwind import ImpedanceComputation
from openwind.technical import InstrumentGeometry, Player
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt


damping = True #  False # True
adim = False
F1 = 20
F2 = 1200
fs =  np.arange(F1, F2, 1)
print('param loaded')
player = Player()
mk_model = InstrumentGeometry('Tr_co_MP')
r = 8
N = 82
def GradT(x):
    return 37 - (37 - 21) * x / mk_model.get_main_bore_length()

temp = np.mean(GradT(np.linspace(0, mk_model.get_main_bore_length(), 100)))
print('temperature ' + str(temp))
#phy_model = InstrumentPhysics(mk_model, temp, player, damping)


print("nombre d'elements requis: " + str(N))
lenEle = mk_model.get_main_bore_length() / N

# Mean temperature
temp = np.mean(GradT(np.linspace(0, mk_model.get_main_bore_length(), 100)))
print('Mean temperature ' + str(temp))
zFEMCst = ImpedanceComputation(fs,'Tr_co_MP',temperature=temp,losses=damping,player=player,l_ele=lenEle,order=r,nondim = True)


# Variable temperature
#physicsNonConstant = Physics(GradT)
zFEMGrad = ImpedanceComputation(fs,'Tr_co_MP',temperature=GradT,losses=damping,player=player,l_ele=lenEle,order=r,nondim = True)

#%%
fig = plt.figure(6)
plt.clf()
zFEMCst.plot_impedance(figure=fig, label='Mean')
zFEMGrad.plot_impedance(figure=fig, label='Variable')
plt.show()
