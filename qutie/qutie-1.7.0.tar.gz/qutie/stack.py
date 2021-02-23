"""Stack module.

For more information on the underlying Qt5 object see
[QStackedWidget](https://doc.qt.io/qt-5/qstackedwidget.html).
"""

from .qutie import QtCore
from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Stack']

class Stack(BaseWidget):

    QtClass = QtWidgets.QStackedWidget

    changed = None
    removed = None

    def __init__(self, *items, changed=None, removed=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        for item in items:
            self.append(item)
        # Callbacks
        self.changed = changed
        self.removed = removed
        # Connect signals
        self.qt.currentChanged.connect(lambda index: self.emit(self.changed, index))
        self.qt.widgetRemoved.connect(lambda index: self.emit(self.removed, index))

    def append(self, item) -> None:
        self.qt.addWidget(item.qt)

    def insert(self, index: int, item) -> None:
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertWidget(index, item.qt)

    def extend(self, iterable) -> None:
        """Extend list by appending values from the iterable."""
        for item in iterable:
            self.append(item)

    def remove(self, item):
        self.index(item)
        self.qt.removeWidget(item.qt)

    def clear(self):
        while len(self):
            self.remove(self[0])

    @property
    def current(self):
        index = self.qt.currentIndex()
        if index < 0:
            return None
        return self[index]

    @current.setter
    def current(self, item):
        self.qt.setCurrentIndex(self.index(item))

    def index(self, item) -> int:
        index = self.qt.indexOf(item.qt)
        if index < 0:
            raise ValueError("item not in stack")
        return index

    def __getitem__(self, key):
        item = self.qt.widget(key)
        if not item:
            raise KeyError(key)
        return item.reflection()

    def __setitem__(self, key, value):
        del self[key]
        self.insert(key, value)

    def __delitem__(self, key):
        item = self[key]
        self.qt.removeWidget(item)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[index] for index in range(len(self)))
