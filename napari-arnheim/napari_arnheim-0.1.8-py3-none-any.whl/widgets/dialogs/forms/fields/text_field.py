from PyQt5.QtCore import QEvent, QObject
from napari_arnheim.widgets.dialogs.forms.fields.base import FieldMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout, QWidget
import namegenerator

class FocusFilter(QObject):


    def __init__(self, *args, on_focus_out = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.on_focus_out = on_focus_out

    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            # do custom stuff
            if self.on_focus_out: self.on_focus_out(event)
            # return False so that the widget will also handle the event
            # otherwise it won't focus out
            return False
        else:
            # we don't care about other events
            return False




class TextField(QLineEdit):

    def __init__(self, initial=None, base=None, on_select=False, **kwargs):
        super().__init__(initial or namegenerator.gen(), **kwargs)

        if on_select:
            self._filter = FocusFilter(on_focus_out=on_select)
            self.installEventFilter(self._filter)


    def getValue(self):
        return str(self.text())