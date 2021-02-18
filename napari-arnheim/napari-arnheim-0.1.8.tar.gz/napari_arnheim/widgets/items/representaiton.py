


from napari_arnheim.widgets.base import BaseWidget
from napari_arnheim.registries.napari import get_current_viewer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget
from grunnlag.schema import Representation
from napari.viewer import Viewer

class RepresentationItemWidget(BaseWidget):
    def __init__(self, rep: Representation, *args, **kwargs):
        super(RepresentationItemWidget, self).__init__( *args, **kwargs)
        self.rep = rep


        self.row = QHBoxLayout()
        self.row.addWidget(QLabel(self.rep.name))
        self.row.addWidget(QLabel("".join(self.rep.tags)))

        #self.open3DButton = QPushButton("3D")
        #self.open3DButton.clicked.connect(self.open3D)
        #self.row.addWidget(self.open3DButton)

        self.setLayout(self.row)




        