"""Frame module.

For more information on the underlying Qt5 object see
[QFrame](https://doc.qt.io/qt-5/qframe.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Frame']

class Frame(BaseWidget):

    QtClass = QtWidgets.QFrame

    def __init__(self, *, line_width=None, mid_line_width=None, **kwargs):
        super().__init__(**kwargs)
        if line_width is not None:
            self.line_width = line_width
        if mid_line_width is not None:
            self.mid_line_width = mid_line_width

    @property
    def frame_width(self) -> int:
        return self.qt.frameWidth()

    @property
    def line_width(self) -> int:
        return self.qt.lineWidth()

    @line_width.setter
    def line_width(self, value: int) -> None:
        self.qt.setLineWidth(value)

    @property
    def mid_line_width(self) -> int:
        return self.qt.midLineWidth()

    @mid_line_width.setter
    def mid_line_width(self, value: int) -> None:
        self.qt.setMidLineWidth(value)
