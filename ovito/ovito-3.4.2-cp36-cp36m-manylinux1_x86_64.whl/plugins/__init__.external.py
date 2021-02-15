import sys

# This is the ovito.plugins Python package. It hosts the C++ extension modules of OVITO.

# Load all the PySide2 modules first before the OVITO C++ modules get loaded.
# This ensures that the right Qt5 shared libraries get loaded when
# running in a system Python interpreter.
#
# Note: No need to load Qt5 modules that are specific to the OVITO desktop application (e.g. QtWidgets).

import PySide2
import PySide2.QtCore
import PySide2.QtGui
import PySide2.QtNetwork
import PySide2.QtXml

# Load the C++ extension module containing the OVITO bindings.
import ovito.plugins.ovito_bindings
