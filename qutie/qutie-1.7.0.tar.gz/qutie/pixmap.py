from .qutie import QtGui
from .qutie import QutieStub

__all__ = ['Pixmap']

class Pixmap(QutieStub):

    QtClass = QtGui.QPixmap

    def __init__(self, filename=None, **kwargs):
        super().__init__(**kwargs)
        if filename is not None:
            self.load(filename)

    @property
    def width(self):
        return self.qt.width()

    @property
    def height(self):
        return self.qt.height()

    @property
    def size(self):
        return self.width, self.height

    def load(self, filename):
        """Loa pixmap from file."""
        return self.qt.load(filename)

    def save(self, filename, quality=-1):
        """Save pixmap to file."""
        return self.qt.save(filename, quality)

    def fill(self, color):
        """Fill pixmap with color."""
        self.qt.fill(QtGui.QColor(color))

    @classmethod
    def create(cls, width, height, color=None):
        """Return new pixmap instance, with optional fill color."""
        pixmap = Pixmap(qt=cls.QtClass(width, height))
        if color is not None:
            pixmap.fill(color)
        return pixmap
