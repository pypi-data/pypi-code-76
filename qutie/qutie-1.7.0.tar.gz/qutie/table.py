"""Simple item based table view.

For more information on the underlying Qt5 objects see
[QTableWidget](https://doc.qt.io/qt-5/qtablewidget.html) and
[QTableWidgetItem](https://doc.qt.io/qt-5/qtablewidgetitem.html).
"""

from .qutie import QtCore
from .qutie import QtGui
from .qutie import QtWidgets
from .qutie import Qutie, QutieStub

from .icon import Icon
from .list import BaseItemView

__all__ = ['Table', 'TableItem']

class Table(BaseItemView):
    """Table widget.

    >>> table = Table(header=["Key", "Value"])
    >>> table.append(["Spam", "Eggs"])
    >>> table.insert(0, ["Ham", "Spam"])
    >>> for row in table:
    ...     for item in row:
    ...         item.color = "blue"
    >>> table.clear()
    """

    QtClass = QtWidgets.QTableWidget

    activated = None
    changed = None
    clicked = None
    double_clicked = None
    selected = None

    def __init__(self, rows=None, *, header=None, stretch=True, sortable=False,
                 vertical_header=False, activated=None, changed=None,
                 clicked=None, double_clicked=None, selected=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.horizontalHeader().setHighlightSections(False)
        self.qt.verticalHeader().setHighlightSections(False)
        # Properties
        self.header = header or []
        for row in rows or []:
            self.append(row)
        self.stretch = stretch
        self.sortable = sortable
        self.vertical_header = vertical_header
        self.selection_mode = 'single'
        self.selection_behavior = 'rows'
        # Callbacks
        self.activated = activated
        self.changed = changed
        self.clicked = clicked
        self.double_clicked = double_clicked
        self.selected = selected
        # Connect signals
        def handle_item_activated(item):
            if callable(self.activated):
                data = item.data(item.UserType)
                if data is not None:
                    self.emit(self.activated, data)
        self.qt.itemActivated.connect(handle_item_activated)
        def handle_item_changed(item):
            if callable(self.changed):
                data = item.data(item.UserType)
                if data is not None:
                    self.emit(self.changed, data)
        self.qt.itemChanged.connect(handle_item_changed)
        def handle_item_clicked(item):
            if callable(self.clicked):
                data = item.data(item.UserType)
                if data is not None:
                    self.emit(self.clicked, data)
        self.qt.itemClicked.connect(handle_item_clicked)
        def handle_item_double_clicked(item):
            if callable(self.double_clicked):
                data = item.data(item.UserType)
                if data is not None:
                    self.emit(self.double_clicked, data)
        self.qt.itemDoubleClicked.connect(handle_item_double_clicked)
        def handle_item_selected():
            if callable(self.selected):
                data = self.qt.selectedItems()
                if data:
                    first = data[0].data(data[0].UserType)
                    self.emit(self.selected, first)
        self.qt.itemSelectionChanged.connect(handle_item_selected)

    @property
    def header(self):
        """Horizontal header labels.

        >>> table.header = 'Key', 'Value'
        >>> table.header
        ('Key', 'Value')
        """
        return tuple([self.qt.horizontalHeaderItem(index).text() for index in range(self.qt.columnCount())])

    @header.setter
    def header(self, value):
        self.qt.setColumnCount(len(value))
        self.qt.setHorizontalHeaderLabels(value)

    @property
    def vertical_header(self):
        return self.qt.verticalHeader().visible()

    @vertical_header.setter
    def vertical_header(self, value):
        self.qt.verticalHeader().setVisible(value)

    @property
    def sortable(self):
        return self.qt.isSortingEnabled()

    @sortable.setter
    def sortable(self, value):
        self.qt.setSortingEnabled(value)

    @property
    def selection_behavior(self):
        return {
            QtWidgets.QAbstractItemView.SelectItems: 'items',
            QtWidgets.QAbstractItemView.SelectRows: 'rows',
            QtWidgets.QAbstractItemView.SelectColumns: 'columns'
        }[self.qt.selectionBehavior()]

    @selection_behavior.setter
    def selection_behavior(self, value):
        self.qt.setSelectionBehavior({
            'items': QtWidgets.QAbstractItemView.SelectItems,
            'rows': QtWidgets.QAbstractItemView.SelectRows,
            'columns': QtWidgets.QAbstractItemView.SelectColumns
        }[value])

    @property
    def selection_mode(self):
        return {
            QtWidgets.QAbstractItemView.SingleSelection: 'single',
            QtWidgets.QAbstractItemView.ContiguousSelection: 'contiguous',
            QtWidgets.QAbstractItemView.ExtendedSelection: 'extended',
            QtWidgets.QAbstractItemView.MultiSelection: 'multi',
            QtWidgets.QAbstractItemView.NoSelection: 'no'
        }[self.qt.selectionMode()]

    @selection_mode.setter
    def selection_mode(self, value):
        self.qt.setSelectionMode({
            'single': QtWidgets.QAbstractItemView.SingleSelection,
            'contiguous': QtWidgets.QAbstractItemView.ContiguousSelection,
            'extended': QtWidgets.QAbstractItemView.ExtendedSelection,
            'multi': QtWidgets.QAbstractItemView.MultiSelection,
            'no': QtWidgets.QAbstractItemView.NoSelection
        }[value])

    @property
    def row_count(self):
        """Return row count."""
        return self.qt.rowCount()

    @property
    def column_count(self):
        """Return column count."""
        return self.qt.columnCount()

    def row(self, item):
        """Return item row."""
        return self.qt.row(item.qt)

    def column(self, item):
        """Return item column."""
        return self.qt.column(item.qt)

    def append(self, items):
        """Append items, returns appended items.

        >>> table.append([TableItem(value="Spam"), TableItem(value="Eggs")])
        or
        >>> table.append(["Spam", "Eggs"])
        """
        row = self.row_count
        return self.insert(row, items)

    def insert(self, row: int, items):
        """Insert items at row, returns inserted items.

        >>> table.insert(0, [TableItem(value="Spam"), TableItem(value="Eggs")])
        or
        >>> table.insert(0, ["Spam", "Eggs"])
        """
        self.qt.insertRow(row)
        for column, item in enumerate(items):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(row, column, item.qt)
            self.qt.resizeRowToContents(row)
        return self[row]

    def remove_row(self, row):
        if row < 0:
            row = max(0, self.row_count + row)
        self.qt.removeRow(row)

    def remove_column(self, column):
        if column < 0:
            column = max(0, self.column_count + column)
        self.qt.removeColumn(column)

    def clear(self):
        """Clear table contents."""
        self.qt.clearContents()

    @property
    def current(self):
        """Returns current table item or None."""
        item = self.qt.currentItem()
        if item is not None:
            return item.data(item.UserType)
        return None

    @current.setter
    def current(self, value):
        assert isinstance(value, TableItem)
        self.qt.setCurrentItem(value.qt)

    @property
    def stretch(self):
        """Stretch last column.

        >>> table.stretch = True
        >>> table.stretch
        True
        """
        return self.qt.horizontalHeader().stretchLastSection()

    @stretch.setter
    def stretch(self, value):
        self.qt.horizontalHeader().setStretchLastSection(value)

    def fit(self, column=None):
        if column is None:
            self.qt.resizeColumnsToContents()
        else:
            self.qt.resizeColumnToContents(column)
        self.qt.resizeRowsToContents()

    def __getitem__(self, key):
        items = []
        for column in range(self.column_count):
            item = self.qt.item(key, column)
            if item:
                items.append(item.data(item.UserType))
            else:
                items.append(None)
        return items

    def __setitem__(self, key, value):
        self.qt.removeRow(key)
        self.qt.insertRow(key)
        for column, item in enumerate(value):
            if not isinstance(item, TableItem):
                item = TableItem(value=item)
            self.qt.setItem(key, column, item.qt)

    def __delitem__(self, key):
        self.remove_row(key)

    def __len__(self):
        return self.row_count

    def __iter__(self):
        return (self[row] for row in range(len(self)))

class TableItem(QutieStub):

    QtClass = QtWidgets.QTableWidgetItem

    def __init__(self, value=None, *, color=None, background=None, icon=None,
                 enabled=True, readonly=True, checked=None, checkable=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.__default_foreground = self.qt.foreground()
        self.__default_background = self.qt.background()
        self.qt.setData(self.qt.UserType, self)
        # Properties
        self.value = value
        self.color = color
        self.background = background
        if icon is not None:
            self.icon = icon
        self.enabled = enabled
        self.readonly = readonly
        if checkable is not None:
            self.checkable = checkable
        if checked is not None:
            self.checked = checked

    @property
    def value(self):
        return self.qt.data(self.qt.Type)

    @value.setter
    def value(self, value):
        return self.qt.setData(self.qt.Type, value)

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
    def readonly(self):
        return bool(self.qt.flags() & QtCore.Qt.ItemIsEditable)

    @readonly.setter
    def readonly(self, value):
        if value:
            self.qt.setFlags(self.qt.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            self.qt.setFlags(self.qt.flags() | QtCore.Qt.ItemIsEditable)

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
        else:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
        self.qt.setFlags(flags)
        self.qt.setCheckState(self.checked)
