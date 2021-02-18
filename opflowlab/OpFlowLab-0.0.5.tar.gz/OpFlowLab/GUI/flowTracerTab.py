from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QProgressBar, QPushButton, QLineEdit, QLabel, \
    QVBoxLayout, QCheckBox, QHBoxLayout, QGroupBox, QComboBox

from .imageViewerWidget import imageViewerWidget
from .opFlowLabWorker import opFlowLabWorker, opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet, stop_button_stylesheet, start_button_stylesheet


class flowTracerTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)
    nextSignal = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.forwardPathLabel = QLabel("Forward velocity field folder: ")
        self.layout.addWidget(self.forwardPathLabel)

        self.segmentationPathLabel = QLabel("Object segmentation folder: ")
        self.layout.addWidget(self.segmentationPathLabel)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.tracerMethods = ["Random tracers", "Grid tracers", "Object centroids"]
        self.randomTracerLayout = QHBoxLayout()
        self.randomTracerLayout.addWidget(QLabel("Tracer generation type"))
        self.randomTracersComboBox = QComboBox()
        self.randomTracersComboBox.addItems(self.tracerMethods)
        self.randomTracerLayout.addWidget(self.randomTracersComboBox)
        self.optionsLayout.addLayout(self.randomTracerLayout, 0, 0)

        self.saveTracerPosCheckBox = QCheckBox("Save initial tracer positions")
        self.saveTracerPosCheckBox.setChecked(True)
        self.optionsLayout.addWidget(self.saveTracerPosCheckBox, 0, 1, 1, -1)

        self.optionsLayout.addWidget(QLabel("Number of tracers"), 1, 0)
        self.tracerNumLineEdit = QLineEdit("10000")
        self.tracerNumLineEdit.setPlaceholderText("Number of tracers")
        self.optionsLayout.addWidget(self.tracerNumLineEdit, 2, 0)

        self.optionsLayout.addWidget(QLabel("Tracer grid spacing"), 1, 1)
        self.spacingLineEdit = QLineEdit("16")
        self.spacingLineEdit.setEnabled(False)
        self.spacingLineEdit.setPlaceholderText("Tracer grid spacing")
        self.optionsLayout.addWidget(self.spacingLineEdit, 2, 1)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

        self.layout.addStretch()

        self.processButton = QPushButton("Generate FlowTracer")
        self.processButton.setEnabled(False)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.processButton)
        self.displayOutput = QPushButton("Display FlowTracer")
        self.displayOutput.setEnabled(False)
        self.buttons.addWidget(self.displayOutput)
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

        self.imageViewer = imageViewerWidget()
        self.colorWheelViewer = imageViewerWidget()

        self.config = opFlowLabConfig()

        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.opFlowLabWorker = opFlowLabWorker()

        # move object to another thread
        self.opFlowLabWorker.moveToThread(self.thread)
        self.opFlowLabWorker.progressSignal.connect(self.updateProgressBar)
        self.killSignal.connect(self.opFlowLabWorker.terminateCalculation)
        self.opFlowLabWorker.finishSignal.connect(self.updateToProcessButton)
        self.opFlowLabWorker.updateSignal.connect(self.updateImageViewer)
        self.opFlowLabWorker.timeSignal.connect(self.updateTimeLeft)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.opFlowLabWorker.runFlowTracer)

        self.processButton.clicked.connect(self.onProcessButtonClicked)
        self.displayOutput.clicked.connect(self.onDisplayOutputButtonClicked)
        self.nextButton.clicked.connect(self.onNextButtonClicked)

        self.randomTracersComboBox.currentTextChanged.connect(self.updateTracerGeneration)
        self.tracerNumLineEdit.editingFinished.connect(self.updateTracerNum)
        self.spacingLineEdit.editingFinished.connect(self.updateSpacingValue)

    @pyqtSlot()
    def updateToProcessButton(self):
        print("Calculation has been stopped")
        self.processButton.setStyleSheet(start_button_stylesheet)
        self.processButton.setText("Generate Flowtracer")
        self.nextButton.setEnabled(True)
        self.thread.quit()

    def onProcessButtonClicked(self):
        if self.thread.isRunning():
            self.killSignal.emit()
            self.thread.quit()
        else:
            valid = True
            self.config.save_initial_tracer_pos = self.saveTracerPosCheckBox.isChecked()
            if self.randomTracersComboBox.currentText() == self.tracerMethods[0]:
                valid = valid and self.updateTracerNum()
            elif self.randomTracersComboBox.currentText() == self.tracerMethods[1]:
                valid = valid and self.updateSpacingValue()
            elif self.randomTracersComboBox.currentText() == self.tracerMethods[2]:
                valid = valid and self.config.segmentationFolderPath is not None

            if self.opFlowLabWorker.isImageLoaded() and self.config.forwardFolderPath is not None:
                if valid is True:
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("Visualizing flow using FlowTracer with the following parameters:", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("------------- Folders ------------", "param")
                    self.messageSignal.emit("Image file path: {}".format(self.config.imageFilePath), "param")
                    self.messageSignal.emit("Forward velocity field folder path: {}".format(self.config.forwardFolderPath), "param")
                    if self.randomTracersComboBox.currentText() == self.tracerMethods[2]:
                        self.messageSignal.emit("Segmentation folder path: {}".format(self.config.segmentationFolderPath), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("----------- Parameters -----------", "param")
                    self.messageSignal.emit("Save initial tracer position: {}".format(self.config.save_initial_tracer_pos), "param")
                    self.messageSignal.emit("Using random tracers: {}".format(self.config.use_random_tracers), "param")
                    if self.randomTracersComboBox.currentText() == self.tracerMethods[0]:
                        self.messageSignal.emit("Number of tracers: {}".format(self.config.tracer_no), "param")
                    elif self.randomTracersComboBox.currentText() == self.tracerMethods[1]:
                        self.messageSignal.emit("Tracer grid spacing: {}".format(self.config.grid_spacing), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("-------- Save parameters ---------", "param")
                    self.messageSignal.emit("Save location: {}".format(self.config.forwardFolderPath + "/" + self.config.flowTracer_folder), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")

                    # save parameters
                    self.config.saveParameters("FlowTracer", ["imageFilePath", "forwardFolderPath", "segmentationFolderPath",
                                                              "save_initial_tracer_pos", "use_random_tracers", "tracer_no",
                                                              "grid_spacing"])
                    # start thread
                    self.thread.start()
                    self.displayOutput.setEnabled(True)
                    self.processButton.setStyleSheet(stop_button_stylesheet)
                    self.processButton.setText("Stop FlowTracer")
                else:
                    self.messageSignal.emit("Please ensure that all inputs are valid", "error")
            else:
                self.messageSignal.emit("Please load image file and forward velocity field folder first!", "error")

    def onFocusUpdate(self):
        self.forwardPathLabel.setText("Forward velocity field folder: {}".format(self.config.forwardFolderPath))
        self.segmentationPathLabel.setText("Object segmentation folder: {}".format(self.config.segmentationFolderPath))
        if self.config.forwardFolderPath is None:
            self.messageSignal.emit("FlowTracer can only be performed when the forward velocity field folder is defined.", "warn")
            self.messageSignal.emit("Please ensure this folder is loaded under the 'Load velocity field' tab.", "warn")
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)

    def updateTracerGeneration(self):
        if self.randomTracersComboBox.currentText() == self.tracerMethods[0]:
            self.tracerNumLineEdit.setEnabled(True)
            self.spacingLineEdit.setEnabled(False)
            self.config.use_random_tracers = True
        elif self.randomTracersComboBox.currentText() == self.tracerMethods[1]:
            self.tracerNumLineEdit.setEnabled(False)
            self.spacingLineEdit.setEnabled(True)
            self.config.use_random_tracers = False
        elif self.randomTracersComboBox.currentText() == self.tracerMethods[2]:
            self.tracerNumLineEdit.setEnabled(False)
            self.spacingLineEdit.setEnabled(False)
            self.config.use_random_tracers = False

    def updateTracerNum(self):
        try:
            tracer_no = int(self.tracerNumLineEdit.text())
            assert tracer_no > 0
            self.config.tracer_no = tracer_no
            self.tracerNumLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.tracerNumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Tracer number should be an integer", "error")
            return False
        except AssertionError:
            self.tracerNumLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Tracer number should be a value greater than 0", "error")
            return False

    def updateSpacingValue(self):
        try:
            grid_spacing = int(self.spacingLineEdit.text())
            assert grid_spacing > 0
            self.config.grid_spacing = grid_spacing
            self.spacingLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.spacingLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Spacing should be an integer", "error")
            return False
        except AssertionError:
            self.spacingLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Spacing should be a value greater than 0", "error")
            return False

    def onDisplayOutputButtonClicked(self):
        self.imageViewer.displayImage()
        self.imageViewer.setWindowTitle("Artificial tracers")
        if self.config.hasInstance():
            self.imageViewer.updateImageViewer(self.config.images)

    def updateImageViewer(self):
        self.imageViewer.updateImageViewer(self.config.images)

    @pyqtSlot(int)
    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot(float)
    def updateTimeLeft(self, value):
        if value > 60:
            self.timeLeft.setText("Time Left: {:.2f} mins".format(value/60))
        else:
            self.timeLeft.setText("Time Left: {:.2f} secs".format(value))

    def onNextButtonClicked(self):
        self.nextSignal.emit()
