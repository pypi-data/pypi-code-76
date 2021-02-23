"""Button module.

For more information on the underlying Qt5 objects see
[QPushButton](https://doc.qt.io/qt-5/qpushbutton.html),
[QToolButton](https://doc.qt.io/qt-5/qtoolbutton.html),
[QRadioButton](https://doc.qt.io/qt-5/qradiobutton.html) and
[QButtonGroup](https://doc.qt.io/qt-5/qbuttongroup.html).
"""

from .qutie import QtGui
from .qutie import QtWidgets
from .qutie import ArrowType

from .icon import Icon
from .object import Object
from .widget import Widget

__all__ = ['Button', 'PushButton', 'ToolButton', 'RadioButton', 'ButtonGroup']

class AbstractButton(Widget):
    """AbstractButton

    Properties
     - text
     - checkable
     - checked
     - icon

    Callbacks
     - clicked()
     - pressed()
     - released()
     - toggled()
    """

    QtClass = QtWidgets.QAbstractButton

    clicked = None
    pressed = None
    released = None
    toggled = None

    def __init__(self, text=None, *, checkable=None, checked=None, icon=None,
                 clicked=None, pressed=None, released=None, toggled=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Properties
        if text is not None:
            self.text = text
        if checkable is not None:
            self.checkable = checkable
        if checked is not None:
            self.checked = checked
        if icon is not None:
            self.icon = icon
        # Callbacks
        self.clicked = clicked
        self.pressed = pressed
        self.released = released
        self.toggled = toggled
        # Connect signals
        self.qt.clicked.connect(lambda: self.emit(self.clicked))
        self.qt.pressed.connect(lambda: self.emit(self.pressed))
        self.qt.released.connect(lambda: self.emit(self.released))
        self.qt.toggled.connect(lambda checked: self.emit(self.toggled, checked))

    @property
    def text(self) -> str:
        return self.qt.text()

    @text.setter
    def text(self, value: str):
        self.qt.setText(value)

    @property
    def checkable(self) -> bool:
        return self.qt.isCheckable()

    @checkable.setter
    def checkable(self, value: bool):
        self.qt.setCheckable(value)

    @property
    def checked(self) -> bool:
        return self.qt.isChecked()

    @checked.setter
    def checked(self, value: bool):
        self.qt.setChecked(value)

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

    def click(self):
        self.qt.click()

class PushButton(AbstractButton):
    """PushButton

    Properties
     - default
     - auto_default
     - flat
    """

    QtClass = QtWidgets.QPushButton

    def __init__(self, text=None, *, default=False, auto_default=False,
                 flat=None, **kwargs):
        super().__init__(text=text, **kwargs)
        # Properties
        if default is not None:
            self.default = default
        if auto_default is not None:
            self.auto_default = auto_default
        if flat is not None:
            self.flat = flat

    @property
    def default(self) -> bool:
        return self.qt.isDefault()

    @default.setter
    def default(self, value: bool):
        self.qt.setDefault(value)

    @property
    def auto_default(self) -> bool:
        return self.qt.isAutoDefault()

    @auto_default.setter
    def auto_default(self, value: bool):
        self.qt.setAutoDefault(value)

    @property
    def flat(self) -> bool:
        return self.qt.isFlat()

    @flat.setter
    def flat(self, value: bool):
        self.qt.setFlat(value)

Button = PushButton

class ToolButton(AbstractButton):
    """ToolButton

    Properties
     - arrow_type
     - auto_raise
    """

    QtClass = QtWidgets.QToolButton

    def __init__(self, text=None, *, arrow_type=None, auto_raise=None,
                 **kwargs):
        super().__init__(text=text, **kwargs)
        # Properties
        if arrow_type is not None:
            self.arrow_type = arrow_type
        if auto_raise is not None:
            self.auto_raise = auto_raise

    @property
    @ArrowType.getter
    def arrow_type(self):
        return self.qt.arrowType()

    @arrow_type.setter
    @ArrowType.setter
    def arrow_type(self, value):
        self.qt.setArrowType(value)

    @property
    def auto_raise(self):
        return self.qt.autoRaise()

    @auto_raise.setter
    def auto_raise(self, value):
        self.qt.setAutoRaise(value)

class RadioButton(AbstractButton):
    """RadioButton"""

    QtClass = QtWidgets.QRadioButton

class ButtonGroup(Object):
    """ButtonGroup

    Properties
     - exclusive
    """

    QtClass = QtWidgets.QButtonGroup

    def __init__(self, *buttons, exclusive=True, **kwargs):
        super().__init__(**kwargs)
        self.update(buttons)
        self.exclusive = exclusive

    @property
    def exclusive(self):
        return self.qt.exclusive()

    @exclusive.setter
    def exclusive(self, value):
        self.qt.setExclusive(value)

    def add(self, button):
        self.qt.addButton(button.qt)

    def remove(self, button):
        self.qt.removeButton(button.qt)

    def update(self, buttons):
        for button in buttons:
            self.add(button)

    def clear(self):
        for button in list(self):
            self.remove(button)

    def __len__(self):
        return len(self.qt.buttons())

    def __iter__(self):
        return (button.reflection for button in self.qt.buttons())
