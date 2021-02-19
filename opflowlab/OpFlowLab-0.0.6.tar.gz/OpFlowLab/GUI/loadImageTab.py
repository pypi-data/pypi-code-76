import os

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from .imageViewerWidget import imageViewerWidget
from .opFlowLabWorker import opFlowLabConfig
from .pathWidget import pathWidget


class loadImageTab(QWidget):
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.config = opFlowLabConfig()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.optionsLayout = QGridLayout()
        # Image File
        self.imageFileWidget = pathWidget(pathtype="file", defaultFolder="", desc="image")
        self.optionsLayout.addWidget(QLabel("Image file path"), 0, 0)
        self.optionsLayout.addWidget(self.imageFileWidget, 0, 1)
        self.layout.addLayout(self.optionsLayout)
        self.layout.addStretch()

        self.buttons = QHBoxLayout()
        self.initializeButton = QPushButton("Load image")
        self.buttons.addWidget(self.initializeButton)
        self.displayOutput = QPushButton("Display loaded image")
        self.buttons.addWidget(self.displayOutput)
        self.displayOutput.setEnabled(False)
        self.nextButton = QPushButton("Next " + u'\u2794')
        self.nextButton.setMaximumWidth(80)
        self.buttons.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        self.layout.addLayout(self.buttons)

        self.imageViewer = imageViewerWidget()

        self.initializeButton.clicked.connect(self.onInitializeButtonClicked)
        self.displayOutput.clicked.connect(self.onDisplayOutputButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)
        self.imageFileWidget.messageSignal.connect(self.passMessageSignal)

    @pyqtSlot(str, str)
    def passMessageSignal(self, msg, msg_type):
        self.messageSignal.emit(msg, msg_type)

    def onInitializeButtonClicked(self):
        valid = self.imageFileWidget.validatePath()
        if valid is True:
            self.config.imageFilePath = self.imageFileWidget.getPath()
            self.config.mainFolderPath = os.path.dirname(self.config.imageFilePath)

            self.config.initialize()
            self.displayOutput.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.initializeButton.setText("Reload image")

            self.messageSignal.emit("Image loading completed", "load")
            self.messageSignal.emit("Image file path: {}".format(self.config.imageFilePath), "load")
        else:
            self.messageSignal.emit("Please ensure that all inputs are valid", "error")

    def onDisplayOutputButtonClicked(self):
        self.imageViewer.displayImage()
        self.imageViewer.setWindowTitle("Image")
        if self.config.hasInstance():
            self.imageViewer.updateImageViewer(self.config.getInstance().image)

    def onNextButtonClicked(self):
        self.nextSignal.emit()
