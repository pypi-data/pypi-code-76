from napari_arnheim.widgets.context.non_arnheim_stage import NonArnheimStageWidget
from napari_arnheim.widgets.context.arnheim_stage import ArnheimStageWidget
from napari_arnheim.widgets.lists.generatorlist import GeneratorListWidget
from napari_arnheim.widgets.lists.nodelist import NodeListWidget
from napari_arnheim.widgets.base import BaseWidget
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QWidget
from bergen.query import QueryList
from bergen.models import Node
from qasync import asyncSlot, asyncClose
from napari_arnheim.widgets.context.empty_stage import EmptyStageWidget

class ContextAwareWidget(BaseWidget):

    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)

        self.suggestions = QLabel("Waiting for suggestions")
        self.layout.addStretch()
        self.layout.addWidget(self.suggestions)

        self.viewer.events.emitters["active_layer"].connect(self.on_active_layer_changed)
        print("Received here")
        self.rebuildSuggestions()


    def replaceSuggestions(self, newWidget: QWidget):
        self.layout.removeWidget(self.suggestions)
        self.suggestions.close()
        self.suggestions = newWidget
        self.layout.addWidget(self.suggestions)
        self.layout.update()

    def rebuildSuggestions(self):

        if self.viewer.active_layer is not None:
            if "rep" in self.viewer.active_layer.metadata: #TODO: DO this according to the correct Typename
                self.replaceSuggestions(ArnheimStageWidget(base=self.base))
            else:
                self.replaceSuggestions(NonArnheimStageWidget(base=self.base, layer=self.viewer.active_layer))
        else:
            self.replaceSuggestions(EmptyStageWidget(base=self.base))


    def on_active_layer_changed(self, *args, **kwargs):
        self.rebuildSuggestions()
            









    






