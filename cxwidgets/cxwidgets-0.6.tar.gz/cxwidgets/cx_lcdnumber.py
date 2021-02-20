from cxwidgets.aQt.QtWidgets import QLCDNumber
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda


class CXLCDNumber(QLCDNumber):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        self.display(chan.val)

    @pyqtSlot(float)
    def setCname(self, cname):
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)
