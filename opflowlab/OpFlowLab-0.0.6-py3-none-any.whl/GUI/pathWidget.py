import os
from pathlib import Path

import qtawesome as qta
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QToolButton, QFileDialog

from .opFlowLabWorker import opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet


class pathWidget(QWidget):
    messageSignal = pyqtSignal(str, str)

    def __init__(self, defaultFolder="", pathtype="folder",
                 filter="TIFF images (*.tif *.tiff);; PNG images (*.png);; JPEG images (*.jpg *.jpeg)",
                 desc=None,
                 ):
        super(QWidget, self).__init__()

        self.path = defaultFolder
        self.pathtype = pathtype
        self.filter = filter
        self.desc = desc
        self.config = opFlowLabConfig()

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Main folder
        self.inputPathLineEdit = QLineEdit(defaultFolder)
        if self.pathtype == "folder":
            self.inputPathLineEdit.setPlaceholderText("Input {} folder path".format(self.desc))
        elif self.pathtype == "file":
            self.inputPathLineEdit.setPlaceholderText("Input {} file path".format(self.desc))
        self.layout.addWidget(self.inputPathLineEdit, 0, 0)
        self.inputButton = QToolButton()
        self.inputButton.setIcon(qta.icon('fa5s.folder', color=QColor("#20639B")))
        self.layout.addWidget(self.inputButton, 0, 1)
        self.setLayout(self.layout)
        self.inputButton.clicked.connect(self.onInputButtonClicked)

        self.inputPathLineEdit.textChanged.connect(self.validatePath)

    def onInputButtonClicked(self):
        path = self.inputPathLineEdit.text()
        if os.path.isdir(path) is False:
            if os.path.isfile(path) is True:
                path = os.path.dirname(path)
            elif self.config.mainFolderPath is None:
                path = str(Path.home())
            else:
                path = self.config.mainFolderPath

        if self.pathtype == "folder":
            filepath = QFileDialog.getExistingDirectory(self, "Choose {} folder".format(self.desc), path)
        elif self.pathtype == "file":
            filepath, filter = QFileDialog.getOpenFileName(self, "Choose {} file".format(self.desc), path, filter=self.filter)

        if filepath:
            self.path = filepath
            self.inputPathLineEdit.setText(filepath)

    def validatePath(self):
        path = self.inputPathLineEdit.text()

        if self.pathtype == "folder":
            if os.path.isdir(path) is False:
                self.inputPathLineEdit.setStyleSheet(invalid_stylesheet)
                self.messageSignal.emit("Please check {} folder path".format(self.desc), "error")
                return False
            else:
                self.path = path
                self.inputPathLineEdit.setStyleSheet(valid_stylesheet)
                return True
        elif self.pathtype == "file":
            if os.path.isfile(path) is False:
                self.inputPathLineEdit.setStyleSheet(invalid_stylesheet)
                self.messageSignal.emit("Please check {} file path".format(self.desc), "error")
                return False
            else:
                self.path = path
                self.inputPathLineEdit.setStyleSheet(valid_stylesheet)
                return True

    def setText(self, text):
        self.inputPathLineEdit.setText(text)

    def getPath(self):
        valid = self.validatePath()
        if valid is True:
            return self.path
        else:
            return None
