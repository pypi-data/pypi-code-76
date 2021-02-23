"""A scrollable area.

For more information on the underlying Qt5 object see
[QScrollArea](https://doc.qt.io/qt-5/qscrollarea.html).
"""

from .qutie import QtGui
from .qutie import QtWidgets

from .widget import Widget

__all__ = ['ScrollArea']

class ScrollArea(Widget):
    """A scrollable area."""

    QtClass = QtWidgets.QScrollArea

    def __init__(self, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setWidgetResizable(True)
        self.qt.setWidget(Widget().qt)
        self.qt.setBackgroundRole(QtGui.QPalette.Base) # fix background
        if layout is not None:
            self.layout = layout

    @property
    def layout(self):
        return self.qt.widget().reflection().layout

    @layout.setter
    def layout(self, value):
        if self.qt.widget():
            self.qt.widget().reflection().layout = value
