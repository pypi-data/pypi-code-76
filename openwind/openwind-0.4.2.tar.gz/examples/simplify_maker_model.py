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

""" This example present a way to obtained a simplified geometry from a
complex geometry: here a simple spline from 10 conical parts"""

from openwind.technical import InstrumentGeometry, AdjustInstrumentGeometry
import numpy as np
import matplotlib.pyplot as plt

# creation of an arbitrary series of conical parts:
# it is the geometry which must be simplified
x_targ = np.linspace(0,.5,10)
r_targ = np.linspace(5e-3,1e-2,10) + 2e-3*np.sin(x_targ*2*np.pi)
Geom = np.array([x_targ, r_targ]).T.tolist()

# creation of a geometry which will be adjusted on the prevous one
geom_adjust = [[0, .5, 5e-3, '~5e-3', 'spline', '.15', '.3', '~5e-3', '~5e-3']]
# here it is only one spline, the parameters which are adjusted are preceded by '~'

# the corresponding InstrumentGeometry object are instanciated
mm_target_test = InstrumentGeometry(Geom)
mm_adjust_test = InstrumentGeometry(geom_adjust)

fig = plt.figure()
mm_target_test.plot_InstrumentGeometry(figure=fig, label='target')
mm_adjust_test.plot_InstrumentGeometry(figure=fig, label='initial', linestyle='--')

# the AdjustInstrumentGeometry is instanciated from the two maker models
test = AdjustInstrumentGeometry(mm_adjust_test, mm_target_test)
# the optimization process is carried out
adjusted = test.optimize_mkm(iter_detailed=False)
adjusted.plot_InstrumentGeometry(figure=fig, label='final', linestyle=':')
