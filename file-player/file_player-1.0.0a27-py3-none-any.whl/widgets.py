import logging

from PyQt5 import QtWidgets, QtCore, QtGui


class ListWidget(QtWidgets.QListWidget):
    item_dropped_signal = QtCore.pyqtSignal()

    def __init__(self, i_parent):
        super().__init__(parent=i_parent)
        self.setDragDropMode(QtWidgets.QListWidget.DragDrop)
        # -Internal*Move* isn't effected by "defaultDropAction"
        self.viewport().setAcceptDrops(True)  # <----
        self.setAcceptDrops(True)  # <----
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        # https://doc.qt.io/qt-5/qdropevent.html
        super().dropEvent(event)
        logging.debug("dropEvent")
        self.item_dropped_signal.emit()


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        # self.setPalette()
        self.setLineWidth(1)


