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

from openwind.technical import InstrumentGeometry
import matplotlib.pyplot as plt

""" This example shows how to add side holes to your instrument"""

# In Ex1, we have learned how to import a geometry from a file :

# my_instrument = InstrumentGeometry("Ex2_instrument.txt")

# Most wind instruments have side holes. In OpenWind, you can define your own
# side holes for your instrument.
# This can be done either directly in the code or in a independent file.

# This file must be written in an adequate format. Please refer directly to the
# example file Ex2_holes.txt or to the help page for InstrumentGeometry for more
# information.

# To add holes to your instrument, simply add the file with the holes info in
# your InstrumentGeometry. Make sure the file with the holes is second after the main
# bore geometry.

instrument_with_holes = InstrumentGeometry("Ex2_instrument.txt", "Ex2_holes.txt" )


fig1 = plt.figure(1)
instrument_with_holes.plot_InstrumentGeometry(figure=fig1)
plt.suptitle('wind instrument with side holes')

# -----------------------------------------------------------------------------

# Side holes are useful for calculating the impedance or simulating the sound
# of your instrument for a given note, i.e., fingering. For this you need to
# specify which holes are open and which are closed.
# You can add a 'fingering chart' file to your instrument to make this step
# easier.
# Please refer to the example file Ex2_fingering_chart.txt or to the help page
# for InstrumentGeometry for more information about the formatting of this file.


# Simply add the fingering chart as third file for the InstrumentGeometry :
complete_instrument = InstrumentGeometry("Ex2_instrument.txt",
                                 "Ex2_holes.txt",
                                 "Ex2_fingering_chart.txt")

# With a fingering chart, you can plot the instrument for a given note :

fig2 = plt.figure(2)
complete_instrument.plot_InstrumentGeometry(figure=fig2, note='E')
plt.suptitle('wind instrument with side holes (closed holes are filled)')


# -----------------------------------------------------------------------------
# This instrument is now fully ready to be used in simulations !
