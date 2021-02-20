from cxwidgets.aQt.QtWidgets import QLineEdit
from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty
import pycx4.qcda as cda


class CXLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self._cname = kwargs.get('cname', '')
        self._max_len = kwargs.get('max_len', 100)
        self.setReadOnly(bool(kwargs.get('readonly', False)))
        self.chan = None
        self.cx_connect()

    def cx_connect(self):
        if self._cname == '':
            return
        self.chan = cda.StrChan(self._cname, max_nelems=self._max_len, private=True, on_update=True)
        self.chan.valueChanged.connect(self.cs_update)

    def cs_update(self, chan):
        if self.text() != chan.val:
            self.setText(chan.val)

    @pyqtSlot(str)
    def cs_send(self, value):
        self.chan.setValue(value)

    @pyqtSlot(str)
    def set_cname(self, chan_name):
        if self._cname == chan_name:
            return
        self._cname = chan_name
        self.cx_connect()

    def get_cname(self):
        return self._cname

    def set_max_len(self, ml):
        if self._max_len == ml:
            return
        self._max_len = ml
        self.cx_connect()

    def get_max_len(self):
        return self._max_len

    cname = pyqtProperty(str, get_cname, set_cname)
    max_len = pyqtProperty(int, get_max_len, set_max_len)

