from pioneer.common.logging_manager import LoggingManager
from pioneer.common.gui import Product

from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot, pyqtProperty as Property, Q_ENUMS, QVariant, QObject

try:
    import leddar
except:
    LoggingManager.instance().warning("Could not import 'leddar', no live sensor can be used!")

import pprint
import traceback

class LeddarUtils(QObject):

    def __init__(self, parent = None):
        super(QObject, self).__init__(parent)

    @Slot(QVariant, result = str)
    def prettyPrint(self, d):
        return pprint.pformat(Product.cvt_if_js_value(d))

    @Slot(str, result = QVariant)
    def devices(self, type):
        try:
            if type not in ['', 'Serial', 'SpiFTDI', 'Ethernet', 'Usb']:
                raise RuntimeError(f'invalid type {type}')
            return QVariant(leddar.get_devices(type))
        except:
            print(traceback.format_exc())

