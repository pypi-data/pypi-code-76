"""Object module.

For more information on the underlying Qt5 object see
[QObject](https://doc.qt.io/qt-5/qobject.html).
"""

from .qutie import QtCore
from .qutie import Qutie

__all__ = ['Object']

class Object(Qutie):
    """Object

    Properties
    - object_name
    - parent

    Callbacks
    - destroyed()
    - object_name_changed(object_name)
    """

    QtClass = QtCore.QObject

    destroyed = None
    object_name_changed = None

    def __init__(self, *, object_name=None, parent=None, destroyed=None,
                 object_name_changed=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setReflection(self)
        # Properties
        if object_name is not None:
            self.object_name = object_name
        if parent is not None:
            self.parent = parent
        # Callbacks
        self.destroyed = destroyed
        self.object_name_changed = object_name_changed
        # Connect signals
        def handle_destroyed():
            if callable(self.destroyed):
                self.destroyed()
        self.qt.destroyed.connect(handle_destroyed) # can't reference already destroyed object
        self.qt.objectNameChanged.connect(lambda object_name: self.emit(self.object_name_changed, self.object_name))
        self.qt.handleEvent.connect(lambda event: event())

    @property
    def object_name(self) -> str:
        return self.qt.objectName()

    @object_name.setter
    def object_name(self, value: str):
        self.qt.setObjectName(value)

    @property
    def parent(self):
        parent = self.qt.parent()
        if hasattr(parent, 'reflection'):
            return parent.reflection()

    @parent.setter
    def parent(self, value):
        assert isinstance(value, Object), "Parent must inherit from Object"
        self.qt.setParent(value.qt)

    def emit(self, *args, **kwargs):
        """Emit an event.

        >>> o.event = lambda value: print(value) # assign event callback
        >>> o.emit('event', 42)
        """
        if not args:
            raise ValueError("Missing event argument.")
        event = args[0]
        if isinstance(event, str):
            if hasattr(self, event):
                event = getattr(self, event)
        if callable(event):
            self.qt.handleEvent.emit(lambda: event(*args[1:], **kwargs))
