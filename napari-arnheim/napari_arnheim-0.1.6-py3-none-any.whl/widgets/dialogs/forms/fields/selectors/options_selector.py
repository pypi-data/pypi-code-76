from napari_arnheim.widgets.utils import replaceWidgetInLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from bergen.query import QueryList
from napari_arnheim.widgets.dialogs.forms.fields.selectors.base import BaseSelector
from napari_arnheim.widgets.base import BaseMixin
from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class OptionsSelector(BaseSelector):
    options = None
    # can stay not used

    def __init__(self, *args, base, options=None, add_none=False, on_select=None, **kwargs):
        super().__init__(*args, base=base, **kwargs)
        self.add_none = add_none
        self.on_select= on_select
        self.options = options or self.options
        self.option_items = list(options.items())
        self.options_selector = None
        assert self.options is not None, "Please provide either options as argument or subclass"

        self.layout = QHBoxLayout()

        self.setLayout(self.layout)

        self.buildOrReplaceSelector()


    def buildOrReplaceSelector(self):

        options_selector = QComboBox()

        if self.add_none: options_selector.addItem("-----")
        for key, option in self.option_items:
            options_selector.addItem(option)

        options_selector.currentIndexChanged.connect(self.indexChanged)

        if len(self.option_items) > 0 and not self.add_none:
            self.selected_option = self.option_items[0][0] # We automatically select the first item once rebuilding

        if not self.options_selector:
            self.layout.addWidget(options_selector)
            self.model_selector = options_selector
        
        else:
            self.layout.replaceWidget(self.options_selector, options_selector)
            self.model_selector.close()
            self.model_selector.setParent(None)
            self.model_selector = options_selector

        self.layout.update()

        return self.options_selector

    def indexChanged(self, index):
        if self.add_none: 
            if index == 0:
                self.selected_option = None
            else:
                self.selected_option = self.option_items[index - 1][0] # First item is the key not the label
        else: 
            self.selected_option = self.option_items[index][0]
        
        if self.on_select: self.on_select(self.selected_option)

    def getValue(self):
        return self.selected_option

