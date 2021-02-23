"""Main window module.

For more information on the underlying Qt5 objects see
[QStatusBar](https://doc.qt.io/qt-5/qstatusbar.html) and
[QMainWindow](https://doc.qt.io/qt-5/qmainwindow.html).
"""

import weakref

from .qutie import QtCore
from .qutie import QtWidgets

from .action import Action
from .menu import Menu
from .menubar import MenuBar
from .toolbar import ToolBar
from .widget import BaseWidget

__all__ = ['MainWindow', 'StatusBar']

class StatusBar(BaseWidget):

    QtClass = QtWidgets.QStatusBar

    message_changed = None

    def __init__(self, *, size_grip_enabled=True, message_changed=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.size_grip_enabled = size_grip_enabled
        # Callbacks
        self.message_changed = message_changed
        # Connect signals
        def handle_message_changed(message):
            self.emit(self.message_changed, message)
        self.qt.messageChanged.connect(handle_message_changed)

    @property
    def size_grip_enabled(self) -> bool:
        return self.qt.isSizeGripEnabled()

    @size_grip_enabled.setter
    def size_grip_enabled(self, value: bool):
        self.qt.setSizeGripEnabled(value)

    @property
    def current_message(self) -> str:
        return self.qt.currentMessage()

    def show_message(self, message: str, *, timeout=0) -> None:
        self.qt.showMessage(message, timeout * 1000.)

    def clear_message(self) -> None:
        self.qt.clearMessage()

    def append(self, widget) -> None:
        self.qt.addPermanentWidget(widget.qt)

    def insert(self, index: int, widget) -> None:
        """Insert widget before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertPermanentWidget(index, widget.qt)

    def extend(self, iterable) -> None:
        """Extend list by appending values from the iterable."""
        for widget in iterable:
            self.append(widget)

    def remove(self, widget) -> None:
        self.qt.removeWidget(widget.qt)

    def index(self, widget) -> int:
        index = self.qt.layout().indexOf(widget.qt)
        if index < 0:
            raise ValueError("widget not in layout")
        return index

    def __len__(self) -> int:
        return self.qt.layout().count()

class MainWindow(BaseWidget):

    QtClass = QtWidgets.QMainWindow

    class ToolBars:

        def __init__(self, qt):
            self.__qt = qt
            self.__toolbars = set()

        def clear(self):
            for item in self.__toolbars:
                self.__qt.removeToolBar(item.qt)
            self.__toolbars.clear()

        def add(self, item):
            if isinstance(item, str):
                item = ToolBar(title=item)
            self.__qt.addToolBar(item.qt)
            self.__toolbars.add(item)
            return item

        def remove(self, item):
            if item in self.__toolbars:
                self.__qt.removeToolBar(item.qt)
                self.__toolbars.remove(item)

        def __iter__(self):
            return iter(self.__toolbars)

        def __len__(self):
            return len(self.__toolbars)

    def __init__(self, *, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setMenuBar(MenuBar().qt)
        self.qt.setStatusBar(StatusBar().qt)
        self.layout = layout
        self.qt.__toolbars = self.ToolBars(self.qt)

    @property
    def layout(self):
        widget = self.qt.centralWidget()
        if widget is not None:
            return widget.reflection()
        return None

    @layout.setter
    def layout(self, value):
        if value is None:
            self.qt.setCentralWidget(None)
        else:
            if not isinstance(value, BaseWidget):
                raise ValueError(value)
            self.qt.setCentralWidget(value.qt)

    @property
    def menubar(self):
        return self.qt.menuBar().reflection()

    @property
    def statusbar(self):
        return self.qt.statusBar().reflection()

    @property
    def toolbars(self):
        return self.qt.__toolbars
