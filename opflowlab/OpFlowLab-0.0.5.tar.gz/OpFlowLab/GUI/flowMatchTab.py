from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QProgressBar, QPushButton, QLineEdit, QLabel, \
    QVBoxLayout, QCheckBox, QHBoxLayout, QGroupBox

from .opFlowLabWorker import opFlowLabWorker, opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet, start_button_stylesheet, stop_button_stylesheet


class flowMatchTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.config = opFlowLabConfig()

        self.layout = QVBoxLayout(self)

        self.forwardPathLabel = QLabel("Forward velocity field folder: ")
        self.layout.addWidget(self.forwardPathLabel)

        self.reversePathLabel = QLabel("Reverse velocity field folder: ")
        self.layout.addWidget(self.reversePathLabel)

        self.segmentationPathLabel = QLabel("Object segmentation folder: ")
        self.layout.addWidget(self.segmentationPathLabel)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsLayout.addWidget(QLabel("Pairwise threshold distance"), 0, 0)
        self.pairwiseLineEdit = QLineEdit("10")
        self.pairwiseLineEdit.setPlaceholderText("Pairwise threshold distance")
        self.optionsLayout.addWidget(self.pairwiseLineEdit, 1, 0)
        self.optionsLayout.addWidget(QLabel("Minimum object size"), 2, 0)
        self.minimumLineEdit = QLineEdit("None")
        self.minimumLineEdit.setPlaceholderText("Minimum object size")
        self.optionsLayout.addWidget(self.minimumLineEdit, 3, 0)
        self.optionsLayout.addWidget(QLabel("Maximum object size"), 2, 1)
        self.maximumLineEdit = QLineEdit("None")
        self.maximumLineEdit.setPlaceholderText("Maximum object size")
        self.optionsLayout.addWidget(self.maximumLineEdit, 3, 1)
        self.tiffCheckBox = QCheckBox("Save velocity components as 32bit tiff")
        self.optionsLayout.addWidget(self.tiffCheckBox, 4, 0)
        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

        self.layout.addStretch()

        self.processButton = QPushButton("Perform FlowMatch")
        self.processButton.setEnabled(False)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.processButton)
        self.nextButton = QPushButton("Next " + u'\u2794')
        self.nextButton.setMaximumWidth(80)
        self.buttons.addWidget(self.nextButton)
        self.nextButton.setEnabled(False)
        self.layout.addLayout(self.buttons)

        self.progressBarLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBarLayout.addWidget(QLabel("Progress:"))
        self.progressBarLayout.addWidget(self.progressBar)
        self.timeLeft = QLabel("Time Left:")
        self.timeLeft.setMinimumWidth(120)
        self.progressBarLayout.addWidget(self.timeLeft)
        self.layout.addLayout(self.progressBarLayout)

        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.opFlowLabWorker = opFlowLabWorker()

        # move object to another thread
        self.opFlowLabWorker.moveToThread(self.thread)
        self.opFlowLabWorker.progressSignal.connect(self.updateProgressBar)
        self.killSignal.connect(self.opFlowLabWorker.terminateCalculation)
        self.opFlowLabWorker.finishSignal.connect(self.updateProcessButton)
        self.opFlowLabWorker.timeSignal.connect(self.updateTimeLeft)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.opFlowLabWorker.runFlowMatch)

        self.processButton.clicked.connect(self.onProcessButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)

        self.pairwiseLineEdit.editingFinished.connect(self.updatePairwiseValue)
        self.minimumLineEdit.editingFinished.connect(self.updateMinValue)
        self.maximumLineEdit.editingFinished.connect(self.updateMaxValue)

    @pyqtSlot()
    def updateProcessButton(self):
        print("Calculation has been stopped")
        self.processButton.setStyleSheet(start_button_stylesheet)
        self.processButton.setText("Perform FlowMatch")
        self.nextButton.setEnabled(True)
        self.thread.terminate()

    def onProcessButtonClicked(self):
        if self.thread.isRunning():
            print("Process will be stopped once the current frame is completed.")
            self.killSignal.emit()
            self.thread.terminate()
        else:
            if self.opFlowLabWorker.isImageLoaded() and \
                    self.config.forwardFolderPath is not None and \
                    self.config.reverseFolderPath is not None and \
                    self.config.segmentationFolderPath is not None:
                valid = self.updatePairwiseValue()
                valid = valid and self.updateMinValue()
                valid = valid and self.updateMaxValue()

                self.config.save_velocities_as_tif = self.tiffCheckBox.isChecked()

                if valid is True:
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("Performing FlowMatch with the following parameters:", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("------------- Folders ------------", "param")
                    self.messageSignal.emit("Image file path: {}".format(self.config.imageFilePath), "param")
                    self.messageSignal.emit("Forward velocity field folder path: {}".format(self.config.forwardFolderPath), "param")
                    self.messageSignal.emit("Reverse velocity field folder path: {}".format(self.config.reverseFolderPath), "param")
                    self.messageSignal.emit("Segmentation folder path: {}".format(self.config.segmentationFolderPath), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("----------- Parameters -----------", "param")
                    self.messageSignal.emit("Pairwise threshold value: {}".format(self.config.pairwise_threshold_distance), "param")
                    self.messageSignal.emit("Minimum object size: {}".format(self.config.min_object_size), "param")
                    self.messageSignal.emit("Maximum object size: {}".format(self.config.max_object_size), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("-------- Save parameters ---------", "param")
                    self.messageSignal.emit("Save location: {}".format(self.config.forwardFolderPath + "/" + self.config.flowMatch_folder), "param")
                    self.messageSignal.emit("Saving as {} file".format(".tif" if self.config.save_velocities_as_tif else ".bin"), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    # save parameters
                    self.config.saveParameters("FlowMatch", ["forwardFolderPath", "reverseFolderPath", "segmentationFolderPath",
                                                             "pairwise_threshold_distance", "min_object_size", "max_object_size",
                                                             "save_velocities_as_tif"])

                    # start thread
                    self.thread.start()
                    self.processButton.setStyleSheet(stop_button_stylesheet)
                    self.processButton.setText("Stop FlowMatch")
                else:
                    self.messageSignal.emit("Please ensure that all inputs are valid", "error")
            else:
                self.messageSignal.emit("Please load image file and/or forward velocity field folder first!", "error")

    def onFocusUpdate(self):
        self.forwardPathLabel.setText("Forward velocity field folder: {}".format(self.config.forwardFolderPath))
        self.reversePathLabel.setText("Reverse velocity field folder: {}".format(self.config.reverseFolderPath))
        self.segmentationPathLabel.setText("Object segmentation folder: {}".format(self.config.segmentationFolderPath))
        if self.config.forwardFolderPath is None or self.config.reverseFolderPath is None or self.config.segmentationFolderPath is None:
            self.messageSignal.emit("FlowMatch can only be performed when the forward velocity field folder, reverse velocity field folder and object segmentation folder are defined.", "warn")
            self.messageSignal.emit("Please ensure these folders are loaded under the 'Load velocity field' tab.", "warn")
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)

    def updatePairwiseValue(self):
        try:
            pairwise_distance = float(self.pairwiseLineEdit.text())
            assert pairwise_distance > 0
            self.config.pairwise_threshold_distance = pairwise_distance
            self.pairwiseLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.pairwiseLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Pairwise distance should be an integer", "error")
            return False
        except AssertionError:
            self.pairwiseLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Pairwise distance should be a value greater than 0", "error")
            return False

    def updateMinValue(self):
        try:
            minimum_size = self.minimumLineEdit.text()
            if minimum_size.lower() == "none":
                minimum_size = None
            else:
                minimum_size = int(minimum_size)
                assert minimum_size > 0
                if self.config.max_object_size is not None:
                    assert minimum_size < self.config.max_object_size
            self.config.min_object_size = minimum_size
            self.minimumLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.minimumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Minimum object size should be an integer or \"None\"", "error")
            return False
        except AssertionError:
            self.minimumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Minimum object size should be a value greater than 0 amd smaller than maximum object size", "error")
            return False

    def updateMaxValue(self):
        try:
            maximum_size = self.maximumLineEdit.text()
            if maximum_size.lower() == "none":
                maximum_size = None
            else:
                maximum_size = int(maximum_size)
                assert maximum_size > 0
                if self.config.min_object_size is not None:
                    assert maximum_size > self.config.min_object_size
            self.config.max_object_size = maximum_size
            self.maximumLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.maximumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Maximum object size should be an integer or \"None\"", "error")
            return False
        except:
            self.maximumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Maximum object size should be a value greater than 0 amd larger than minimum object size", "error")
            return False

    @pyqtSlot(int)
    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot(float)
    def updateTimeLeft(self, value):
        if value > 60:
            self.timeLeft.setText("Time Left: {:.2f} mins".format(value / 60))
        else:
            self.timeLeft.setText("Time Left: {:.2f} secs".format(value))

    def onNextButtonClicked(self):
        self.nextSignal.emit()
