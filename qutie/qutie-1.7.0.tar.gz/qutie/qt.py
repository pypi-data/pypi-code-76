"""This module provides backward compatibility for qutie < 1.6.0"""

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

__all__ = [
    'QtCore',
    'QtGui',
    'QtWidgets',
    'bind'
]

def bind(qt):
    """Decorator used to bind custom events on a Qt base class."""
    def bind(cls):
        cls.QtClass = qt
        return cls
    return bind
