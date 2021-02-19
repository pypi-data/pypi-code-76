# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_echoes_patches.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_PresetEchoesPatches(object):
    def setupUi(self, PresetEchoesPatches):
        if not PresetEchoesPatches.objectName():
            PresetEchoesPatches.setObjectName(u"PresetEchoesPatches")
        PresetEchoesPatches.resize(466, 454)
        self.centralWidget = QWidget(PresetEchoesPatches)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.include_menu_mod_check = QCheckBox(self.centralWidget)
        self.include_menu_mod_check.setObjectName(u"include_menu_mod_check")
        self.include_menu_mod_check.setEnabled(True)

        self.verticalLayout.addWidget(self.include_menu_mod_check)

        self.include_menu_mod_label = QLabel(self.centralWidget)
        self.include_menu_mod_label.setObjectName(u"include_menu_mod_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.include_menu_mod_label.sizePolicy().hasHeightForWidth())
        self.include_menu_mod_label.setSizePolicy(sizePolicy)
        self.include_menu_mod_label.setMaximumSize(QSize(16777215, 60))
        self.include_menu_mod_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.include_menu_mod_label.setWordWrap(True)
        self.include_menu_mod_label.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.include_menu_mod_label)

        self.line_1 = QFrame(self.centralWidget)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.HLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_1)

        self.warp_to_start_check = QCheckBox(self.centralWidget)
        self.warp_to_start_check.setObjectName(u"warp_to_start_check")

        self.verticalLayout.addWidget(self.warp_to_start_check)

        self.warp_to_start_label = QLabel(self.centralWidget)
        self.warp_to_start_label.setObjectName(u"warp_to_start_label")
        sizePolicy.setHeightForWidth(self.warp_to_start_label.sizePolicy().hasHeightForWidth())
        self.warp_to_start_label.setSizePolicy(sizePolicy)
        self.warp_to_start_label.setMaximumSize(QSize(16777215, 70))
        self.warp_to_start_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.warp_to_start_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.warp_to_start_label)

        self.line_2 = QFrame(self.centralWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.skip_final_bosses_check = QCheckBox(self.centralWidget)
        self.skip_final_bosses_check.setObjectName(u"skip_final_bosses_check")

        self.verticalLayout.addWidget(self.skip_final_bosses_check)

        self.skip_final_bosses_label = QLabel(self.centralWidget)
        self.skip_final_bosses_label.setObjectName(u"skip_final_bosses_label")
        self.skip_final_bosses_label.setMouseTracking(True)
        self.skip_final_bosses_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.skip_final_bosses_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.skip_final_bosses_label)

        self.line_3 = QFrame(self.centralWidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.pickup_style_box = QGroupBox(self.centralWidget)
        self.pickup_style_box.setObjectName(u"pickup_style_box")
        sizePolicy.setHeightForWidth(self.pickup_style_box.sizePolicy().hasHeightForWidth())
        self.pickup_style_box.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.pickup_style_box)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pickup_model_combo = QComboBox(self.pickup_style_box)
        self.pickup_model_combo.addItem("")
        self.pickup_model_combo.addItem("")
        self.pickup_model_combo.addItem("")
        self.pickup_model_combo.addItem("")
        self.pickup_model_combo.setObjectName(u"pickup_model_combo")

        self.verticalLayout_2.addWidget(self.pickup_model_combo)

        self.pickup_data_source_label = QLabel(self.pickup_style_box)
        self.pickup_data_source_label.setObjectName(u"pickup_data_source_label")

        self.verticalLayout_2.addWidget(self.pickup_data_source_label)

        self.pickup_data_source_combo = QComboBox(self.pickup_style_box)
        self.pickup_data_source_combo.addItem("")
        self.pickup_data_source_combo.addItem("")
        self.pickup_data_source_combo.addItem("")
        self.pickup_data_source_combo.setObjectName(u"pickup_data_source_combo")

        self.verticalLayout_2.addWidget(self.pickup_data_source_combo)


        self.verticalLayout.addWidget(self.pickup_style_box)

        PresetEchoesPatches.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetEchoesPatches)

        QMetaObject.connectSlotsByName(PresetEchoesPatches)
    # setupUi

    def retranslateUi(self, PresetEchoesPatches):
        PresetEchoesPatches.setWindowTitle(QCoreApplication.translate("PresetEchoesPatches", u"Other", None))
        self.include_menu_mod_check.setText(QCoreApplication.translate("PresetEchoesPatches", u"Include Menu Mod", None))
        self.include_menu_mod_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"<html><head/><body><p>Menu Mod is a pratice tool for Echoes, allowing in-game changes to which items you have and warping to all rooms.</p><p>See the <a href=\"https://www.dropbox.com/s/yhqqafaxfo3l4vn/Echoes%20Menu.7z?file_subpath=%2FEchoes+Menu%2Freadme.txt\"><span style=\" text-decoration: underline; color:#0000ff;\">Menu Mod README</span></a> for more details.</p></body></html>", None))
        self.warp_to_start_check.setText(QCoreApplication.translate("PresetEchoesPatches", u"Add warping to starting location to save stations", None))
        self.warp_to_start_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"<html><head/><body><p>Refusing to save at any Save Station will prompt if you want to warp to the starting location (usually Samus' Ship).</p><p><span style=\" color:#005500;\">Usage of the this option is encouraged for all, as it prevents many softlocks that occurs normally in Echoes.</span></p></body></html>", None))
        self.skip_final_bosses_check.setText(QCoreApplication.translate("PresetEchoesPatches", u"Go directly to credits from Sky Temple Gateway", None))
        self.skip_final_bosses_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"<html><head/><body><p>Change the light beam in Sky Temple Gateway to go directly to the credits, skipping the final bosses.</p><p>This changes the requirements to <span style=\" font-weight:600;\">not need the final bosses</span>, turning certain items optional such as Screw Attack and Spider Ball.</p></body></html>", None))
        self.pickup_style_box.setTitle(QCoreApplication.translate("PresetEchoesPatches", u"Pickup style", None))
        self.pickup_model_combo.setItemText(0, QCoreApplication.translate("PresetEchoesPatches", u"Use correct item model, scan and name", None))
        self.pickup_model_combo.setItemText(1, QCoreApplication.translate("PresetEchoesPatches", u"Use correct scan and name, hide the model", None))
        self.pickup_model_combo.setItemText(2, QCoreApplication.translate("PresetEchoesPatches", u"Use correct name, hide the model and scan", None))
        self.pickup_model_combo.setItemText(3, QCoreApplication.translate("PresetEchoesPatches", u"Hide the model, scan and name", None))

        self.pickup_data_source_label.setText(QCoreApplication.translate("PresetEchoesPatches", u"When hiding some part of the pickup, it's replaced with:", None))
        self.pickup_data_source_combo.setItemText(0, QCoreApplication.translate("PresetEchoesPatches", u"Energy Transfer Module's data", None))
        self.pickup_data_source_combo.setItemText(1, QCoreApplication.translate("PresetEchoesPatches", u"A random item data", None))
        self.pickup_data_source_combo.setItemText(2, QCoreApplication.translate("PresetEchoesPatches", u"The data of the pickup in that place", None))

    # retranslateUi

