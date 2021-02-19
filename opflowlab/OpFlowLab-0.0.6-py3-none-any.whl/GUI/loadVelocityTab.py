from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QGroupBox, QComboBox, QLabel, QPushButton, QVBoxLayout, \
    QHBoxLayout, QCheckBox

from .opFlowLabWorker import opFlowLabConfig
from .pathWidget import pathWidget
from .styleSheet import invalid_stylesheet, valid_stylesheet


class loadVelocityTab(QWidget):
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.default_forward = 'NvidiaOF_Slow'
        self.default_reverse = 'reverse/NvidiaOF_Slow'

        self.config = opFlowLabConfig()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self.foldersLayout = QGridLayout()
        # Forward velocity folder
        self.forwardFolderWidget = pathWidget(pathtype="folder", defaultFolder="", desc="forward velocities")
        self.foldersLayout.addWidget(QLabel("Forward velocity field folder"), 0, 1)
        self.foldersLayout.addWidget(self.forwardFolderWidget, 0, 2)

        self.reverseFolderCheckBox = QCheckBox()
        self.foldersLayout.addWidget(self.reverseFolderCheckBox, 1, 0)
        self.reverseFolderWidget = pathWidget(pathtype="folder", defaultFolder="", desc="reverse velocities")
        self.reverseFolderWidget.setDisabled(True)
        self.foldersLayout.addWidget(QLabel("Reverse velocity field folder"), 1, 1)
        self.foldersLayout.addWidget(self.reverseFolderWidget, 1, 2)

        self.segmentationFolderCheckBox = QCheckBox()
        self.foldersLayout.addWidget(self.segmentationFolderCheckBox, 2, 0)
        self.segmentationFolderWidget = pathWidget(pathtype="folder", defaultFolder="", desc="object segmentation")
        self.segmentationFolderWidget.setDisabled(True)
        self.foldersLayout.addWidget(QLabel("Object segmentation folder"), 2, 1)
        self.foldersLayout.addWidget(self.segmentationFolderWidget, 2, 2)

        self.layout.addLayout(self.foldersLayout)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.typeLabel = QLabel("Velocity type")
        self.optionsLayout.addWidget(self.typeLabel, 0, 0)
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(["Dense", "Sparse"])
        self.optionsLayout.addWidget(self.typeComboBox, 1, 0)

        self.dtypeLabel = QLabel("Velocity data type")
        self.optionsLayout.addWidget(self.dtypeLabel, 0, 1)
        self.dtypeComboBox = QComboBox()
        self.dtypeComboBox.addItems(["float16", "float32"])
        self.optionsLayout.addWidget(self.dtypeComboBox, 1, 1)

        self.extensionLabel = QLabel("Extension type")
        self.optionsLayout.addWidget(self.extensionLabel, 0, 2)
        self.extensionComboBox = QComboBox()
        self.extensionComboBox.addItems(["*.bin", "*.mat"])
        self.optionsLayout.addWidget(self.extensionComboBox, 1, 2)

        self.optionsLayout.addWidget(QLabel("Median filter kernel size [px]"), 2, 0, 1, -1)
        self.kernelSizeLineEdit = QLineEdit("5")
        self.kernelSizeLineEdit.setPlaceholderText("Median filter kernel size")
        self.optionsLayout.addWidget(self.kernelSizeLineEdit, 3, 0, 1, -1)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

        self.layout.addStretch()

        self.buttons = QHBoxLayout()
        self.initializeButton = QPushButton("Import velocities")
        self.buttons.addWidget(self.initializeButton)
        self.nextButton = QPushButton("Next " + u'\u2794')
        self.nextButton.setMaximumWidth(80)
        self.buttons.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        self.layout.addLayout(self.buttons)

        self.initializeButton.clicked.connect(self.onInitializeButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)

        self.kernelSizeLineEdit.editingFinished.connect(self.updateKernelValue)
        self.forwardFolderWidget.messageSignal.connect(self.passMessageSignal)
        self.reverseFolderWidget.messageSignal.connect(self.passMessageSignal)
        self.segmentationFolderWidget.messageSignal.connect(self.passMessageSignal)
        self.reverseFolderCheckBox.stateChanged.connect(self.setStatusReverseCheckbox)
        self.segmentationFolderCheckBox.stateChanged.connect(self.setStatusSegmentationCheckbox)

    @pyqtSlot(str, str)
    def passMessageSignal(self, msg, msg_type):
        self.messageSignal.emit(msg, msg_type)

    def onFocusUpdate(self):
        self.forwardFolderWidget.setText(self.config.forwardFolderPath)

    def onInitializeButtonClicked(self):
        if self.config.hasInstance():
            valid = self.forwardFolderWidget.validatePath()
            valid = valid and self.updateKernelValue()
            if self.reverseFolderCheckBox.isChecked():
                valid = valid and self.reverseFolderWidget.validatePath()
            if self.segmentationFolderCheckBox.isChecked():
                valid = valid and self.segmentationFolderWidget.validatePath()

            if valid is True:
                self.config.forwardFolderPath = self.forwardFolderWidget.getPath()
                self.config.setattr("velocity_type", self.typeComboBox.currentText().lower())
                self.config.setattr("velocity_dtype", self.dtypeComboBox.currentText().lower())
                self.config.setattr("velocity_ext_type", self.extensionComboBox.currentText().lower())
                self.config.getInstance().initialize_forward_velocities(self.config.forwardFolderPath)

                self.messageSignal.emit("Forward velocity loading completed", "load")
                self.messageSignal.emit("Forward velocity folder path: {}".format(self.config.forwardFolderPath), "load")

                if self.reverseFolderCheckBox.isChecked():
                    self.config.reverseFolderPath = self.reverseFolderWidget.getPath()
                    self.config.getInstance().initialize_reverse_velocities(self.config.reverseFolderPath)
                    self.messageSignal.emit("Reverse velocity loading completed", "load")
                    self.messageSignal.emit(
                        "Reverse velocity folder path: {}".format(self.config.reverseFolderPath), "load")
                if self.segmentationFolderCheckBox.isChecked():
                    self.config.segmentationFolderPath = self.segmentationFolderWidget.getPath()
                    self.config.getInstance().initialize_segmentation_folder(
                        self.config.segmentationFolderPath)
                    self.messageSignal.emit("Object segmentation loading completed", "load")
                    self.messageSignal.emit(
                        "Object segmentation folder path: {}".format(self.config.segmentationFolderPath), "load")

                # save parameters
                self.config.saveParameters("Load Velocity", ["forwardFolderPath", "reverseFolderPath",
                                                             "segmentationFolderPath",
                                                             "velocity_type", "velocity_dtype",
                                                             "velocity_ext_type"])

                self.nextButton.setEnabled(True)
            else:
                self.messageSignal.emit("Please ensure that all inputs are valid", "error")
        else:
            self.messageSignal.emit("Please load image file first!", "error")

    def updateKernelValue(self):
        if self.config.hasInstance():
            try:
                kernel_size = self.kernelSizeLineEdit.text()
                if kernel_size.lower() == "none":
                    kernel_size = None
                else:
                    kernel_size = int(kernel_size)
                    assert kernel_size > 0
                self.config.setattr("kernel_size", kernel_size)
                self.kernelSizeLineEdit.setStyleSheet(valid_stylesheet)
                return True
            except ValueError:
                self.kernelSizeLineEdit.setStyleSheet(invalid_stylesheet)
                self.messageSignal.emit("Kernel size should be an integer or \"None\"", "error")
                return False
            except AssertionError:
                self.kernelSizeLineEdit.setStyleSheet(invalid_stylesheet)
                self.messageSignal.emit("Kernel size should be a value greater than 0", "error")
                return False

    def setStatusReverseCheckbox(self):
        if self.reverseFolderCheckBox.isChecked() is True:
            self.reverseFolderWidget.setEnabled(True)
        else:
            self.reverseFolderWidget.setDisabled(True)

    def setStatusSegmentationCheckbox(self):
        if self.segmentationFolderCheckBox.isChecked() is True:
            self.segmentationFolderWidget.setEnabled(True)
        else:
            self.segmentationFolderWidget.setDisabled(True)

    def onNextButtonClicked(self):
        self.nextSignal.emit()
