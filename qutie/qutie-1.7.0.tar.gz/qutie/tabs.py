"""Stack of tabbed widgets.

## Example Usage

>>> tabs = Tabs(
    Tab(title="Spam"),
    Tab(title="Ham")
)
>>> tabs.append(Tab("Eggs")) # append tab "Eggs"
>>> tabs.remove(tabs[0]) # remove tab "Spam"
>>> tabs.insert(0, Tab(title="Spam")) # insert again at begin
>>> tabs.current = tabs[1] # show tab "Ham"
>>> for tab in tabs:
...     print(tab.title)

For more information on the underlying Qt5 object see [QTabWidget](https://doc.qt.io/qt-5/qtabwidget.html).
"""

from .qutie import QtWidgets
from .widget import BaseWidget, Widget

__all__ = [
    'Tab',
    'Tabs'
]

class Tab(Widget):
    """Tab item, property `title` displayed in tab bar."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def title(self):
        """Title displayed in tab bar."""
        return self.qt.windowTitle()

    @title.setter
    def title(self, value):
        self.qt.setWindowTitle(value)
        # Update tab title
        parent = self.qt.parent()
        if parent:
            if parent.parent():
                index = parent.parent().indexOf(self.qt)
                parent.parent().setTabText(index, value)

class Tabs(BaseWidget):
    """Tab widget providign a tab bar and item stack."""

    QtClass = QtWidgets.QTabWidget

    changed = None
    tab_close_request = None

    def __init__(self, *items, tabs_closable=False, changed=None,
                 tab_close_request=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        for item in items:
            self.append(item)
        self.tabs_closable = tabs_closable
        # Callbacks
        self.changed = changed
        self.tab_close_request = tab_close_request
        # Connect signals
        self.qt.currentChanged.connect(lambda index: self.emit(self.changed, index))
        self.qt.tabCloseRequested.connect(lambda index: self.emit(self.tab_close_request, index))

    @property
    def tabs_closable(self) -> bool:
        return self.qt.tabsClosable()

    @tabs_closable.setter
    def tabs_closable(self, value: bool) -> None:
        self.qt.setTabsClosable(value)

    def append(self, tab) -> None:
        """Append tab item to tab widget.

        >>> tabs.append(Tab(title="Spam"))
        """
        self.qt.addTab(tab.qt, tab.title)

    def insert(self, index: int, tab) -> None:
        """Insert tab item at index to tab widget.

        >>> tabs.insert(0, Tab(title="Spam"))
        """
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertTab(index, tab.qt, tab.title)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, tab):
        """Remove tab item from tab widget.

        >>> tabs.remove(tabs[0])
        """
        index = self.qt.indexOf(tab.qt)
        self.qt.removeTab(index)

    @property
    def current(self):
        """Current active tab item.

        >>> tabs.current = tabs[0]
        >>> tabs.current
        <Tab ...>
        """
        index = self.qt.currentIndex()
        if index < 0:
            return None
        return self[index]

    @current.setter
    def current(self, item):
        index = self.index(item)
        self.qt.setCurrentIndex(index)

    def index(self, item):
        """Return index of tab item. Raising a `ValueError` if provided item is
        not part of the tab widget.

        >>> tabs.index(tabs[0])
        0
        """
        index = self.qt.indexOf(item.qt)
        if index < 0:
            raise ValueError("item not in tabs")
        return index

    def clear(self):
        """Remove all tab items."""
        while len(self):
            self.remove(self.current)

    def __getitem__(self, key):
        widget = self.qt.widget(key)
        if not widget:
            raise KeyError(key)
        return widget.reflection()

    def __setitem__(self, key, value):
        del self[key]
        self.insert(key, value)

    def __delitem__(self, key):
        self.qt.removeTab(key)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[index] for index in range(len(self)))
