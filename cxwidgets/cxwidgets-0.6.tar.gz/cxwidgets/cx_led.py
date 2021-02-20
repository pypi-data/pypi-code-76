from cxwidgets.aQt.QtCore import pyqtProperty, pyqtSlot
import pycx4.qcda as cda
from .pledwidget import LedWidget


class CXEventLed(LedWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', None)
        self.setState(False)
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)
        self.chan.valueMeasured.connect(self.cs_update)

    def cs_update(self, chan):
        self.flashOnce()

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)


class CXStateLed(LedWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self._cname = kwargs.get('cname', '')
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True, on_update=True)
        self.chan.valueMeasured.connect(self.cs_update)

    def cs_update(self, chan):
        self.setState(bool(chan.val))

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)


