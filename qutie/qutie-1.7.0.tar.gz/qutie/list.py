"""Simple item based list view.

For more information on the underlying Qt5 objects see
[QListWidget](https://doc.qt.io/qt-5/qlistwidget.html) and
[QListWidgetItem](https://doc.qt.io/qt-5/qlistwidgetitem.html).
"""

from .qutie import QtCore
from .qutie import QtGui
from .qutie import QtWidgets
from .qutie import Qutie, QutieStub, Enum

from .icon import Icon
from .widget import BaseWidget

__all__ = ['List', 'ListItem']

class ViewMode(Enum):

    QtEnums = {
        'list': QtWidgets.QListView.ListMode,
        'icon': QtWidgets.QListView.IconMode
    }

class ResizeMode(Enum):

    QtEnums = {
        'fixed': QtWidgets.QListView.Fixed,
        'adjust': QtWidgets.QListView.Adjust
    }

class BaseItemView(BaseWidget):

    QtClass = QtWidgets.QAbstractItemView

    def __init__(self, *, icon_size=None, **kwargs):
        super().__init__(**kwargs)
        if icon_size is not None:
            self.icon_size = icon_size

    @property
    def icon_size(self):
        size = self.qt.iconSize()
        return size.width(), size.height()

    @icon_size.setter
    def icon_size(self, value):
        if isinstance(value, int):
            value = value, value
        self.qt.setIconSize(QtCore.QSize(*value))

class List(BaseItemView):

    QtClass = QtWidgets.QListWidget

    changed = None
    selected = None
    clicked = None
    double_clicked = None

    def __init__(self, items=None, *, view_mode=None, resize_mode=None,
                 changed=None, selected=None, clicked=None, double_clicked=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Properties
        if items is not None:
            self.extend(items)
        if view_mode is not None:
            self.view_mode = view_mode
        if resize_mode is not None:
            self.resize_mode = resize_mode
        # HACK: adjust default icons size
        if 'icon_size' not in kwargs:
            self.icon_size = 16
        # Callbacks
        self.changed = changed
        self.selected = selected
        self.clicked = clicked
        self.double_clicked = double_clicked
        # Connect signals
        def handle_current_item_changed(current, _):
            index = self.qt.row(current)
            item = self[index]
            self.emit(self.changed, item.value, index)
        self.qt.currentItemChanged.connect(handle_current_item_changed)
        def handle_current_row_changed(index):
            if index >= 0:
                value = self[index]
                self.emit(self.selected, value, index)
        self.qt.currentRowChanged[int].connect(handle_current_row_changed)
        def handle_item_clicked(item):
            data = item.data(ListItem.QtPropertyRole)
            if data is not None:
                index = self.qt.row(item)
                self.emit(self.clicked, index, data)
        self.qt.itemClicked.connect(handle_item_clicked)
        def handle_item_double_clicked(item):
            data = item.data(ListItem.QtPropertyRole)
            if data is not None:
                index = self.qt.row(item)
                self.emit(self.double_clicked, index, data)
        self.qt.itemDoubleClicked.connect(handle_item_double_clicked)

    @property
    @ViewMode.getter
    def view_mode(self):
        return self.qt.viewMode()

    @view_mode.setter
    @ViewMode.setter
    def view_mode(self, value):
        self.qt.setViewMode(value)

    @property
    @ResizeMode.getter
    def resize_mode(self):
        return self.qt.resizeMode()

    @resize_mode.setter
    @ResizeMode.setter
    def resize_mode(self, value):
        self.qt.setResizeMode(value)

    @property
    def current(self):
        item = self.qt.currentItem()
        if item:
            return item.data(ListItem.QtPropertyRole)
        return None

    @current.setter
    def current(self, item):
        index = self.qt.row(item.qt)
        if index < 0:
            raise IndexError(item)
        self.qt.setCurrentItem(item.qt)

    def append(self, item):
        """Append item to end."""
        if not isinstance(item, ListItem):
            item = ListItem(item)
        self.qt.addItem(item.qt)
        return item

    def insert(self, index: int, item) -> None:
        """Insert item before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        if not isinstance(item, ListItem):
            item = ListItem(item)
        self.qt.insertItem(index, item.qt)
        return item

    def extend(self, iterable) -> None:
        """Extend list by appending items from the iterable."""
        for item in iterable:
            self.append(item)

    def remove(self, item) -> None:
        """Remove first occurrence of value. Raises ValueError if the value is
        not present.
        """
        self.qt.takeItem(self.index(item))

    def clear(self) -> None:
        """Remove all item from widget."""
        self.qt.clear()

    def count(self, value) -> int:
        """Return number of occurrences of value."""
        return list(self).count(value)

    def index(self, item):
        """Return first index of item. Raises ValueError if the item is not
        present.
        """
        index = self.qt.row(item.qt)
        if index < 0:
            raise ValueError("value not in list")
        return index

    def scroll_to(self, item):
        self.qt.scrollToItem(item.qt)

    def __getitem__(self, key):
        item = self.qt.item(key)
        if not item:
            raise IndexError(key)
        return item.data(ListItem.QtPropertyRole)

    def __setitem__(self, key, value):
        item = ListItem(value)
        self.qt.takeItem(key)
        self.qt.insertItem(key, item.qt)

    def __delitem__(self, key):
        self.qt.takeItem(key)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[row] for row in range(len(self)))

class ListItem(QutieStub):

    QtClass = QtWidgets.QListWidgetItem

    QtPropertyRole = 0x8000

    def __init__(self, value, *, color=None, background=None, icon=None,
                 enabled=True, checked=None, checkable=False, **kwargs):
        super().__init__(**kwargs)
        self.__default_foreground = self.qt.foreground()
        self.__default_background = self.qt.background()
        self.qt.setData(self.QtPropertyRole, self)
        self.value = value
        self.color = color
        self.background = background
        if icon is not None:
            self.icon = icon
        self.enabled = enabled
        self.checkable = checkable
        self.checked = checked

    @property
    def value(self):
        return self.qt.data(QtCore.Qt.UserRole)

    @value.setter
    def value(self, value):
        self.qt.setData(QtCore.Qt.UserRole, value)
        self.qt.setText(format(value))

    @property
    def color(self):
        return self.qt.foreground().color().name()

    @color.setter
    def color(self, value):
        if value is None:
            brush = QtGui.QBrush(self.__default_foreground)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setForeground(brush)

    @property
    def background(self):
        return self.qt.background().color().name()

    @background.setter
    def background(self, value):
        if value is None:
            brush = QtGui.QBrush(self.__default_background)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setBackground(brush)

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
    def enabled(self):
        return bool(self.qt.flags() & QtCore.Qt.ItemIsEnabled)

    @enabled.setter
    def enabled(self, value):
        if value:
            self.qt.setFlags(self.qt.flags() | QtCore.Qt.ItemIsEnabled)
        else:
            self.qt.setFlags(self.qt.flags() & ~QtCore.Qt.ItemIsEnabled)

    @property
    def checked(self):
        return self.qt.checkState() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, value):
        if value is None:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
            self.qt.setFlags(flags)
        else:
            self.qt.setCheckState(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)

    @property
    def checkable(self):
        return self.qt.flags() & QtCore.Qt.ItemIsUserCheckable

    @checkable.setter
    def checkable(self, value):
        if value:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
            self.qt.setCheckState(self.checked)
        else:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
        self.qt.setFlags(flags)
