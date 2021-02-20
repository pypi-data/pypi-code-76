from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
from cxwidgets import PCheckBox
import pycx4.qcda as cda


class CXCheckBox(PCheckBox):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.done.connect(self.cs_send)

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.IChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(bool)
    def cs_send(self, value):
        if int(value) == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        self.setValue(bool(chan.val))

    @pyqtSlot(str)
    def set_cname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def get_cname(self):
        return self._cname

    cname = pyqtProperty(str, get_cname, set_cname)



