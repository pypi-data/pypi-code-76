"""Single line text input.

For more information on the underlying Qt5 object see
[QLineEdit](https://doc.qt.io/qt-5/qlineedit.html).
"""

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = ['Text']

class Text(BaseWidget):
    """Text input widget.

    >>> text = Text('lorem')
    >>> text.append(' ispum')
    >>> text.value
    'lorem ipsum'
    >>> tree.clear()
    text.value
    ''
    """

    QtClass = QtWidgets.QLineEdit

    changed = None
    edited = None
    editing_finished = None

    def __init__(self, value=None, *, readonly=False, clearable=False,
                 changed=None, edited=None, editing_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.readonly = readonly
        self.clearable = clearable
        if value is not None:
            self.value = value
        # Callbacks
        self.changed = changed
        self.edited = edited
        self.editing_finished = editing_finished
        # Connect signals
        self.qt.textChanged.connect(lambda text: self.emit(self.changed, text))
        self.qt.textEdited.connect(lambda text: self.emit(self.edited, text))
        self.qt.editingFinished.connect(lambda: self.emit(self.editing_finished))

    @property
    def value(self):
        return self.qt.text()

    @value.setter
    def value(self, value):
        self.qt.setText(format(value))

    @property
    def readonly(self):
        """Read only enabled.

        >>> text.readonly = True
        >>> text.readonly
        True
        """
        return self.qt.isReadOnly()

    @readonly.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)

    @property
    def clearable(self):
        """Inline clear button enabled.

        >>> text.clearable = True
        >>> text.clearable
        True
        """
        return self.qt.isClearButtonEnabled()

    @clearable.setter
    def clearable(self, value):
        self.qt.setClearButtonEnabled(bool(value))

    @property
    def modified(self) -> bool:
        return self.qt.modified()

    @modified.setter
    def modified(self, value: bool) -> None:
        self.qt.setModified(value)

    def append(self, text):
        """Append text to current value.

        >>> text =Text('lorem')
        >>> text.append(' ipsum')
        >>> text.value
        'lorem ipsum'
        """
        self.value = ''.join((self.value, format(text)))

    def extend(self, iterable):
        for text in iterable:
            self.append(text)

    def clear(self):
        """Clear current value.

        >>> text.clear()
        >>> text.value
        ''
        """
        self.qt.clear()
