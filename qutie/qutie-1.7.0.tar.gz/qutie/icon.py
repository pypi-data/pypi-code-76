"""Icon module.

For more information on the underlying Qt5 object see
[QIcon](https://doc.qt.io/qt-5/qicon.html).
"""

from .qutie import QtGui
from .qutie import QutieStub

from .pixmap import Pixmap

__all__ = ['Icon']

class Icon(QutieStub):
    """Icon containing multiple resolution pixmaps.

    Load multiple resoultion icons.
    >>> icon = Icon('small.png', 'large.png')

    Load icon from theme (X11 only).
    >>> icon = Icon.from_theme('document-open', Icon('fallback.png'))

    Create a color icon.
    >>> icon = Icon.from_color('red')

    Create a color icon of custom size.
    >>> icon = Icon.from_color('green', 32, 32)
    """

    QtClass = QtGui.QIcon

    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)

    @property
    def available_sizes(self):
        sizes = []
        for size in self.qt.availableSizes():
            sizes.append((size.width(), size.height()))
        return tuple(sizes)

    @property
    def name(self):
        return self.qt.name()

    @property
    def theme_name(self):
        return self.QtClass.themeName()

    def append(self, value):
        if isinstance(value, str):
            # Try to create color from string
            color = QtGui.QColor(value)
            if color.isValid():
                pixmap = Pixmap.QtClass(64, 64)
                pixmap.fill(color)
                self.qt.addPixmap(pixmap)
            else:
                self.qt.addFile(value)
        elif isinstance(value, Pixmap):
            self.qt.addPixmap(value.qt)
        else:
            raise ValueError(value)

    def pixmap(self, width, height):
        return Pixmap(qt=self.qt.pixmap(width, height))

    @classmethod
    def from_color(cls, color, width=16, height=16):
        color = QtGui.QColor(color)
        pixmap = Pixmap.QtClass(width, height)
        pixmap.fill(color)
        return Icon(qt=pixmap)

    @classmethod
    def from_theme(cls, name, fallback=None):
        args = [name]
        if fallback is not None:
            args.append(fallback)
        icon = cls.QtClass.fromTheme(*args)
        return Icon(qt=icon)
