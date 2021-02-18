


from napari_arnheim.widgets.base import BaseWidget
from PyQt5.QtWidgets import QVBoxLayout
from napari_arnheim.widgets.items.representaiton import RepresentationItemWidget
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QWidget
from PyQt5 import QtCore
import typing
from bergen.query import QueryList
from grunnlag.schema import Representation

class RepresentationListWidget(BaseWidget):


    def __init__(self, representations: typing.List[Representation] , *args, title=None,  viewer = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.list = QListWidget()


        representations = QueryList("""
            query {
                myrepresentations {
                    id
                    name
                    store
                }
            }
        """)



        for rep in representations:

            item = QListWidgetItem(self.list)
            self.list.addItem(item)
            repwidget = RepresentationItemWidget(rep, base=self.base)
            item.setSizeHint(repwidget.minimumSizeHint())
            self.list.setItemWidget(item, repwidget)

        self.layout = QVBoxLayout(self)
        if title:
            self.layout.addWidget(QLabel(title))
        self.layout.addWidget(self.list)





