import os

from OpFlowLab.GUI.pathWidget import pathWidget
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, \
    QVBoxLayout, QGroupBox, QPushButton
from ruamel.yaml import YAML

from .opFlowLabWorker import opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet


class advancedConfigTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.config = opFlowLabConfig()

        self.layout = QVBoxLayout(self)

        self.saveConfigGroup = QGroupBox("Save folder options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.opticalFlowLabel = QLabel("OpFlowLab executable")

        self.optionsLayout.addWidget(self.opticalFlowLabel, 0, 0)
        self.executablePathWidget = pathWidget(pathtype="file",
                                               defaultFolder=self.config.executablePath,
                                               filter="Executable (*.exe);;",
                                               desc="OpFlowLab executable")
        self.optionsLayout.addWidget(self.executablePathWidget, 0, 1)

        self.optionsLayout.addWidget(QLabel("FlowMatch folder"), 1, 0)
        self.flowMatchFolderLineEdit = QLineEdit("FlowMatch")
        self.flowMatchFolderLineEdit.setPlaceholderText("Set name of FlowMatch folder to create")
        self.optionsLayout.addWidget(self.flowMatchFolderLineEdit, 1, 1)

        self.optionsLayout.addWidget(QLabel("FlowPath folder"), 2, 0)
        self.flowPathFolderLineEdit = QLineEdit("FlowPath")
        self.flowPathFolderLineEdit.setPlaceholderText("Set name of FlowPath folder to create")
        self.optionsLayout.addWidget(self.flowPathFolderLineEdit, 2, 1)

        self.optionsLayout.addWidget(QLabel("FlowTracer folder"), 3, 0)
        self.flowTracerFolderLineEdit = QLineEdit("FlowTracer")
        self.flowTracerFolderLineEdit.setPlaceholderText("Set name of FlowTracer folder to create")
        self.optionsLayout.addWidget(self.flowTracerFolderLineEdit, 3, 1)

        self.optionsLayout.addWidget(QLabel("FlowWarp folder"), 4, 0)
        self.flowWarpFolderLineEdit = QLineEdit("FlowWarp")
        self.flowWarpFolderLineEdit.setPlaceholderText("Set name of FlowWarp folder to create")
        self.optionsLayout.addWidget(self.flowWarpFolderLineEdit, 4, 1)

        self.layout.addLayout(self.optionsLayout)
        self.layout.addStretch()

        self.layout.addStretch()

        self.saveButton = QPushButton("Save Settings")
        self.layout.addWidget(self.saveButton)

        self.flowMatchFolderLineEdit.editingFinished.connect(self.updateFlowMatchFolderValue)
        self.flowPathFolderLineEdit.editingFinished.connect(self.updateFlowPathFolderValue)
        self.flowTracerFolderLineEdit.editingFinished.connect(self.updateFlowTracerFolderValue)
        self.flowWarpFolderLineEdit.editingFinished.connect(self.updateFlowWarpFolderValue)

        self.saveButton.clicked.connect(self.onSaveButtonClicked)

        self.executablePathWidget.messageSignal.connect(self.passMessageSignal)

    @pyqtSlot(str, str)
    def passMessageSignal(self, msg, msg_type):
        self.messageSignal.emit(msg, msg_type)

    def updateFlowMatchFolderValue(self):
        folder_name = self.flowMatchFolderLineEdit.text()
        if self.stringCheck(folder_name):
            self.flowMatchFolderLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Invalid folder name entered for FlowMatch folder", "error")
        else:
            self.flowMatchFolderLineEdit.setStyleSheet(valid_stylesheet)

    def updateFlowPathFolderValue(self):
        folder_name = self.flowPathFolderLineEdit.text()
        if self.stringCheck(folder_name):
            self.flowPathFolderLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Invalid folder name entered for FlowPath folder", "error")
        else:
            self.flowPathFolderLineEdit.setStyleSheet(valid_stylesheet)

    def updateFlowTracerFolderValue(self):
        folder_name = self.flowTracerFolderLineEdit.text()
        if self.stringCheck(folder_name):
            self.flowTracerFolderLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Invalid folder name entered for FlowTracer folder", "error")
        else:
            self.flowTracerFolderLineEdit.setStyleSheet(valid_stylesheet)

    def updateFlowWarpFolderValue(self):
        folder_name = self.flowWarpFolderLineEdit.text()
        if self.stringCheck(folder_name):
            self.flowWarpFolderLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Invalid folder name entered for FlowWarp folder", "error")
        else:
            self.flowWarpFolderLineEdit.setStyleSheet(valid_stylesheet)

    def onSaveButtonClicked(self):
        self.config.flowMatch_folder = self.flowMatchFolderLineEdit.text()
        self.config.flowPath_folder = self.flowPathFolderLineEdit.text()
        self.config.flowTracer_folder = self.flowTracerFolderLineEdit.text()
        self.config.flowWarp_folder = self.flowWarpFolderLineEdit.text()
        self.config.executablePath = self.executablePathWidget.getPath()
        self.config.saveSettings()
        self.messageSignal.emit("Settings have been saved to {}".format(self.config.settingsPath), "info")

    @staticmethod
    def stringCheck(text):
        special_characters = "<>:\"\\/|?*"

        if any(c in text for c in special_characters):
            return True
        else:
            return False