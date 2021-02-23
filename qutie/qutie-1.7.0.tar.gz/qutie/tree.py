"""Tree module.

For more information on the underlying Qt5 objects see
[QTreeWidget](https://doc.qt.io/qt-5/qtreewidget.html) and
[QTreeWidgetItem](https://doc.qt.io/qt-5/qtreewidgetitem.html).
"""

from .qutie import QtCore
from .qutie import QtGui
from .qutie import QtWidgets
from .qutie import Qutie, QutieStub

from .icon import Icon
from .list import BaseItemView

__all__ = ['Tree', 'TreeItem', 'TreeItemColumn']

class Tree(BaseItemView):
    """Tree widget.

    >>> tree = Tree(header=["Key", "Value"])
    >>> tree.append(["Spam", "Eggs"])
    >>> for item in tree:
    ...     item[0].checked =True
    ...     item[1].color = "blue"
    ...     child = item.append(["Ham", "Spam"])
    ...     child.checked = False
    >>> tree.clear()
    """

    QtClass = QtWidgets.QTreeWidget

    activated = None
    changed = None
    clicked = None
    double_clicked = None
    selected = None

    def __init__(self, items=None, *, expands_on_double_click=None, header=None,
                 sortable=False, indentation=None, root_is_decorated=None,
                 uniform_row_heights=None, word_wrap=None, activated=None,
                 changed=None, clicked=None, double_clicked=None, selected=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Properties
        if items is not None:
            self.items = items
        if expands_on_double_click is not None:
            self.expands_on_double_click = expands_on_double_click
        self.header = header or []
        self.sortable = sortable
        if indentation is not None:
            self.indentation = indentation
        if root_is_decorated is not None:
            self.root_is_decorated = root_is_decorated
        if uniform_row_heights is not None:
            self.uniform_row_heights = uniform_row_heights
        if word_wrap is not None:
            self.word_wrap = word_wrap
        # Callbacks
        self.activated = activated
        self.changed = changed
        self.clicked = clicked
        self.double_clicked = double_clicked
        self.selected = selected
        # Connect signals
        def handle_item_activated(item, index):
            data = item.data(0, item.UserType)
            if data is not None:
                self.emit(self.activated, index, data)
        self.qt.itemActivated.connect(handle_item_activated)
        def handle_item_changed(item, index):
            data = item.data(0, item.UserType)
            if data is not None:
                self.emit(self.changed, index, data)
        self.qt.itemChanged.connect(handle_item_changed)
        def handle_item_clicked(item, index):
            data = item.data(0, item.UserType)
            if data is not None:
                self.emit(self.clicked, index, data)
        self.qt.itemClicked.connect(handle_item_clicked)
        def handle_item_double_clicked(item, index):
            data = item.data(0, item.UserType)
            if data is not None:
                self.emit(self.double_clicked, index, data)
        self.qt.itemDoubleClicked.connect(handle_item_double_clicked)
        def handle_item_selection_changed():
            items = self.qt.selectedItems()
            if items:
                first = items[0].data(0, items[0].UserType)
                self.emit(self.selected, first)
        self.qt.itemSelectionChanged.connect(handle_item_selection_changed)

    @property
    def expands_on_double_click(self):
        return self.qt.expandsOnDoubleClick()

    @expands_on_double_click.setter
    def expands_on_double_click(self, value):
        self.qt.setExpandsOnDoubleClick(bool(value))

    @property
    def header(self):
        item = self.qt.headerItem()
        return tuple([item.text(index) for index in range(self.qt.columnCount())])

    @header.setter
    def header(self, value):
        self.qt.setColumnCount(len(value))
        self.qt.setHeaderLabels(value)

    @property
    def sortable(self):
        return self.qt.isSortingEnabled()

    @sortable.setter
    def sortable(self, value):
        self.qt.setSortingEnabled(value)

    @property
    def indentation(self):
        return self.qt.indentation()

    @indentation.setter
    def indentation(self, value):
        if value is None:
            self.qt.resetIndentation()
        else:
            self.qt.setIndentation(int(value))

    @property
    def root_is_decorated(self):
        return self.qt.rootIsDecorated()

    @root_is_decorated.setter
    def root_is_decorated(self, value):
        self.qt.setRootIsDecorated(bool(value))

    @property
    def uniform_row_heights(self):
        return self.qt.uniformRowHeights()

    @uniform_row_heights.setter
    def uniform_row_heights(self, value):
        self.qt.setUniformRowHeights(bool(value))

    @property
    def word_wrap(self):
        return self.qt.wordWrap()

    @word_wrap.setter
    def word_wrap(self, value):
        self.qt.setWordWrap(bool(value))

    def append(self, item):
        """Append item or item labels, returns appended item.
        >>> tree.append(TreeItem(["Spam", "Eggs"]))
        or
        >>> tree.append(["Spam", "Eggs"])
        """
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addTopLevelItem(item.qt)
        item.expanded = True
        return item

    def insert(self, index, item):
        """Insert item or item labels at index, returns inserted item.
        >>> tree.insert(0, TreeItem(["Spam", "Eggs"]))
        or
        >>> tree.insert(0, ["Spam", "Eggs"])
        """
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertTopLevelItem(index, item.qt)
        item.expanded = True
        return item

    def remove(self, item):
        """Remove item from tree. Raises ValueError if the value is not present.
        """
        if not isinstance(item, TreeItem):
            raise TypeError("invalid item type")
        self.qt.takeTopLevelItem(self.index(item))

    def clear(self):
        """Remove all tree items."""
        self.qt.clear()

    @property
    def current(self):
        """Returns current tree item or None."""
        item = self.qt.currentItem()
        if item is not None:
            return item.data(0, item.UserType)
        return item

    @current.setter
    def current(self, item):
        if not isinstance(item, TreeItem):
            raise TypeError("invalid item type")
        self.qt.setCurrentItem(item.qt)

    def index(self, item):
        """Return index of item. Raises ValueError if the item is not present.
        """
        index = self.qt.indexOfTopLevelItem(item.qt)
        if index < 0:
            raise ValueError("item not in tree")
        return index

    @property
    def stretch(self):
        return self.qt.header().stretchLastSection()

    @stretch.setter
    def stretch(self, value):
        self.qt.header().setStretchLastSection(value)

    def fit(self, column=None):
        if column is None:
            for column in range(self.qt.columnCount()):
                self.qt.resizeColumnToContents(column)
        else:
            self.qt.resizeColumnToContents(column)

    def scroll_to(self, item):
        """Scroll to item to ensure item is visible."""
        if not isinstance(item, TreeItem):
            raise TypeError("invalid item type")
        self.qt.scrollToItem(item.qt)

    def __getitem__(self, key):
        item = self.qt.topLevelItem(key)
        if not item:
            raise IndexError(key)
        return item.data(0, item.UserType)

    def __setitem__(self, key, value):
        self.remove(value)
        self.insert(key, value)

    def __delitem__(self, key):
        item = self.qt.topLevelItem(key)
        if not item:
            raise IndexError(key)
        self.remove(item)

    def __len__(self):
        return self.qt.topLevelItemCount()

    def __iter__(self):
        return (self[index] for index in range(len(self)))

class TreeItem(QutieStub):
    """Tree item class."""

    QtClass = QtWidgets.QTreeWidgetItem

    def __init__(self, values=None, **kwargs):
        super().__init__(**kwargs)
        self.qt._default_foreground = self.qt.foreground(0)
        self.qt._default_background = self.qt.background(0)
        self.qt.setData(0, self.qt.UserType, self)
        if values is not None:
            for column, value in enumerate(values):
                self[column].value = value

    @property
    def children(self):
        """List of tree item's children."""
        items = []
        for index in range(self.qt.childCount()):
            item = self.qt.child(index)
            items.append(item.data(0, item.UserType))
        return items

    def append(self, item):
        """Append child item to this item."""
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.addChild(item.qt)
        return item

    def insert(self, index, item):
        """Insert child item to this item."""
        if not isinstance(item, TreeItem):
            item = TreeItem(item)
        self.qt.insertChild(index, item.qt)
        return item

    def remove(self, item):
        """Remove child item."""
        if not isinstance(item, TreeItem):
            raise TypeError("invalid item type")
        self.qt.takeChild(self.index(item))

    def clear(self):
        """Remove all child items."""
        while len(self.children):
            self.remove(self.children[0])

    def index(self, item):
        """Return index of child item."""
        if not isinstance(item, TreeItem):
            raise TypeError("invalid item type")
        index = self.qt.indexOfChild(item.qt)
        if index < 0:
            raise ValueError("no such child item")
        return index

    @property
    def checkable(self):
        """Checkable state, `True` if item is checkable by user."""
        return self.qt.flags() & QtCore.Qt.ItemIsUserCheckable

    @checkable.setter
    def checkable(self, value):
        if value:
            flags = self.qt.flags() | QtCore.Qt.ItemIsUserCheckable
        else:
            flags = self.qt.flags() & ~QtCore.Qt.ItemIsUserCheckable
        self.qt.setFlags(flags)

    @property
    def expanded(self):
        """Expanded state, `True` if item is expanded."""
        return self.qt.isExpanded()

    @expanded.setter
    def expanded(self, value):
        self.qt.setExpanded(value)

    def __getitem__(self, column):
        return TreeItemColumn(column, self.qt)

    def __len__(self):
        return self.qt.columnCount()

    def __iter__(self):
        return (TreeItemColumn(column, self.qt) for column in range(len(self)))

class TreeItemColumn:
    """This class provides access to tree item column specific properties."""

    def __init__(self, column, qt):
        self.__column = column
        self.__qt = qt

    @property
    def column(self):
        return self.__column

    @property
    def qt(self):
        return self.__qt

    @property
    def value(self):
        """Column value."""
        return self.qt.data(self.column, self.qt.Type)

    @value.setter
    def value(self, value):
        return self.qt.setData(self.column, self.qt.Type, value)

    @property
    def color(self):
        return self.qt.foreground(self.column).color().name()

    @color.setter
    def color(self, value):
        if value is None:
            brush = QtGui.QBrush(self.qt._default_foreground)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setForeground(self.column, brush)

    @property
    def background(self):
        return self.qt.background(self.column).color().name()

    @background.setter
    def background(self, value):
        if value is None:
            brush = QtGui.QBrush(self.qt._default_background)
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        self.qt.setBackground(self.column, brush)

    @property
    def icon(self):
        """Column icon, can be a `Pixmap`, filename or color."""
        icon = self.qt.icon(self.column)
        if icon.isNull():
            return None
        return Icon(qt=icon)

    @icon.setter
    def icon(self, value):
        if value is None:
            self.qt.setIcon(self.column, QtGui.QIcon())
        else:
            if not isinstance(value, Icon):
                value = Icon(value)
            self.qt.setIcon(self.column, value.qt)

    @property
    def checked(self):
        return self.qt.checkState(self.column) == QtCore.Qt.Checked

    @checked.setter
    def checked(self, value):
        self.qt.setCheckState(self.column, QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
