import re
import numpy as np

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox, QLabel, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt


class dualOptions(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)

        self.tauLabel = QLabel("Time step parameter (tau)")
        self.optionsLayout.addWidget(self.tauLabel, 0, 0)
        self.tauLineEdit = QLineEdit("0.25")
        self.tauLineEdit.setPlaceholderText("Time step parameter (tau)")
        self.optionsLayout.addWidget(self.tauLineEdit, 1, 0)

        self.lambdaLabel = QLabel("Attachment parameter (lambda)")
        self.optionsLayout.addWidget(self.lambdaLabel, 0, 1)
        self.lambdaLineEdit = QLineEdit("0.15")
        self.lambdaLineEdit.setPlaceholderText("Attachment parameter (lambda)")
        self.optionsLayout.addWidget(self.lambdaLineEdit, 1, 1)

        self.thetaLabel = QLabel("Illumination variation parameter (theta)")
        self.optionsLayout.addWidget(self.thetaLabel, 2, 0)
        self.thetaLineEdit = QLineEdit("0.3")
        self.thetaLineEdit.setPlaceholderText("Illumination variation parameter (theta)")
        self.optionsLayout.addWidget(self.thetaLineEdit, 3, 0)

        self.epsilonLabel = QLabel("Stopping criterion threshold (epsilon)")
        self.optionsLayout.addWidget(self.epsilonLabel, 2, 1)
        self.epsilonLineEdit = QLineEdit("0.01")
        self.epsilonLineEdit.setPlaceholderText("Stopping criterion threshold (epsilon)")
        self.optionsLayout.addWidget(self.epsilonLineEdit, 3, 1)

        self.gammaLabel = QLabel("Tightness parameter (gamma)")
        self.optionsLayout.addWidget(self.gammaLabel, 4, 0)
        self.gammaLineEdit = QLineEdit("0.0")
        self.gammaLineEdit.setPlaceholderText("Tightness parameter (gamma)")
        self.optionsLayout.addWidget(self.gammaLineEdit, 5, 0)

        self.iterationsLabel = QLabel("Num of iterations")
        self.optionsLayout.addWidget(self.iterationsLabel, 4, 1)
        self.iterationsLineEdit = QLineEdit("300")
        self.iterationsLineEdit.setPlaceholderText("Number of iterations")
        self.optionsLayout.addWidget(self.iterationsLineEdit, 5, 1)

        self.numLevelsLabel = QLabel("Num pyramidal levels")
        self.optionsLayout.addWidget(self.numLevelsLabel, 6, 0)
        self.levelsLineEdit = QLineEdit("5")
        self.levelsLineEdit.setPlaceholderText("Num pyramidal levels")
        self.optionsLayout.addWidget(self.levelsLineEdit, 7, 0)

        self.warpsLabel = QLabel("Num warpings per scale")
        self.optionsLayout.addWidget(self.warpsLabel, 6, 1)
        self.warpsLineEdit = QLineEdit("5")
        self.warpsLineEdit.setPlaceholderText("Pyramidal scale factor")
        self.optionsLayout.addWidget(self.warpsLineEdit, 7, 1)

        self.scaleLabel = QLabel("Pyramidal scale factor")
        self.optionsLayout.addWidget(self.scaleLabel, 8, 0)
        self.scaleLineEdit = QLineEdit("0.8")
        self.scaleLineEdit.setPlaceholderText("Pyramidal scale factor")
        self.optionsLayout.addWidget(self.scaleLineEdit, 9, 0)

        self.halfPrecisionCheckBox = QCheckBox("Use float16 for outputs")
        self.halfPrecisionCheckBox.setChecked(True)
        self.optionsLayout.addWidget(self.halfPrecisionCheckBox, 8, 1)

        self.reverseCheckBox = QCheckBox("Reverse time direction")
        self.optionsLayout.addWidget(self.reverseCheckBox, 9, 1)

        self.tiffCheckBox = QCheckBox("Save velocity components as tiff file")
        self.optionsLayout.addWidget(self.tiffCheckBox, 10, 1)

        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

    def prepParameters(self, text, type):
        parameter = re.split('[:,-]', text)
        parameter = [type(x) for x in parameter]

        if len(parameter) == 1:
            return parameter
        else:
            return np.arange(*parameter).tolist()

    def getParameters(self):
        tau = self.prepParameters(self.tauLineEdit.text(), float)
        lam = self.prepParameters(self.lambdaLineEdit.text(), float)
        theta = self.prepParameters(self.thetaLineEdit.text(), float)

        epsilon = self.prepParameters(self.epsilonLineEdit.text(), float)
        gamma = self.prepParameters(self.gammaLineEdit.text(), float)
        iterations = self.prepParameters(self.iterationsLineEdit.text(), int)

        levels = self.prepParameters(self.levelsLineEdit.text(), int)
        warps = self.prepParameters(self.warpsLineEdit.text(), int)
        scale = self.prepParameters(self.scaleLineEdit.text(), float)

        halfPrecision = self.halfPrecisionCheckBox.isChecked()
        isReverse = self.reverseCheckBox.isChecked()
        save_as_tif = self.tiffCheckBox.isChecked()

        return tau, lam, theta, epsilon, gamma, iterations, levels, warps, scale, isReverse, halfPrecision, save_as_tif

    def getCommand(self, processPath, imagePath, opticalFlowType):
        processPath = processPath.replace('\\', '/')
        tau, lam, theta, epsilon, gamma, iterations, levels, warps, scale, isReverse, halfPrecision, save_as_tif = self.getParameters()

        command = []
        for _tau in tau:
            for _lambda in lam:
                for _theta in theta:
                    for _epsilon in epsilon:
                        for _gamma in gamma:
                            for _numIters in iterations:
                                for _numLevels in levels:
                                    for _numWarps in warps:
                                        for _pyrScale in scale:
                                            command.append("\"{}\" {} ".format(processPath, opticalFlowType)
                                                           + "--tau={} ".format(_tau)
                                                           + "--lambda={} ".format(_lambda)
                                                           + "--theta={} ".format(_theta)
                                                           + "--epsilon={} ".format(_epsilon)
                                                           + "--gamma={} ".format(_gamma)
                                                           + "--numIters={} ".format(_numIters)
                                                           + "--numLevels={} ".format(_numLevels)
                                                           + "--numWarps={} ".format(_numWarps)
                                                           + "--pyrScale={} ".format(_pyrScale)
                                                           + "{}".format("--use_half_precision " if halfPrecision is True else "")
                                                           + "{}".format("--is_reverse " if isReverse is True else "")
                                                           + "{}".format("--save_as_img " if save_as_tif is True else "")
                                                           + "\"{}\"".format(imagePath))

        param_dict = {"imagePath": imagePath,
                      "type": opticalFlowType,
                      "tau": tau,
                      "lambda": lam,
                      "theta": theta,
                      "epsilon": epsilon,
                      "gamma": gamma,
                      "numIters": iterations,
                      "numLevels": levels,
                      "numWarps": warps,
                      "pyrScale": scale,
                      "halfPrecision": halfPrecision,
                      "is_reverse": isReverse,
                      "save_as_tif": save_as_tif
                      }

        return command, param_dict