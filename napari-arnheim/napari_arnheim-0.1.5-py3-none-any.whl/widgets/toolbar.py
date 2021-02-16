from napari_arnheim.widgets.dialogs.select_rep import RepresentationSelectorDialog
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from napari_arnheim.widgets.base import BaseMixin
from PyQt5.QtWidgets import QDialogButtonBox, QHBoxLayout, QPushButton, QWidget

class ArnheimToolbar(BaseMixin, QWidget):


    def __init__(self, *args, layer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer

        self.openRepresentationButton = QPushButton("Rep")
        self.openRepresentationButton.clicked.connect(self.openRepSelector)
        self.openSampleButton = QPushButton("Samples")

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.openRepresentationButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.openSampleButton, QDialogButtonBox.ActionRole)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)


    def openRepSelector(self, *args, **kwargs):
        rep = RepresentationSelectorDialog(self, base=self.base)
        if rep.exec_():
            for rep in rep.selected_reps:
                self.helper.openRepresentationAsLayer(rep)
              