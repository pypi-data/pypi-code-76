from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QCheckBox, QComboBox
from PyQt5.QtCore import Qt


class nvidiaOFOptions(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.presetLabel = QLabel("Optical flow preset")
        self.optionsLayout.addWidget(self.presetLabel, 0, 0)
        self.presetComboBox = QComboBox()
        self.presetComboBox.addItems(["Slow", "Medium", "Fast"])
        self.optionsLayout.addWidget(self.presetComboBox, 1, 0)

        self.temporalCheckBox = QCheckBox("Use temporal hints")
        self.optionsLayout.addWidget(self.temporalCheckBox, 0, 1)

        self.halfPrecisionCheckBox = QCheckBox("Use float16 for outputs")
        self.halfPrecisionCheckBox.setChecked(True)
        self.optionsLayout.addWidget(self.halfPrecisionCheckBox, 1, 1)

        self.costBufferCheckBox = QCheckBox("Output cost buffer")
        self.optionsLayout.addWidget(self.costBufferCheckBox, 2, 1)

        self.reverseCheckBox = QCheckBox("Reverse time direction")
        self.optionsLayout.addWidget(self.reverseCheckBox, 3, 1)

        self.tiffCheckBox = QCheckBox("Save velocity components as tiff file")
        self.optionsLayout.addWidget(self.tiffCheckBox, 4, 1)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

    def getParameters(self):
        preset = self.presetComboBox.currentText()
        temporalHints = self.temporalCheckBox.isChecked()
        costBuffer = self.costBufferCheckBox.isChecked()
        halfPrecision = self.halfPrecisionCheckBox.isChecked()
        isReverse = self.reverseCheckBox.isChecked()
        save_as_tif = self.tiffCheckBox.isChecked()

        return preset, isReverse, temporalHints, halfPrecision, costBuffer, save_as_tif

    def getCommand(self, processPath, imagePath, opticalFlowType):
        processPath = processPath.replace('\\', '/')
        preset, isReverse, temporalHints, halfPrecision, costBuffer, save_as_tif = self.getParameters()

        command = ["\"{}\" {} ".format(processPath, opticalFlowType)
                   + "--perf={} ".format(preset)
                   + "{}".format("--temporal_hints " if temporalHints is True else "")
                   + "{}".format("--cost_buffer " if costBuffer is True else "")
                   + "{}".format("--use_half_precision " if halfPrecision is True else "")
                   + "{}".format("--is_reverse " if isReverse is True else "")
                   + "{}".format("--save_as_img " if save_as_tif is True else "")
                   + "\"{}\"".format(imagePath)]

        param_dict = {"imagePath": imagePath,
                      "type": opticalFlowType,
                      "preset": preset,
                      "temporalHints": temporalHints,
                      "costBuffer": costBuffer,
                      "halfPrecision": halfPrecision,
                      "isReverse": isReverse,
                      "save_as_tif": save_as_tif
                      }

        return command, param_dict