from cxwidgets.aQt.QtCore import pyqtSlot, pyqtProperty, Qt
import pycx4.qcda as cda
from .pdoublespinbox import PDoubleSpinBox


class CXDoubleSpinBox(PDoubleSpinBox):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._cname = kwargs.get('cname', None)
        self.chan = None
        self.cx_connect()
        self.done.connect(self.cs_send)

    # def contextMenuEvent(self, event):
    #     print("menu?")
    #
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         print("Left Button Clicked")
    #     elif event.button() == Qt.RightButton:
    #         print("Right Button Clicked")

    def cx_connect(self):
        if self._cname is None or self._cname == '':
            return
        self.chan = cda.DChan(self._cname, private=True)
        self.chan.valueChanged.connect(self.cs_update)

    @pyqtSlot(float)
    def cs_send(self, value):
        if self.chan is None:
            return
        if value == self.chan.val:
            return
        self.chan.setValue(value)

    def cs_update(self, chan):
        if self.value() == chan.val:
            return
        self.setValue(chan.val)

    @pyqtSlot(str)
    def setCname(self, cname):
        if self._cname == cname:
            return
        self._cname = cname
        self.cx_connect()

    def getCname(self):
        return self._cname

    cname = pyqtProperty(str, getCname, setCname)

