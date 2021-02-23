"""Check box module.

For more information on the underlying Qt5 object see
[QCheckBox](https://doc.qt.io/qt-5/qcheckbox.html).
"""

from .qutie import QtCore
from .qutie import QtWidgets

from .button import AbstractButton

__all__ = ['CheckBox']

class CheckBox(AbstractButton):
    """CheckBox

    Properties
     - text
     - checked

    Callbacks
     - changed
    """

    QtClass = QtWidgets.QCheckBox

    changed = None

    def __init__(self, text=None, *, checked=False, changed=None, **kwargs):
        super().__init__(**kwargs)
        # Properties
        if text is not None:
            self.text = text
        self.checked = checked
        # Callbacks
        self.changed = changed
        # Connect signals
        def handle_state_changed(state):
            self.emit(self.changed, state == QtCore.Qt.Checked)
        self.qt.stateChanged.connect(handle_state_changed)

    @property
    def text(self) -> str:
        return self.qt.text()

    @text.setter
    def text(self, value: str):
        self.qt.setText(value)

    @property
    def checked(self) -> bool:
        return self.qt.checkState() == QtCore.Qt.Checked

    @checked.setter
    def checked(self, value: bool):
        self.qt.setChecked(QtCore.Qt.Checked if value else QtCore.Qt.Unchecked)
