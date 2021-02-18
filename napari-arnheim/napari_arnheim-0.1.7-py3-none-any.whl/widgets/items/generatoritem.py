


from PyQt5.QtCore import QXmlStreamNotationDeclaration
from napari_arnheim.widgets.base import BaseWidget
from napari_arnheim.widgets.error.error import ErrorDialog
from bergen.models import Node
from napari_arnheim.registries.napari import get_current_viewer
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QWidget
from grunnlag.schema import Representation
from napari.viewer import Viewer
import asyncio
from napari.qt.threading import thread_worker
from qasync import asyncSlot, asyncClose




class GeneratorItemWidget(BaseWidget):
    def __init__(self, node: Node,  *args, **kwargs):
        super(GeneratorItemWidget, self).__init__( *args, **kwargs)
        self.node = node

        self.node_expanded = None
        self.row = QHBoxLayout()


        self.row.addWidget(QLabel(self.node.name))


        self.open2DButton = QPushButton("Run")
        self.open2DButton.clicked.connect(self.run)
        self.row.addWidget(self.open2DButton)

        #self.open3DButton = QPushButton("3D")
        #self.open3DButton.clicked.connect(self.open3D)
        #self.row.addWidget(self.open3DButton)

        self.setLayout(self.row)

    def print_result(self, outputs):
        if "rep" in outputs:
            rep = outputs["rep"]
            self.viewer.add_image(rep.data.sel(c=0).data, name=rep.name, metadata={"rep": rep})


    @asyncClose
    async def closeEvent(self, a0) -> None:
        return super().closeEvent(a0)


    def on_exception(self, exception):
        ErrorDialog.alert(f"The Assignation terminated with this error {str(exception)}")

    @asyncSlot()
    async def run(self):
        self.node_expanded = await Node.asyncs.get(id=self.node.id)
        try:
            result = await self.node_expanded({})
            self.print_result(result)
        except Exception as e:
            self.on_exception(e)
            



        