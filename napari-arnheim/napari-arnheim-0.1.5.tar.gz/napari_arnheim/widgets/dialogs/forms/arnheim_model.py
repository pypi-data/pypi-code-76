from typing import Mapping, Type
from bergen.query import AsyncQuery

from bergen.types.model import ArnheimModel
from qasync import asyncSlot
from napari_arnheim.widgets.dialogs.forms.base import BaseForm
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel, QLineEdit, QVBoxLayout, QWidget
import namegenerator
from napari_arnheim.widgets.dialogs.forms.fields.base import FieldMixin
from napari_arnheim.widgets.dialogs.forms.fields.text_field import TextField

class ArnheimModelForm(BaseForm):
    create_mutation = None
    model: Type[ArnheimModel] = None
    fields: Mapping[str, Type[FieldMixin]] = {
        "name": TextField,
    }


    def __init__(self, *args, base, **kwargs):
        assert self.model is not None, "Please provide a Model"
        assert self.create_mutation is not None, "Provide A create Mutation"

        super().__init__(*args, base=base, **kwargs)

        self.formGroupBox = QGroupBox(self.model.__name__)
        layout = QFormLayout()

        self.field_instances = { key: field(self, base=self.base) for key, field in self.fields.items()}

        for fieldname, field in self.field_instances.items():
            layout.addRow(QLabel(fieldname), field)
        
        self.formGroupBox.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.create)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(f"Create a new {self.model.__name__}")

    @asyncSlot()
    async def create(self):

        model = await AsyncQuery(
            self.create_mutation, self.model).run(variables={
            key: field.getValue() for key, field in self.field_instances.items()   
        })
        
        self.created_model = model
        self.accept()


    def getModel(self):
        if self.exec_():
            return self.created_model
        else:
            return None