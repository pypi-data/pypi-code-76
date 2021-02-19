import sys

from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSignal


# See below for sources
# https://stackoverflow.com/questions/11465971/redirecting-output-in-pyqt
class XStream(QObject):
    _stdout = None

    messageWritten = pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(str(msg))

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout


class XStreamError(QObject):
    _stderr = None

    errorWritten = pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.errorWritten.emit(str(msg))

    @staticmethod
    def stderr():
        if not XStreamError._stderr:
            XStreamError._stderr = XStreamError()
            sys.stderr = XStreamError._stderr
        return XStreamError._stderr
