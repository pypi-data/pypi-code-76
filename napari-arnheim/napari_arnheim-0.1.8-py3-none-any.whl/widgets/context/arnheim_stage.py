from napari_arnheim.widgets.lists.generatorlist import GeneratorListWidget
from napari_arnheim.widgets.lists.nodelist import NodeListWidget
from napari_arnheim.widgets.base import BaseWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen.query import QueryList
from bergen.models import Node
from qasync import asyncSlot, asyncClose
from napari_arnheim.widgets.details.rep import RepresentationDetailWidget

class ArnheimStageWidget(BaseWidget):

    
    def __init__(self,  *args, rep = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)




        self.suggestions = NodeListWidget(title="Fitting Nodes", base=self.base)

        self.layout.addWidget(self.suggestions)
        self.layout.update()









    






