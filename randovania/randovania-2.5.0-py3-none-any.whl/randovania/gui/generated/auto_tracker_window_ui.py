# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auto_tracker_window.ui'
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


class Ui_AutoTrackerWindow(object):
    def setupUi(self, AutoTrackerWindow):
        if not AutoTrackerWindow.objectName():
            AutoTrackerWindow.setObjectName(u"AutoTrackerWindow")
        AutoTrackerWindow.resize(402, 248)
        self.centralwidget = QWidget(AutoTrackerWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.inventory_group = QGroupBox(self.centralwidget)
        self.inventory_group.setObjectName(u"inventory_group")
        self.inventory_group.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.inventory_layout = QGridLayout(self.inventory_group)
        self.inventory_layout.setObjectName(u"inventory_layout")

        self.gridLayout.addWidget(self.inventory_group, 0, 0, 1, 1)

        self.game_connection_layout = QHBoxLayout()
        self.game_connection_layout.setObjectName(u"game_connection_layout")
        self.game_connection_tool = QToolButton(self.centralwidget)
        self.game_connection_tool.setObjectName(u"game_connection_tool")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_connection_tool.sizePolicy().hasHeightForWidth())
        self.game_connection_tool.setSizePolicy(sizePolicy)
        self.game_connection_tool.setPopupMode(QToolButton.InstantPopup)

        self.game_connection_layout.addWidget(self.game_connection_tool)

        self.connection_status_label = QLabel(self.centralwidget)
        self.connection_status_label.setObjectName(u"connection_status_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.connection_status_label.sizePolicy().hasHeightForWidth())
        self.connection_status_label.setSizePolicy(sizePolicy1)

        self.game_connection_layout.addWidget(self.connection_status_label)

        self.force_update_button = QPushButton(self.centralwidget)
        self.force_update_button.setObjectName(u"force_update_button")
        sizePolicy.setHeightForWidth(self.force_update_button.sizePolicy().hasHeightForWidth())
        self.force_update_button.setSizePolicy(sizePolicy)

        self.game_connection_layout.addWidget(self.force_update_button)


        self.gridLayout.addLayout(self.game_connection_layout, 1, 0, 1, 1)

        AutoTrackerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(AutoTrackerWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 402, 21))
        AutoTrackerWindow.setMenuBar(self.menubar)

        self.retranslateUi(AutoTrackerWindow)

        QMetaObject.connectSlotsByName(AutoTrackerWindow)
    # setupUi

    def retranslateUi(self, AutoTrackerWindow):
        AutoTrackerWindow.setWindowTitle(QCoreApplication.translate("AutoTrackerWindow", u"Auto Tracker", None))
        self.inventory_group.setTitle(QCoreApplication.translate("AutoTrackerWindow", u"Inventory", None))
        self.game_connection_tool.setText(QCoreApplication.translate("AutoTrackerWindow", u"Connect to game", None))
        self.connection_status_label.setText(QCoreApplication.translate("AutoTrackerWindow", u"Connection Status", None))
        self.force_update_button.setText(QCoreApplication.translate("AutoTrackerWindow", u"Update", None))
    # retranslateUi

