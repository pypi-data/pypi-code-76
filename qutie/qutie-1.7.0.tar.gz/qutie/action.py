"""Action module.

For more information on the underlying Qt5 object see
[QAction](https://doc.qt.io/qt-5/qaction.html).
"""

from .qutie import QtGui
from .qutie import QtWidgets

from .object import Object
from .icon import Icon

__all__ = ['Action']

class Action(Object):
    """
    Properties
     - text
     - checkable
     - checked
     - tool_tip
     - status_tip
     - shortcut
     - icon
     - separator

    Callbacks
     - changed()
     - hovered()
     - toggled(checked)
     - triggered()
    """

    QtClass = QtWidgets.QAction

    changed = None
    hovered = None
    toggled = None
    triggered = None

    def __init__(self, text=None, *, checkable=None, checked=False, tool_tip=None,
                 status_tip=None, shortcut=None, icon=None, separator=None,
                 changed=None, hovered=None, toggled=None, triggered=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Create separator from text
        if isinstance(text, str) and text.startswith("---"):
            text = None
            separator = True
        # Properties
        if text is not None:
            self.text = text
        if checkable is not None:
            self.checkable = checkable
        self.checked = checked
        if tool_tip is not None:
            self.tool_tip = tool_tip
        if status_tip is not None:
            self.status_tip = status_tip
        if shortcut is not None:
            self.shortcut = shortcut
        if icon is not None:
            self.icon = icon
        if separator is not None:
            self.separator = separator
        # Callbacks
        self.changed = changed
        self.hovered = hovered
        self.toggled = toggled
        self.triggered = triggered
        # Connect signals
        self.qt.changed.connect(lambda: self.emit(self.changed))
        self.qt.hovered.connect(lambda: self.emit(self.hovered))
        self.qt.toggled.connect(lambda checked: self.emit(self.toggled, checked))
        self.qt.triggered.connect(lambda: self.emit(self.triggered))

    @property
    def text(self) -> str:
        return self.qt.text()

    @text.setter
    def text(self, value: str):
        self.qt.setText(value)

    @property
    def checked(self) -> bool:
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value: bool):
        self.qt.setChecked(value)

    @property
    def checkable(self) -> bool:
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value: bool):
        self.qt.setCheckable(value)

    @property
    def tool_tip(self) -> str:
        return self.qt.toolTip()

    @tool_tip.setter
    def tool_tip(self, value: str):
        self.qt.setToolTip(value)

    @property
    def status_tip(self) -> str:
        return self.qt.statusTip()

    @status_tip.setter
    def status_tip(self, value: str):
        self.qt.setStatusTip(value)

    @property
    def shortcut(self):
        return self.qt.shortcut().toString() or None

    @shortcut.setter
    def shortcut(self, value):
        if value is None:
            self.qt.setShortcut(QtGui.QKeySequence())
        else:
            self.qt.setShortcut(QtGui.QKeySequence(value))

    @property
    def icon(self):
        icon = self.qt.icon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setIcon(value.qt)

    @property
    def separator(self):
        return self.qt.isSeparator()

    @separator.setter
    def separator(self, value):
        self.qt.setSeparator(value)

    def trigger(self):
        self.qt.trigger()

    def toggle(self):
        self.qt.toggle()
