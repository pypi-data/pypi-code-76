from napari_arnheim.widgets.utils import replaceWidgetInLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from bergen.query import QueryList
from napari_arnheim.widgets.dialogs.forms.fields.selectors.base import BaseSelector
from napari_arnheim.widgets.base import BaseMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class ArnheimModelSelector(BaseSelector):
    list_query = None
    model = None
    new_form = None
    # can stay not used

    def __init__(self, *args, base, add_none=False, variables=None, with_form=True, on_select=None, **kwargs):
        super().__init__(*args, base=base, **kwargs)
        self.selected_model = None
        self.variables = variables
        self.selector = None
        self.model_selector = None
        self.with_form = with_form
        self.add_none = add_none
        self.on_select= on_select
        self.loadModels()


        self.layout = QHBoxLayout()

        self.setLayout(self.layout)

        self.buildOrReplaceSelector()
        self.buildButton()


    def loadModels(self):
        self.models = QueryList(
            self.list_query,
            self.model).run(
                variables=self.variables
        )

    def requestNewModel(self):
        form = self.new_form(base=self.base, parent=self)
        model = form.getModel()
        if model:
            self.models = [model] + self.models # We are adding it to the first list
            self.buildOrReplaceSelector()

    def buildOrReplaceSelector(self):
        assert self.models is not None, "Please load Models beforee"
 
        model_selector = QComboBox()


        if self.add_none: model_selector.addItem("-----")
        for model in self.models:
            model_selector.addItem(model.name)

        model_selector.currentIndexChanged.connect(self.indexChanged)

        if len(self.models) > 0:
            self.selected_model = self.models[0] # We automatically select the first item once rebuilding

        if not self.model_selector:
            self.layout.addWidget(model_selector)
            self.model_selector = model_selector
        
        else:
            self.layout.replaceWidget(self.model_selector, model_selector)
            self.model_selector.close()
            self.model_selector.setParent(None)
            self.model_selector = model_selector

        self.layout.update()

        return self.model_selector

    def buildButton(self):
        if self.new_form and self.with_form:
            new_model_button = QPushButton("+")
            new_model_button.clicked.connect(self.requestNewModel)
            self.layout.addWidget(new_model_button)
            self.layout.update()


    def indexChanged(self, index):
        if self.add_none: 
            if index == 0:
                self.selected_model = None
            else:
                self.selected_model = self.models[index - 1] # First item is now add 
        else:
            self.selected_model = self.models[index]
        
        if self.on_select: self.on_select(self.selected_model)

    def getValue(self):
        return str(self.selected_model.id) if self.selected_model is not None else None

