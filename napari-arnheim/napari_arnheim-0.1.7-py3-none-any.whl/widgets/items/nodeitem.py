


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

@thread_worker
def run_node(loop, node, *args, **kwargs):
    # We need to run courotine threadsafe because napari uses the gt event loop and bergen is using the asyncio eventloop in the main thread,
    # We are using this thread and await the result here. 
    


    # This is the weirdest thing ever
    if loop.is_running():
        print("Loop alreday running")
        test = asyncio.run_coroutine_threadsafe(node(*args, **kwargs),loop)
        nana = test.result()
    else:
        nana = node(*args, **kwargs)
    # Wait for the result:
    return nana


import logging

logger = logging.getLogger(__name__)



class NodeItemWidget(BaseWidget):
    def __init__(self, node: Node,  *args, **kwargs):
        super(NodeItemWidget, self).__init__( *args, **kwargs)
        self.node = node

        self.node_expanded = None
        self.row = QHBoxLayout()


        self.row.addWidget(QLabel(self.node.name))


        self.open2DButton = QPushButton("Run")
        self.open2DButton.clicked.connect(self.run)
        self.row.addWidget(self.open2DButton)


        self.tasks = []

        #self.open3DButton = QPushButton("3D")
        #self.open3DButton.clicked.connect(self.open3D)
        #self.row.addWidget(self.open3DButton)

        self.setLayout(self.row)

    def on_result(self, outputs):
        if "rep" in outputs:
            rep = outputs["rep"]
            self.helper.openRepresentationAsLayer(rep)


    @asyncClose
    async def closeEvent(self, a0) -> None:
        print("Cancelling all tasks")
        print(self.tasks)
        for task in self.tasks:
            task.cancel()
        return super().closeEvent(a0)


    def on_exception(self, exception):
        ErrorDialog.alert(f"The Assignation terminated with this error {str(exception)}")



    async def callNode(self, node, inputs):
        try:
                print(f"Calling with {inputs}")
                result = await self.node_expanded(inputs)
                print(result)
                self.on_result(result)
        except asyncio.CancelledError:
            print("Canceledd")
        
        except Exception as e:
            self.on_exception(e)


    def run(self):
        active_image = self.viewer.active_layer
        if active_image is None: return ErrorDialog.alert("No Layer selected")
        meta = active_image.metadata
        if "rep" in meta:
            self.node_expanded =  Node.objects.get(id=self.node.id)

            inputs = self.node_expanded.askInputs(forced_values={"rep": meta["rep"].id}, parent=self)
            if inputs:
                task = asyncio.create_task(self.callNode(self.node_expanded, inputs))
                self.tasks.append(task)
            else:
                print("Cancelled")# Not sure if the smartest way?
        else:
            return ErrorDialog.alert("The Layer you selected is not a ArnheimModel")

            # We are dealing with an Image
        
            # Lets first get the Real Node 

            



        