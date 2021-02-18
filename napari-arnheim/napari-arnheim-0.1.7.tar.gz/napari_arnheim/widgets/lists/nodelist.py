


from napari_arnheim.widgets.base import BaseWidget
from napari_arnheim.widgets.items.nodeitem import NodeItemWidget
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from bergen.schema import Node
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QWidget
from PyQt5 import QtCore
import typing
from bergen.query import QueryList
from grunnlag.schema import Representation

class NodeListWidget(BaseWidget):


    def __init__(self, title=None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.list = QListWidget()
        self.refreshButton = QPushButton("R")
        self.refreshButton.clicked.connect(self.updateList)
         
        self.layout = QVBoxLayout(self)
        if title:
            self.layout.addWidget(QLabel(title))


        self.layout.addWidget(self.refreshButton)
        self.layout.addWidget(self.list)
        self.updateList()


    def updateList(self):
        self.nodes = QueryList("""query {
                nodes{
                    id
                    name
                }
        }""", Node).run()

        self.list.clear()
        for node in self.nodes:

            item = QListWidgetItem(self.list)
            self.list.addItem(item)
            nodewidget = NodeItemWidget(node, base=self.base)
            item.setSizeHint(nodewidget.minimumSizeHint())
            self.list.setItemWidget(item, nodewidget)





