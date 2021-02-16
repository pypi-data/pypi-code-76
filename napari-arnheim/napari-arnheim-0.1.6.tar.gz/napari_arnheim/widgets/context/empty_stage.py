from napari_arnheim.widgets.lists.generatorlist import GeneratorListWidget
from napari_arnheim.widgets.lists.nodelist import NodeListWidget
from napari_arnheim.widgets.base import BaseWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen.query import QueryList
from bergen.models import Node
from qasync import asyncSlot, asyncClose


class EmptyStageWidget(BaseWidget):

    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout(self)

        generators = QueryList("""query {
                generators {
                    id
                    name
                }
            }""", Node).run()


        self.generators = GeneratorListWidget(generators, title="Generate Data", base=self.base)
        self.layout.addWidget(self.generators)
        self.layout.update()









    






