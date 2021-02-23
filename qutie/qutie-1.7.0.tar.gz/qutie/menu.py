"""Menu module.

For more information on the underlying Qt5 object see
[QMenu](https://doc.qt.io/qt-5/qmenu.html).
"""

from .qutie import QtWidgets

from .action import Action
from .widget import BaseWidget

__all__ = ['Menu']

class Menu(BaseWidget):
    """
    Properties
     - text

    Callbacks
     - about_to_show()
     - about_to_hide()
     - hovered(action)
     - triggered(action)
    """

    QtClass = QtWidgets.QMenu

    about_to_show = None
    about_to_hide = None
    hovered = None
    triggered = None

    def __init__(self, *items, text=None, about_to_show=None,
                 about_to_hide=None, hovered=None, triggered=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        for item in items:
            self.append(item)
        if text is not None:
            self.text = text
        # Callbacks
        self.about_to_show = about_to_show
        self.about_to_hide = about_to_hide
        self.hovered = hovered
        self.triggered = triggered
        # Connect signals
        def handle_about_to_show():
            self.emit(self.about_to_show)
        self.qt.aboutToShow.connect(handle_about_to_show)
        def handle_about_to_hide():
            self.emit(self.about_to_hide)
        self.qt.aboutToHide.connect(handle_about_to_hide)
        def handle_hovered(action):
            if isinstance(action, Action):
                self.emit(self.hovered, action.qt)
        self.qt.hovered.connect(handle_hovered)
        def handle_triggered(action):
            if isinstance(action, Action):
                self.emit(self.triggered, action.qt)
        self.qt.triggered.connect(handle_triggered)

    @property
    def text(self):
        return self.qt.title()

    @text.setter
    def text(self, value):
        self.qt.setTitle(value)

    def append(self, item):
        if isinstance(item, str):
            item = Action(item)
        if isinstance(item, Action):
            self.qt.addAction(item.qt)
        elif isinstance(item, Menu):
            self.qt.addMenu(item.qt)
        else:
            raise ValueError(item)
        return item

    def insert(self, index: int, item) -> None:
        """Insert item before index. Permits negative indexing."""
        if index < 0:
            index = max(0, len(self) + index)
        if isinstance(item, str):
            item = Action(item)
        before = self[index].qt if len(self) else None
        if isinstance(item, Action):
            self.qt.insertAction(before, item.qt)
        elif isinstance(item, Menu):
            self.qt.insertMenu(before, item.qt)
        else:
            raise ValueError(item)
        return item

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, item):
        if not isinstance(item, (Action, Menu)):
            raise TypeError("value not an action or menu")
        if not item in self:
            raise ValueError("value not in menu")
        self.qt.removeAction(item.qt)

    def index(self, item):
        """Return first index of item. Raises ValueError if the item is not
        present.
        """
        if not isinstance(item, (Action, Menu)):
            raise TypeError("value not an action or menu")
        index = self.qt.actions().index(item.qt)
        if index < 0:
            raise ValueError("value not in list")
        return index

    def clear(self):
        """Remove all actions."""
        while len(self):
            self.remove(self[0])

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
