from .qutie import QtWidgets

from .action import Action
from .menu import Menu
from .widget import BaseWidget

__all__ = ['MenuBar']

class MenuBar(BaseWidget):

    QtClass = QtWidgets.QMenuBar

    def __init__(self, *items, **kwargs):
        super().__init__(**kwargs)
        for item in items:
            self.append(item)

    def index(self, item):
        for index, action in enumerate(self):
            if action is item:
                return index
        raise ValueError("item not in list")

    def clear(self) -> None:
        while len(self):
            self.remove(self[0])

    def append(self, item):
        if isinstance(item, str):
            item = Menu(text=item)
        if isinstance(item, Action):
            self.qt.addAction(item.qt)
        else:
            self.qt.addMenu(item.qt)
        return item

    def insert(self, index: int, item) -> None:
        """Insert value before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        if isinstance(item, str):
            item = Menu(text=item)
        before = self[index] if len(self) else None
        if isinstance(before, type(None)):
            self.qt.insertMenu(None, item.qt)
        elif isinstance(before, Menu):
            self.qt.insertMenu(before.qt.menuAction(), item.qt)
        else:
            self.qt.insertMenu(before.qt, item.qt)
        return item

    def extend(self, iterable) -> None:
        """Extend list by appending values from the iterable."""
        for item in iterable:
            self.append(item)

    def remove(self, item):
        index = self.index(item)
        self.qt.removeAction(self.qt.actions()[index])

    def _get_action_or_menu(self, action):
        if hasattr(action, 'reflection'):
            return action.reflection()
        return action.menu().reflection()

    def __getitem__(self, index):
        action = self.qt.actions()[index]
        return self._get_action_or_menu(action)

    def __iter__(self):
        return iter(self._get_action_or_menu(action) for action in self.qt.actions())

    def __len__(self):
        return len(self.qt.actions())
