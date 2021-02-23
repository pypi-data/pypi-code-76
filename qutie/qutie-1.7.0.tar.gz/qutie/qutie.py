from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

__all__ = ['Qutie']

Qt = QtCore.Qt

def to_brush(method):
    def to_brush(self, value):
        if value is None:
            brush = QtGui.QBrush()
        else:
            brush = QtGui.QBrush(QtGui.QColor(value))
        return method(self, brush)
    return to_brush

def from_brush(method):
    def from_brush(self):
        value = method(self)
        if value is not None:
            return QtGui.QBrush(value).color().name()
        return None
    return from_brush

class Enum:

    QtEnums = {}

    @classmethod
    def setter(cls, method):
        def setter(self, value):
            return method(self, cls.to_value(value))
        return setter

    @classmethod
    def getter(cls, method):
        def getter(self):
            value = method(self)
            return cls.to_key(value)
        return getter

    @classmethod
    def to_value(cls, key):
        return cls.QtEnums.get(key)

    @classmethod
    def to_key(cls, value):
        values = tuple(cls.QtEnums.values())
        if value in values:
            return tuple(cls.QtEnums.keys())[values.index(value)]
        return None

class ArrowType(Enum):

    QtEnums = {
        'no': Qt.NoArrow,
        'up': Qt.UpArrow,
        'down': Qt.DownArrow,
        'left': Qt.LeftArrow,
        'right': Qt.RightArrow
    }

class CursorShape(Enum):

    QtEnums = {
        'arrow': Qt.ArrowCursor,
        'up_arrow': Qt.UpArrowCursor,
        'cross': Qt.CrossCursor,
        'wait': Qt.WaitCursor,
        'i_beam': Qt.IBeamCursor,
        'size_ver': Qt.SizeVerCursor,
        'size_hor': Qt.SizeHorCursor,
        'size_b_diag': Qt.SizeBDiagCursor,
        'size_f_diag': Qt.SizeFDiagCursor,
        'size_all': Qt.SizeAllCursor,
        'blank': Qt.BlankCursor,
        'split_v': Qt.SplitVCursor,
        'split_h': Qt.SplitHCursor,
        'pointing_hand': Qt.PointingHandCursor,
        'forbidden': Qt.ForbiddenCursor,
        'open_hand': Qt.OpenHandCursor,
        'closed_hand': Qt.ClosedHandCursor,
        'whats_this': Qt.WhatsThisCursor,
        'busy': Qt.BusyCursor,
        'drag_move': Qt.DragMoveCursor,
        'drag_copy': Qt.DragCopyCursor,
        'drag_link': Qt.DragLinkCursor,
        'bitmap': Qt.BitmapCursor
    }

class Orientation(Enum):

    QtEnums = {
        'horizontal': Qt.Horizontal,
        'vertical': Qt.Vertical
    }

class TextFormat(Enum):

    QtEnums = {
        'plain': Qt.PlainText,
        'rich': Qt.RichText,
        'auto': Qt.AutoText,
        'markdown': Qt.MarkdownText
    }

class ToolButtonStyle(Enum):

    QtEnums = {
        'icon_only': QtCore.Qt.ToolButtonIconOnly,
        'text_only': QtCore.Qt.ToolButtonTextOnly,
        'text_beside_icon': QtCore.Qt.ToolButtonTextBesideIcon,
        'text_under_icon': QtCore.Qt.ToolButtonTextUnderIcon,
        'follow_style': QtCore.Qt.ToolButtonFollowStyle
    }

class QutieStub:

    QtClass = NotImplemented

    def __init__(self, qt=None):
        class QtClassWrapper(type(self).QtClass):

            def reflection(self):
                return self._reflection

            def setReflection(self, value):
                self._reflection = value

        if qt is None: qt = []
        if not isinstance(qt, (tuple, list)):
            qt=[qt]
        self.__qt = QtClassWrapper(*qt)
        self.qt.setReflection(self)

    @property
    def qt(self):
        return self.__qt

class Qutie:

    QtClass = NotImplemented

    def __init__(self, qt=None):
        class QtClassWrapper(type(self).QtClass):

            handleEvent = QtCore.pyqtSignal(object)

            def reflection(self):
                return self.property('__qutie_property')

            def setReflection(self, value):
                self.setProperty('__qutie_property', value)

        if qt is None: qt = []
        if not isinstance(qt, (tuple, list)):
            qt=[qt]
        self.__qt = QtClassWrapper(*qt)
        self.qt.setReflection(self)

    @property
    def qt(self):
        return self.__qt
