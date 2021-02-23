from .qutie import QtCore
from .qutie import Orientation

__all__ = ['OrientationMixin']

class OrientationMixin:

    @property
    @Orientation.getter
    def orientation(self):
        return self.qt.orientation()

    @orientation.setter
    @Orientation.setter
    def orientation(self, value):
        self.qt.setOrientation(value)
