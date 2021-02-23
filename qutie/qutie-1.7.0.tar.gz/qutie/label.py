"""Label module.

For more information on the underlying Qt5 object see
[QLabel](https://doc.qt.io/qt-5/qlabel.html).
"""

from .qutie import QtWidgets
from .qutie import TextFormat

from .frame import Frame
from .pixmap import Pixmap

__all__ = ['Label']

class Label(Frame):
    """A label widget.

    >>> label = Label('lorem')
    >>> label.text
    'lorem'

    Use a pixmap instead of text.

    >>> label = Label(pixmap='sample.png')
    """

    QtClass = QtWidgets.QLabel

    link_activated = None
    link_hovered = None

    def __init__(self, text=None, *, indent=None, margin=None, pixmap=None,
                 text_format=None, word_wrap=None, link_activated=None,
                 link_hovered=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if text is not None:
            self.text = text
        if indent is not None:
            self.indent = indent
        if margin is not None:
            self.margin = margin
        if pixmap is not None:
            self.pixmap = pixmap
        if text_format is not None:
            self.text_format = text_format
        if word_wrap is not None:
            self.word_wrap = word_wrap
        # Callbacks
        self.link_activated = link_activated
        self.link_hovered = link_hovered
        # Connect signals
        self.qt.linkActivated.connect(lambda link: self.emit(self.link_activated, link))
        self.qt.linkHovered.connect(lambda link: self.emit(self.link_hovered, link))

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(format(value))

    @property
    def indent(self):
        return self.qt.indent()

    @indent.setter
    def indent(self, value):
        self.qt.setIndent(int(value))

    @property
    def margin(self):
        return self.qt.margin()

    @margin.setter
    def margin(self, value):
        self.qt.setMargin(int(value))

    @property
    def pixmap(self):
        pixmap = self.qt.pixmap()
        if pixmap is not None:
            return Pixmap(qt=pixmap)
        return None

    @pixmap.setter
    def pixmap(self, value):
        if not isinstance(value, Pixmap):
            value = Pixmap(value)
        self.qt.setPixmap(value.qt)

    @property
    @TextFormat.getter
    def text_format(self):
        return self.qt.textFormat()

    @text_format.setter
    @TextFormat.setter
    def text_format(self, value):
        self.qt.setTextFormat(value)

    @property
    def word_wrap(self):
        """Enable automatic word wrap."""
        return self.qt.wordWrap()

    @word_wrap.setter
    def word_wrap(self, value):
        self.qt.setWordWrap(bool(value))

    @property
    def selected_text(self):
        return self.qt.selectedText()

    def clear(self):
        """Clears label contents."""
        self.qt.clear()
