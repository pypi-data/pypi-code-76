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

from openwind.technical import InstrumentGeometry, Player
from openwind.continuous import InstrumentPhysics
from openwind.continuous.physics import Physics
from openwind.frequential import FrequentialSolver
from openwind import ImpedanceComputation
from timeit import timeit

import numpy as np
import matplotlib.pyplot as plt


def l2error(z1, z2):
    return np.linalg.norm(z1.impedance - z2.impedance) / np.linalg.norm(z2.impedance)


damping = True
F1 = 20
F2 = 2000
fs = np.arange(F1, F2, 1)
temp = 25
subdivisions = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

print('param loaded')
physics = Physics(temp)
player=Player()

# Trompette
xr = np.loadtxt('Tr_co_MP')
x = xr[:,0]
mk_model = InstrumentGeometry('Tr_co_MP')
phy_model = InstrumentPhysics(mk_model, temp, player, damping)

lbdmin = physics.c(0) / F2
lEleCvg = lbdmin / 10
ordreCvg = 14

##
print('--------- computation FEM adapt')
labels  = ['bore0', 'bore1', 'bore2', 'bore3', 'bore4', 'bore5', 'bore6', 'bore7',
 'bore8', 'bore9', 'bore10', 'bore11', 'bore12', 'bore13', 'bore14', 'bore15',
 'bore16', 'bore17', 'bore18', 'bore19', 'bore20', 'bore21', 'bore22', 'bore23',
 'bore24', 'bore25', 'bore26', 'bore27', 'bore28', 'bore29', 'bore30']

l_eles_values = list([0.002     , 0.004     , 0.004     , 0.004     , 0.00373405,
       0.06597   , 0.055     , 0.055     , 0.055     , 0.055     ,
       0.165     , 0.165     , 0.165     , 0.02      , 0.019     ,
       0.03      , 0.035     , 0.03      , 0.029     , 0.03      ,
       0.03100005, 0.03      , 0.061     , 0.03      , 0.031     ,
       0.032     , 0.03      , 0.025     , 0.036     , 0.03      ,
       0.034     , 0.029     , 0.028     ])

l_eles = dict(zip(labels, l_eles_values))
orders = dict(zip(labels, list([2, 3, 3, 3, 2, 5, 4, 4, 4, 4, 6, 6, 5, 2, 2, 2, 3, 2, 2, 2, 2, 2,
       3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 5])))

#%% erreurs

print('--------- computation FEM')
lEleClassic = lbdmin / 2
ordreCPUs = range(2, 6)  # 4 is ok for Lossy
zFEMCvg = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp, player=player, losses=damping, compute_method='FEM', l_ele = lEleCvg, order = ordreCvg)


zFEMAdapt = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp, player=player, losses=damping,  compute_method='FEM', l_ele = l_eles, order = orders)

errorFEMAdapt = l2error(zFEMAdapt, zFEMCvg)
print("error fem adapt: " + str(errorFEMAdapt))



##
zTMM = []
errorsTMM = []
for subdiv in subdivisions:
    print('-------- computation TMM ' + str(subdiv))
    zTMM_tmp =  ImpedanceComputation(fs,'Tr_co_MP', temperature=temp, player=player, losses=damping,  compute_method='TMM',  nb_sub=subdiv)
    zTMM.append(zTMM_tmp)
    errorsTMM.append(l2error(zTMM[-1], zFEMCvg))


#%% CPU times
def wrapper_FEM(lEleClassic, ordr):
    def FEM_CPU():
        zFEM = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp,player=player, losses=damping,  compute_method='FEM', l_ele = lEleClassic, order = ordr)
    return FEM_CPU

errorsFEM = []
CPUsFEM = []
for ordreCPU in ordreCPUs:
    zFEM = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp,player=player, losses=damping,  compute_method='FEM', l_ele = lEleClassic, order = ordreCPU)
    errorsFEM.append(l2error(zFEM, zFEMCvg))
    print('CPUFEM')
    repe = 5
    FEM_CPU = wrapper_FEM(lEleClassic, ordreCPU)
    CPUsFEM.append(timeit(FEM_CPU, number=repe))
    print(CPUsFEM[-1] / repe)
    print('--------------------')

##
def FEMAdapt():
    zFEM = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp,player=player, losses=damping,  compute_method='FEM', l_ele = l_eles, order = orders)

print('CPU Adapt')
zFEMadapt = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp,player=player, losses=damping,   compute_method='FEM', l_ele=l_eles,order=orders)
CPUFEMAdapt = timeit(FEMAdapt, number=repe)
print(CPUFEMAdapt / repe)
##
print(str((1 - CPUFEMAdapt / CPUsFEM[2]) * 100) + '%')
CPUFEM = CPUsFEM[2] / repe
CPUFEMAdapt = CPUFEMAdapt / repe
print('--------------------')


##
def wrapper_TMM(subdiv):
    def TMM():
        zTMM = ImpedanceComputation(fs,'Tr_co_MP', temperature=temp,player=player, losses=damping,  compute_method='TMM', nb_sub=subdiv)
    return TMM

print('CPU TMM')
CPUTMM = []
for subdiv in subdivisions:
    TMMGoodVal = wrapper_TMM(subdiv)
    CPUTMM.append(timeit(TMMGoodVal, number=repe) / repe)
print('--------------------')


#%%
plt.figure(7)
plt.clf()
plt.loglog(errorsTMM, CPUTMM, marker = '+')
plt.loglog(errorsFEM,np.array(CPUsFEM) / repe , marker = 'o')
plt.loglog(errorFEMAdapt, CPUFEMAdapt, marker = 'x')
plt.grid()
plt.xlabel("relative L2 error")
plt.ylabel('CPU time')
plt.legend(['TMM','FEM','FEM adapt'])
