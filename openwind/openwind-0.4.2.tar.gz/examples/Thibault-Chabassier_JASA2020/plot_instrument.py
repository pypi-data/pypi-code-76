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
Plot the instrument
"""
import matplotlib.pyplot as plt

from openwind import InstrumentGeometry

mm = InstrumentGeometry('simplified-trumpet')
fig = plt.figure()
mm.plot_InstrumentGeometry(figure=fig, color='k')
ax, = fig.get_axes()
ax.axis('auto')
ax.set_ylim(0, 7e-2)
ax.vlines(0.0, 0.0, 6e-3, linestyle='--', color='gray')
ax.vlines(0.716, 0.0, 6e-3, linestyle='--', color='gray');
ax.vlines(1.335, 0.0, 6e-2, linestyle='--', color='gray');

