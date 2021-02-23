import traceback

from .qutie import QtWidgets

from .widget import BaseWidget

__all__ = [
    'MessageBox',
    'show_info',
    'show_warning',
    'show_error',
    'show_exception',
    'show_question'
]

class MessageBox(BaseWidget):
    """Message box dialog."""

    QtClass = QtWidgets.QMessageBox

    QtIcons = {
        'information': QtWidgets.QMessageBox.Information,
        'warning': QtWidgets.QMessageBox.Warning,
        'critical': QtWidgets.QMessageBox.Critical,
        'question': QtWidgets.QMessageBox.Question
    }
    QtStandardButtons = {
        'ok': QtWidgets.QMessageBox.Ok,
        'open': QtWidgets.QMessageBox.Open,
        'save': QtWidgets.QMessageBox.Save,
        'cancel': QtWidgets.QMessageBox.Cancel,
        'close': QtWidgets.QMessageBox.Close,
        'discard': QtWidgets.QMessageBox.Discard,
        'apply': QtWidgets.QMessageBox.Apply,
        'reset': QtWidgets.QMessageBox.Reset,
        'restore_defaults': QtWidgets.QMessageBox.RestoreDefaults,
        'help': QtWidgets.QMessageBox.Help,
        'save_all': QtWidgets.QMessageBox.SaveAll,
        'yes': QtWidgets.QMessageBox.Yes,
        'yes_to_all': QtWidgets.QMessageBox.YesToAll,
        'no': QtWidgets.QMessageBox.No,
        'no_to_all': QtWidgets.QMessageBox.NoToAll,
        'abort': QtWidgets.QMessageBox.Abort,
        'retry': QtWidgets.QMessageBox.Retry,
        'ignore': QtWidgets.QMessageBox.Ignore
    }

    def __init__(self, *, icon=None, title=None, text=None, details=None,
                 informative=None, buttons=None, width=None, parent=None,
                 **kwargs):
        super().__init__(**kwargs)
        if icon is not None:
            self.icon = icon
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        if details is not None:
            self.details = details
        if informative is not None:
            self.informative = informative
        if buttons is not None:
            self.buttons = buttons
        if parent is not None:
            self.parent = parent
        # Workaround to resize message box
        layout = self.qt.layout()
        rows = layout.rowCount()
        columns = layout.columnCount()
        self._spacer_item = QtWidgets.QSpacerItem(420, 0)
        layout.addItem(self._spacer_item, rows, 0, 1, columns)
        if width is not None:
            self.width = width

    @property
    def icon(self):
        icon = self.qt.icon()
        for key, value in self.QtIcons.items():
            if value == icon:
                return key
        return None

    @icon.setter
    def icon(self, value):
        self.qt.setIcon(self.QtIcons.get(value, QtWidgets.QMessageBox.NoIcon))

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

    @property
    def details(self):
        return self.qt.detailedText()

    @details.setter
    def details(self, value):
        self.qt.setDetailedText(value)

    @property
    def informative(self):
        return self.qt.informativeText()

    @informative.setter
    def informative(self, value):
        self.qt.setInformativeText(value)

    @property
    def buttons(self):
        buttons = []
        values = self.qt.standardButtons()
        for key, mask in self.QtStandardButtons.items():
            if values & mask:
                buttons.append(key)
        return tuple(buttons)

    @buttons.setter
    def buttons(self, value):
        buttons = 0
        for button in value:
            buttons |= self.QtStandardButtons.get(button, 0)
        self.qt.setStandardButtons(buttons)

    @property
    def width(self):
        return self.qt.width()

    @width.setter
    def width(self, value):
        self._spacer_item.changeSize(value, 0)

    def run(self):
        result = self.qt.exec_()
        for key, value in self.QtStandardButtons.items():
            if value == result:
                return key
        return None

def show_info(text, *, title=None, details=None, **kwargs):
    """Show information message box.

    >>> show_info("Info", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(
        icon='information',
        title=title,
        text=text,
        details=details,
        **kwargs
    )
    dialog.run()

def show_warning(text, *, title=None, details=None, **kwargs):
    """Show warning message box.

    >>> show_warning("Warning", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(
        icon='warning',
        title=title,
        text=text,
        details=details,
        **kwargs
    )
    dialog.run()

def show_error(text, *, title=None, details=None, **kwargs):
    """Show warning message box.

    >>> show_error("Error", "NO-body expects the Spanish Inquisition!")
    """
    dialog = MessageBox(
        icon='critical',
        title=title,
        text=text,
        details=details,
        **kwargs
    )
    dialog.run()

def show_exception(exception, tb=None, **kwargs):
    """Show exception message box including exception stack trace.

    >>> try:
    ...     foo()
    ... except NameError as e:
    ...     show_exception(e)
    """
    if not tb:
        tb = traceback.format_exc() or None
    show_error(
        title="An exception occured",
        text=format(exception),
        details=tb,
        **kwargs
    )

def show_question(text, *, title=None, details=None, **kwargs):
    """Show question message box, returns True for yes and False for no.

    >>> show_question("Question", "Fancy a cup of Yorkshire Tea?")
    True
    """
    dialog = MessageBox(
        icon='question',
        title=title,
        text=text,
        details=details,
        buttons=('yes', 'no'),
        **kwargs
    )
    return dialog.run() == 'yes'
