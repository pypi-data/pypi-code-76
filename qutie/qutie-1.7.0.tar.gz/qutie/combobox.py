"""Combo box module.

For more information on the underlying Qt5 object see
[QComboBox](https://doc.qt.io/qt-5/qcombobox.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['ComboBox']

class ComboBox(BaseWidget):
    """ComboBox

    Properties
     - current
     - duplicates_enabled
     - editable
     - max_visible_items
     - minimum_contents_length

    Callbacks
     - changed
    """

    QtClass = QtWidgets.QComboBox

    def __init__(self, values=None, *, current=None, duplicates_enabled=False,
                 editable=False, max_visible_items=None,
                 minimum_contents_length=None, changed=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if values is not None:
            self.extend(values)
        if current is not None:
            self.current = current
        self.duplicates_enabled = duplicates_enabled
        self.editable = editable
        if max_visible_items is not None:
            self.max_visible_items = max_visible_items
        if minimum_contents_length is not None:
            self.minimum_contents_length = minimum_contents_length
        # Callbacks
        self.changed = changed
        # Connect signals
        def handle_current_index_changed(index):
            self.emit(self.changed, self[index])
        self.qt.currentIndexChanged.connect(handle_current_index_changed)

    def append(self, value) -> None:
        """Append value to end."""
        self.qt.addItem(format(value), value)

    def insert(self, index: int, value) -> None:
        """Insert value before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.insertItem(index, format(value), value)

    def extend(self, iterable) -> None:
        """Extend list by appending values from the iterable."""
        for value in iterable:
            self.append(value)

    def remove(self, value) -> None:
        """Remove first occurrence of value. Raises ValueError if the value is
        not present.
        """
        self.qt.removeItem(self.index(value))

    def clear(self) -> None:
        """Remove all values from widget."""
        self.qt.clear()

    def count(self, value) -> int:
        """Return number of occurrences of value."""
        return list(self).count(value)

    def index(self, value) -> int:
        """Return first index of value. Raises ValueError if the value is not
        present.
        """
        index = self.qt.findData(value)
        if index < 0:
            raise ValueError("value not in list")
        return index

    @property
    def current(self):
        return self.qt.itemData(self.qt.currentIndex())

    @current.setter
    def current(self, item):
        index = self.qt.findData(item)
        self.qt.setCurrentIndex(index)

    @property
    def duplicates_enabled(self) -> bool:
        return self.qt.duplicatesEnabled()

    @duplicates_enabled.setter
    def duplicates_enabled(self, value: bool) -> None:
        self.qt.setDuplicatesEnabled(value)

    @property
    def editable(self) -> bool:
        return self.qt.isEditable()

    @editable.setter
    def editable(self, value: bool) -> None:
        self.qt.setEditable(value)

    @property
    def max_visible_items(self) -> int:
        return self.qt.maxVisibleItems()

    @max_visible_items.setter
    def max_visible_items(self, value: int) -> None:
        self.qt.setMaxVisibleItems(value)

    @property
    def minimum_contents_length(self) -> int:
        return self.qt.minimumContentsLength()

    @minimum_contents_length.setter
    def minimum_contents_length(self, value: int) -> None:
        self.qt.setMinimumContentsLength(value)

    def __getitem__(self, index):
        if index < 0:
            index = max(0, len(self) + index)
        value = self.qt.itemData(index)
        key = self.qt.itemText(index)
        if value is None and key:
            return key
        return value

    def __setitem__(self, index, value):
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.setItemText(index, format(value))
        self.qt.setItemData(index, value)

    def __delitem__(self, index):
        if index < 0:
            index = max(0, len(self) + index)
        self.qt.removeItem(index)

    def __len__(self):
        return self.qt.count()

    def __iter__(self):
        return (self[row] for row in range(len(self)))
