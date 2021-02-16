from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from napari_arnheim.widgets.base import BaseMixin
from bergen.query import Query
from grunnlag.schema import Representation

class RepresentationDetailWidget(BaseMixin, QWidget):


    def __init__(self,id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


        rep = Query("""
            query Representation($id: ID!){
                representation(id: $id){
                    store
                    shape
                    sample {
                    name
                    }
                    signature
                    dims
                    name
                    tags
                }
            }
        """, Representation).run(variables={"id": id})

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(rep.name))
        self.layout.addWidget(QLabel(rep.sample.name))
        self.layout.addWidget(QLabel("".join(rep.tags)))
        self.setLayout(self.layout)