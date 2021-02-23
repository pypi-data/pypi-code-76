"""Layout module.

For more information on the underlying Qt5 objects see
[QLayout](https://doc.qt.io/qt-5/qlayout.html),
[QBoxLayout](https://doc.qt.io/qt-5/qboxlayout.html),
[QHBoxLayout](https://doc.qt.io/qt-5/qhboxlayout.html) and
[QVBoxLayout](https://doc.qt.io/qt-5/qvboxlayout.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Column', 'Row', 'Spacer']

class Layout(BaseWidget):

    QtLayoutClass = QtWidgets.QLayout

    def __init__(self, *, spacing=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if spacing is not None:
            self.spacing = spacing

    @property
    def spacing(self) -> int:
        return self.qt.spacing()

    @spacing.setter
    def spacing(self, value: int) -> None:
        self.qt.setSpacing(int(value))

class BoxLayout(Layout):

    QtLayoutClass = QtWidgets.QBoxLayout

    def __init__(self, *widgets, stretch=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setLayout(self.QtLayoutClass())
        self.qt.layout().setContentsMargins(0, 0, 0, 0)
        self.extend(widgets)
        if stretch is not None:
            self.stretch = stretch

    @property
    def stretch(self):
        value = []
        for index in range(len(self)):
            value.append(self.qt.layout().stretch(index))
        return value

    @stretch.setter
    def stretch(self, value):
        value = list(value) + ([0] * (len(self) - len(value)))
        for index in range(len(self)):
            self.qt.layout().setStretch(index, value[index])

    def append(self, widget) -> None:
        """Append widget to end."""
        self.qt.layout().addWidget(widget.qt)

    def insert(self, index: int, widget) -> None:
        """Insert widget before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.layout().insertWidget(index, widget.qt)

    def extend(self, iterable) -> None:
        """Extend list by appending widgets from the iterable."""
        for widget in iterable:
            self.append(widget)

    def remove(self, widget):
        """Remove first occurrence of widget. Raises ValueError if the widget is
        not present.
        """
        self.qt.layout().takeAt(self.index(widget))

    def clear(self) -> None:
        """Remove all widgets from layout."""
        while len(self):
            self.remove(self[0])

    def count(self, widget) -> int:
        """Return number of occurrences of widget."""
        return list(self).count(widget)

    def index(self, widget):
        """Return first index of widget. Raises ValueError if the widget is not
        present.
        """
        index = self.qt.layout().indexOf(widget.qt)
        if index < 0:
            raise ValueError("value not in list")
        return index

    def __getitem__(self, key):
        return self.qt.layout().itemAt(key).widget().reflection()

    def __len__(self):
        return self.qt.layout().count()

    def __iter__(self):
        return (self[index] for index in range(len(self)))

class Column(BoxLayout):

    QtLayoutClass = QtWidgets.QVBoxLayout

class Row(BoxLayout):

    QtLayoutClass = QtWidgets.QHBoxLayout

class Spacer(BaseWidget):

    QtSizePolicy = {
        'fixed': QtWidgets.QSizePolicy.Fixed,
        'minimum': QtWidgets.QSizePolicy.Minimum,
        'maximum': QtWidgets.QSizePolicy.Maximum,
        'preferred': QtWidgets.QSizePolicy.Preferred,
        'expanding': QtWidgets.QSizePolicy.Expanding,
        'minimum_expanding': QtWidgets.QSizePolicy.MinimumExpanding,
        'ignored': QtWidgets.QSizePolicy.Ignored
    }

    def __init__(self, horizontal=True, vertical=True, **kwargs):
        super().__init__(**kwargs)
        self.qt.setSizePolicy(
            self.QtSizePolicy.get('expanding' if horizontal else 'fixed'),
            self.QtSizePolicy.get('expanding' if vertical else 'fixed')
        )
