"""Splitter module.

For more information on the underlying Qt5 object see
[QSplitter](https://doc.qt.io/qt-5/qsplitter.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget
from .mixins import OrientationMixin

__all__ = ['Splitter']

class Splitter(BaseWidget, OrientationMixin):
    """Splitter

    >>> splitter = Splitter(orientation='vertical')
    >>> splitter.append(List(["Spam", "Eggs"]))
    >>> splitter.insert(List(["Ham", "Spam"]))
    >>> for child in splitter.children:
    ...     pass
    """

    QtClass = QtWidgets.QSplitter

    def __init__(self, *children, sizes=None, orientation=None,
                 collapsible=True, stretch=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        for child in children:
            self.append(child)
        if sizes is not None:
            self.sizes = sizes
        if orientation is not None:
            self.orientation = orientation
        self.collapsible = collapsible
        if stretch is not None:
            for index, value in enumerate(stretch):
                self.qt.setStretchFactor(index, value)

    @property
    def children(self):
        children = []
        for index in range(self.qt.count()):
            children.append(self.qt.widget(index).reflection())
        return tuple(children)

    @property
    def sizes(self):
        return tuple(self.qt.sizes())

    @sizes.setter
    def sizes(self, value):
        self.qt.setSizes(list(value))

    @property
    def collapsible(self):
        return self.qt.childrenCollapsible()

    @collapsible.setter
    def collapsible(self, value):
        self.qt.setChildrenCollapsible(value)

    @property
    def handle_width(self):
        return self.qt.handleWidth()

    @handle_width.setter
    def handle_width(self, value):
        self.qt.setHandleWidth(value)

    def append(self, child):
        if not isinstance(child, BaseWidget):
            raise ValueError(child)
        self.qt.addWidget(child.qt)

    def __getitem__(self, index):
        item = self.qt.widget(index)
        if item is not None:
            return item.reflection()
        return None

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self.qt.widget(index).reflection() for index in range(len(self)))
