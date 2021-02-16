from napari_arnheim.widgets.dialogs.upload import UploadFileDialog
from napari_arnheim.widgets.lists.generatorlist import GeneratorListWidget
from napari_arnheim.widgets.lists.nodelist import NodeListWidget
from napari_arnheim.widgets.base import BaseWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen.query import QueryList
from bergen.models import Node
from qasync import asyncSlot, asyncClose


class NonArnheimStageWidget(BaseWidget):

    
    def __init__(self, *args, layer=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.layer = layer
        self.layout = QHBoxLayout(self)

        self.uploadButton = QPushButton("Upload")
        self.uploadButton.clicked.connect(self.on_uploadButton_clicked)
        self.dialogs = []
        
        self.layout.addWidget(self.uploadButton)
        self.layout.update()

    def on_uploadButton_clicked(self):
        dialog = UploadFileDialog(self, base=self.base, layer=self.layer)
        if dialog.exec_():
            self.helper.openRepresentationAsLayer(rep=dialog.created_rep)  

            









    






