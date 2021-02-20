#!/usr/bin/env python3
from cxwidgets.aQt import QtWidgets, QtCore
import pycx4.qcda as cda
import pyqtgraph as pg
import numpy as np
import sys

# need to think some time







app = QtWidgets.QApplication(sys.argv)

# plt = pg.plot(np.random.normal(size=100), title="Simplest possible plotting example")
# print(plt)
w = CXHistoryPlot(cname='sled1.Imes', hist_time=5000)
#w.addChan('WG4_2.Imes')

w.show()


sys.exit(app.exec_())
