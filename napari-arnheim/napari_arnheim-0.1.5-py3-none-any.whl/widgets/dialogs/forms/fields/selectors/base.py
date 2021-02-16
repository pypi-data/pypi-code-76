from napari_arnheim.widgets.base import BaseMixin
from napari_arnheim.widgets.dialogs.forms.fields.base import FieldMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout, QWidget

class BaseSelector(BaseMixin, FieldMixin, QWidget):
    pass

    def __init__(self, *args, base, **kwargs):
        self.serialized_value = None
        super().__init__(*args, base=base, **kwargs)


    def getValue(self):
        return self.serialized_value
