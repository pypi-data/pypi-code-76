# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'debug_backend_window.ui'
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


class Ui_DebugBackendWindow(object):
    def setupUi(self, DebugBackendWindow):
        if not DebugBackendWindow.objectName():
            DebugBackendWindow.setObjectName(u"DebugBackendWindow")
        DebugBackendWindow.resize(707, 322)
        self.central_widget = QWidget(DebugBackendWindow)
        self.central_widget.setObjectName(u"central_widget")
        self.central_widget.setMaximumSize(QSize(16777215, 16777215))
        self.central_widget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.central_widget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(self.central_widget)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 4, 3, 1, 1)

        self.messages_list = QListWidget(self.central_widget)
        self.messages_list.setObjectName(u"messages_list")

        self.gridLayout.addWidget(self.messages_list, 0, 2, 4, 2)

        self.current_status_label = QLabel(self.central_widget)
        self.current_status_label.setObjectName(u"current_status_label")

        self.gridLayout.addWidget(self.current_status_label, 0, 0, 1, 1)

        self.current_status_combo = QComboBox(self.central_widget)
        self.current_status_combo.setObjectName(u"current_status_combo")

        self.gridLayout.addWidget(self.current_status_combo, 0, 1, 1, 1)

        self.collect_location_button = QPushButton(self.central_widget)
        self.collect_location_button.setObjectName(u"collect_location_button")

        self.gridLayout.addWidget(self.collect_location_button, 1, 1, 1, 1)

        self.collect_location_combo = QComboBox(self.central_widget)
        self.collect_location_combo.setObjectName(u"collect_location_combo")

        self.gridLayout.addWidget(self.collect_location_combo, 1, 0, 1, 1)

        self.inventory_box = QGroupBox(self.central_widget)
        self.inventory_box.setObjectName(u"inventory_box")
        self.gridLayout_2 = QGridLayout(self.inventory_box)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.inventory_label = QLabel(self.inventory_box)
        self.inventory_label.setObjectName(u"inventory_label")

        self.gridLayout_2.addWidget(self.inventory_label, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.inventory_box, 2, 0, 2, 2)

        DebugBackendWindow.setCentralWidget(self.central_widget)
        self.menuBar = QMenuBar(DebugBackendWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 707, 21))
        DebugBackendWindow.setMenuBar(self.menuBar)

        self.retranslateUi(DebugBackendWindow)

        QMetaObject.connectSlotsByName(DebugBackendWindow)
    # setupUi

    def retranslateUi(self, DebugBackendWindow):
        DebugBackendWindow.setWindowTitle(QCoreApplication.translate("DebugBackendWindow", u"Debug Backend", None))
        self.reset_button.setText(QCoreApplication.translate("DebugBackendWindow", u"Reset", None))
        self.current_status_label.setText(QCoreApplication.translate("DebugBackendWindow", u"Current Status", None))
        self.collect_location_button.setText(QCoreApplication.translate("DebugBackendWindow", u"Collect Location", None))
        self.inventory_box.setTitle(QCoreApplication.translate("DebugBackendWindow", u"Inventory", None))
        self.inventory_label.setText("")
    # retranslateUi

