"""Group box module.

For more information on the underlying Qt5 object see
[QGroupBox](https://doc.qt.io/qt-5/qgroupbox.html).
"""

from .qutie import QtWidgets

from .widget import Widget

__all__ = ['GroupBox']

class GroupBox(Widget):

    QtClass = QtWidgets.QGroupBox

    clicked = None
    toggled = None

    def __init__(self, title=None, *, checkable=None, checked=None, flat=None,
                 clicked=None, toggled=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if title is not None:
            self.title = title
        if checkable is not None:
            self.checkable = checkable
        if checked is not None:
            self.checked = checked
        if flat is not None:
            self.flat = flat
        # Callbacks
        self.clicked = clicked
        self.toggled = toggled
        # Connect signals
        self.qt.clicked.connect(lambda _: self.emit(self.clicked))
        self.qt.toggled.connect(lambda checked: self.emit(self.toggled, checked))

    @property
    def title(self):
        return self.qt.title()

    @title.setter
    def title(self, value):
        self.qt.setTitle(value)

    @property
    def checkable(self):
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value):
        self.qt.setCheckable(value)

    @property
    def checked(self):
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value):
        self.qt.setChecked(value)

    @property
    def flat(self):
        return self.qt.isFlat()

    @flat.setter
    def flat(self, value):
        self.qt.setFlat(value)
