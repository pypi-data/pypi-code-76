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
Displays the entry impedances computed with the different viscothermal models
"""
import sys
sys.path.append("..")

import numpy as np
from openwind import ImpedanceComputation, InstrumentGeometry
import matplotlib.pyplot as plt

#%% Initialize instrument

fs = np.arange(225, 265, 0.1)
temperature = 20
instrument = 'simplified-trumpet'
mm = InstrumentGeometry(instrument)

ordre = 10
lenEle = 0.04

#%% Compute impedance with different models

result_ZK = ImpedanceComputation(fs, instrument,
                                    temperature=temperature,
                                    l_ele=lenEle, order=ordre,
                                    losses=True,
                                    radiation_category='closed')

result_diffrepr = {
    N:ImpedanceComputation(fs, instrument,
                            temperature=temperature,
                            l_ele=lenEle, order=ordre,
                            losses='diffrepr'+str(N),
                            radiation_category='closed')
     for N in [2, 4, 8, 16]}


#%% Display results

fig = plt.figure()

result_ZK.plot_impedance(figure=fig, label='ZK', linestyle='-', linewidth=2, color='k')

for N, r in result_diffrepr.items():
    r.plot_impedance(figure=fig, label='N=%d'%N, linestyle='--', linewidth=np.log(N))

