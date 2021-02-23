"""Text area input.

For more information on the underlying Qt5 object see
[QTextEdit](https://doc.qt.io/qt-5/qtextedit.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['TextArea']

class TextArea(BaseWidget):
    """Text area widget.

    Callbacks
    - copy_available(yes)
    - cursor_position_changed(position)

    >>> textarea = TextArea('lorem')
    >>> textarea.append(' ispum')
    >>> textarea.value
    'lorem ipsum'
    >>> tree.clear()
    textarea.value
    ''
    """

    QtClass = QtWidgets.QTextEdit

    changed = None
    copy_available = None
    redo_available = None
    undo_available = None

    def __init__(self, value=None, *, readonly=False, richtext=False,
                 placeholder_text=None, changed=None, copy_available=None,
                 redo_available=None, undo_available=None,
                 **kwargs):
        super().__init__(**kwargs)
        # Properties
        self.readonly = readonly
        self.richtext = richtext
        self.placeholder_text = placeholder_text
        if value is not None:
            self.value = value
        # Callbacks
        self.changed = changed
        self.copy_available = copy_available
        self.redo_available = redo_available
        self.undo_available = undo_available
        # Connect signals
        self.qt.textChanged.connect(lambda: self.emit(self.changed))
        self.qt.copyAvailable.connect(lambda yes: self.emit(self.copy_available, yes))
        self.qt.redoAvailable.connect(lambda available: self.emit(self.redo_available, available))
        self.qt.undoAvailable.connect(lambda available: self.emit(self.undo_available, available))

    @property
    def value(self):
        return self.qt.toPlainText()

    @value.setter
    def value(self, value):
        self.qt.setPlainText(value)

    @property
    def readonly(self):
        """Read only enabled.

        >>> textarea.readonly = True
        >>> textarea.readonly
        True
        """
        return self.qt.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)

    @property
    def richtext(self):
        """Rich Text enabled.

        >>> textarea.richtext = True
        >>> textarea.richtext
        True
        """
        return self.qt.acceptRichText()

    @richtext.setter
    def richtext(self, value):
        self.qt.setAcceptRichText(value)

    @property
    def placeholder_text(self):
        return self.qt.placeholderText()

    @placeholder_text.setter
    def placeholder_text(self, value):
        self.qt.setPlaceholderText(value)

    @property
    def cursor_position(self) -> int:
        return self.qt.textCursor().position()

    @cursor_position.setter
    def cursor_position(self, value: int) -> None:
        self.qt.textCursor().setPosition(value)

    @property
    def is_undo_redo_enabled(self) -> bool:
        return self.qt.isUndoRedoEnabled()

    def append(self, text):
        """Append text as paragraph to current value.

        >>> textarea = TextArea('lorem')
        >>> textarea.append(' ipsum')
        >>> textarea.value
        'lorem\n ipsum'
        """
        self.qt.append(text)

    def insert(self, text):
        """Insert text at cursor position.

        >>> textarea.insert('ipsum')
        """
        self.qt.insertPlainText(text)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def clear(self):
        """Clear current value.

        >>> textarea.clear()
        >>> textarea.value
        ''
        """
        self.qt.clear()

    def copy(self):
        """Copy selected text to clipboard."""
        self.qt.copy()

    def cut(self):
        """Copy selected text to clipboard and deletes selection."""
        self.qt.cut()

    def select_all(self):
        """Select entire text."""
        self.qt.selectAll()

    def redo(self):
        """Redo last user changes."""
        self.qt.redo()

    def undo(self):
        """Undo last user changes."""
        self.qt.undo()
