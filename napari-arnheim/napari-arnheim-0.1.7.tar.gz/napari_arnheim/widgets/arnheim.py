from napari_arnheim.widgets.toolbar import ArnheimToolbar
from napari_arnheim.widgets.helper import Helper
import xarray as xr
from bergen.clients.default import Bergen
from bergen.enums import GrantType
from bergen.query import TypedGQL
from bergen.schema import  User
from grunnlag.schema import Representation
from napari.viewer import Viewer
from napari_arnheim.widgets.context.context_aware import ContextAwareWidget
from napari_arnheim.widgets.lists.replist import RepresentationListWidget
from PyQt5.QtWidgets import (QLabel,  QPushButton,
                             QVBoxLayout, QWidget)
from qasync import asyncClose, asyncSlot
import asyncio

class ArnheimWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.status = QLabel(self)
        self.status.text = "Arnheim"

        self._bergen = None # Base Bergen

        self.user_button = QPushButton("Connect")
        self.user_button.clicked.connect(self.connectBergen)

        self.layout.addWidget(self.user_button)
        self.setLayout(self.layout)



    def buildToolbar(self):

        self.toolbar = ArnheimToolbar(self, base=self)
        return self.toolbar



    @property
    def helper(self) -> Helper:
        if hasattr(self.parent(), "qt_viewer"):
            return Helper(self.parent().qt_viewer.viewer)



    @property
    def viewer(self) -> Viewer:
        if hasattr(self.parent(), "qt_viewer"):
            return self.parent().qt_viewer.viewer


    @property
    def bergen(self) -> Bergen:
        if hasattr(self, "_bergen"):
            assert self._bergen is not None, "Please instatiate correctly"
            return self._bergen


    @asyncClose
    async def closeEvent(self, event):
        await self._bergen.disconnect_async()
    

    @asyncSlot()
    async def connectBergen(self):
        if not self._bergen:
            self._bergen = Bergen(host="p-tnagerl-lab1",
                client_id= "huKQboFgvLaqfVb23QAJ7Kchp9Rzl87vCVRgWHjZ",
                port=8000,
                name="karl",
                grant_type = GrantType.IMPLICIT
                # if we want to specifically only use pods on this innstance we would use that it in the selector
            )

            await self._bergen.negotiate_async()


            self.layout.addWidget(self.buildToolbar())
            self.layout.addWidget(self.buildContext())

            user = TypedGQL("""
            query {
                    me {
                        id
                        username
                    }
            }
            """, User).run({})

            self.user_button.setText(f"Logout {user.username}")

        if self._bergen:
            self._bergen = None



    def buildContext(self):
        widget = ContextAwareWidget(base=self)
        return widget

