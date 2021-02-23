"""Base classes of all user interface objects.

For more information on the underlying Qt5 object see
[QWidget](https://doc.qt.io/qt-5/qwidget.html).
"""

from .qutie import QtCore
from .qutie import QtGui
from .qutie import QtWidgets
from .qutie import CursorShape

from .icon import Icon
from .object import Object

__all__ = ['Widget', 'BaseWidget']

class BaseWidget(Object):
    """Base widget for components without layout."""

    QtClass = QtWidgets.QWidget

    close_event = None
    focus_in = None
    focus_out = None

    def __init__(self, *, title=None, width=None, height=None, enabled=None,
                 visible=None, status_tip=None, stylesheet=None, icon=None,
                 tool_tip=None, tool_tip_duration=None, cursor=None, parent=None,
                 close_event=None, focus_in=None, focus_out=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if title is not None:
            self.title = title
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if visible is not None:
            self.visible = visible
        if enabled is not None:
            self.enabled = enabled
        if status_tip is not None:
            self.status_tip = status_tip
        if stylesheet is not None:
            self.stylesheet = stylesheet
        if icon is not None:
            self.icon = icon
        if tool_tip is not None:
            self.tool_tip = tool_tip
        if tool_tip_duration is not None:
            self.tool_tip_duration = tool_tip_duration
        if cursor is not None:
            self.cursor = cursor
        if parent is not None:
            self.parent = parent
        # Callbacks
        self.close_event = close_event
        self.focus_in = focus_in
        self.focus_out = focus_out
        # Connect signals
        self.qt.closeEvent = self.__handle_close_event
        # Custom events
        self.qt._focusInEvent = self.qt.focusInEvent
        def handle_focus_is(event):
            self.qt._focusInEvent(event)
            self.emit(self.focus_in)
        self.qt.focusInEvent = handle_focus_is
        self.qt._focusOutEvent = self.qt.focusOutEvent
        def handle_focus_out(event):
            self.qt._focusOutEvent(event)
            self.emit(self.focus_out)
        self.qt.focusOutEvent = handle_focus_out

    @property
    def title(self) -> str:
        return self.qt.windowTitle()

    @title.setter
    def title(self, value: str) -> None:
        self.qt.setWindowTitle(value)

    @property
    def width(self) -> int:
        return self.qt.width()

    @property
    def minimum_width(self) -> int:
        return self.qt.minimumWidth()

    @minimum_width.setter
    def minimum_width(self, value: int) -> None:
        self.qt.setMinimumWidth(value)

    @property
    def maximum_width(self) -> int:
        return self.qt.maximumWidth()

    @maximum_width.setter
    def maximum_width(self, value: int) -> None:
        self.qt.setMaximumWidth(value)

    @width.setter
    def width(self, value):
        if value is None:
            self.qt.setMinimumWidth(0)
            self.qt.setMaximumWidth(QtWidgets.QWIDGETSIZE_MAX)
        else:
            self.qt.setMinimumWidth(value)
            self.qt.setMaximumWidth(value)

    @property
    def height(self) -> int:
        return self.qt.height()

    @property
    def minimum_height(self) -> int:
        return self.qt.minimumHeight()

    @minimum_height.setter
    def minimum_height(self, value: int) -> None:
        self.qt.setMinimumHeight(value)

    @property
    def maximum_height(self) -> int:
        return self.qt.maximumHeight()

    @maximum_height.setter
    def maximum_height(self, value: int) -> int:
        self.qt.setMaximumHeight(value)

    @height.setter
    def height(self, value):
        if value is None:
            self.qt.setMinimumHeight(0)
            self.qt.setMaximumHeight(QtWidgets.QWIDGETSIZE_MAX)
        else:
            self.qt.setMinimumHeight(value)
            self.qt.setMaximumHeight(value)

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, value):
        self.width = value[0]
        self.height = value[1]

    @property
    def minimum_size(self):
        return self.qt.minimumWidth(), self.qt.minimumHeight()

    @minimum_size.setter
    def minimum_size(self, value):
        return self.qt.setMinimumSize(value[0], value[1])

    @property
    def maximum_size(self):
        return self.qt.maximumWidth(), self.qt.maximumHeight()

    @maximum_size.setter
    def maximum_size(self, value):
        return self.qt.setMaximumSize(value[0], value[1])

    @property
    def position(self):
        return self.qt.x(), self.qt.y()

    @property
    def minimized(self) -> bool:
        return self.qt.isMinimized()

    @minimized.setter
    def minimized(self, value: bool) -> None:
        if value:
            self.qt.showMinimized()
        else:
            self.qt.showNormal()

    @property
    def maximized(self) -> bool:
        return self.qt.isMaximized()

    @maximized.setter
    def maximized(self, value: bool) -> None:
        if value:
            self.qt.showMaximized()
        else:
            self.qt.showNormal()

    @property
    def enabled(self) -> bool:
        return self.qt.isEnabled()

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self.qt.setEnabled(value)

    @property
    def visible(self) -> bool:
        return self.qt.isVisible()

    @visible.setter
    def visible(self, value: bool) -> None:
        self.qt.setVisible(value)

    @property
    def status_tip(self) -> bool:
        return self.qt.statusTip()

    @status_tip.setter
    def status_tip(self, value: bool) -> None:
        self.qt.setStatusTip(value)

    @property
    def stylesheet(self):
        return self.qt.styleSheet()

    @stylesheet.setter
    def stylesheet(self, value):
        self.qt.setStyleSheet(value)

    @property
    def icon(self):
        icon = self.qt.windowIcon()
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setWindowIcon(QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setWindowIcon(value.qt)

    @property
    def tool_tip(self) -> str:
        return self.qt.toolTip()

    @tool_tip.setter
    def tool_tip(self, value: str) -> None:
        self.qt.setToolTip(value)

    @property
    def tool_tip_duration(self) -> float:
        """Tooltip duration in seconds. Minimum duration is 1 millisecond."""
        return self.qt.toolTipDuration() / 1000.

    @tool_tip_duration.setter
    def tool_tip_duration(self, value: float) -> None:
        self.qt.setToolTipDuration(value * 1000.)

    @property
    @CursorShape.getter
    def cursor(self):
        return self.qt.cursor().shape()

    @cursor.setter
    @CursorShape.setter
    def cursor(self, value):
        if value is None:
            self.qt.unsetCursor()
        else:
            self.qt.setCursor(value)

    @property
    def parent(self):
        parent = self.qt.parent()
        if hasattr(parent, 'reflection'):
            return parent.reflection()
        return None

    @parent.setter
    def parent(self, value):
        assert isinstance(value, BaseWidget), f"Parent must inherit from {BaseWidget}"
        self.qt.setParent(value.qt)

    def close(self) -> None:
        """Close widget, return True if widget was closed."""
        return self.qt.close()

    def show(self) -> None:
        """Show widget and all child widgets."""
        self.qt.show()

    def hide(self) -> None:
        """Hide widget and all child widgets."""
        self.qt.hide()

    def down(self) -> None:
        """Lower widget to bottom of parent widget's stack."""
        self.qt.lower()

    def up(self) -> None:
        """Raise widget to top of parent widget's stack."""
        self.qt.raise_()

    def resize(self, width: int, height: int) -> None:
        self.qt.resize(width, height)

    def move(self, x: int, y: int) -> None:
        self.qt.move(x, y)

    def __handle_close_event(self, event):
        # Overwrite slot closeEvent
        if callable(self.close_event):
            if not self.close_event():
                event.ignore()
                return
        super(type(self.qt), self.qt).closeEvent(event)

class Widget(BaseWidget):
    """Widget for components with layout."""

    QtLayoutClass = QtWidgets.QVBoxLayout

    def __init__(self, *, layout=None, modal=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setLayout(self.QtLayoutClass())
        # Properties
        if layout is not None:
            self.layout = layout
        if modal is not None:
            self.modal = modal

    @property
    def layout(self):
        layout = self.qt.layout()
        if layout is not None:
            if layout.count():
                return layout.itemAt(0).widget().reflection()
        return None

    @layout.setter
    def layout(self, value):
        while self.qt.layout().count():
            self.qt.layout().takeAt(0)
        if value is not None:
            if not isinstance(value, BaseWidget):
                raise ValueError(value)
            self.qt.layout().addWidget(value.qt)

    @property
    def modal(self):
        return self.qt.isModal()

    @modal.setter
    def modal(self, value):
        modality = QtCore.Qt.ApplicationModal if value else QtCore.Qt.NonModal
        self.qt.setWindowModality(modality)
