


from napari_arnheim.widgets.items.generatoritem import GeneratorItemWidget
from napari_arnheim.widgets.base import BaseWidget
from napari_arnheim.widgets.items.nodeitem import NodeItemWidget
from PyQt5.QtWidgets import QVBoxLayout
from bergen.schema import Node
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QWidget
from PyQt5 import QtCore
import typing

from grunnlag.schema import Representation

class GeneratorListWidget(BaseWidget):


    def __init__(self, nodes: typing.List[Node] ,  *args, title=None, **kwargs) -> None:
        super().__init__( *args, **kwargs)

        self.list = QListWidget()

        for node in nodes:

            item = QListWidgetItem(self.list)
            self.list.addItem(item)
            nodewidget = GeneratorItemWidget(node, base=self.base)
            item.setSizeHint(nodewidget.minimumSizeHint())
            self.list.setItemWidget(item, nodewidget)

        self.layout = QVBoxLayout(self)
        if title:
            self.layout.addWidget(QLabel(title))
        self.layout.addWidget(self.list)





