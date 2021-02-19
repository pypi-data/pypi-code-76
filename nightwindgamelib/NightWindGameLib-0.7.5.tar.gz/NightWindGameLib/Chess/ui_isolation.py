from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Isolation(object):
    def setupUi(self, Isolation):
        if not Isolation.objectName():
            Isolation.setObjectName(u"Isolation")
        Isolation.resize(500, 500)
        self.centralwidget = QWidget(Isolation)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pbtn_list = []
        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(140, 10, 171, 41))
        font = QFont()
        font.setPointSize(17)
        self.label_title.setFont(font)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.cb_level = QComboBox(self.centralwidget)
        self.cb_level.addItem("")
        self.cb_level.addItem("")
        self.cb_level.addItem("")
        self.cb_level.setObjectName(u"cb_level")
        self.cb_level.setGeometry(QRect(30, 10, 101, 41))
        font1 = QFont()
        font1.setPointSize(15)
        self.cb_level.setFont(font1)
        self.cb_first = QComboBox(self.centralwidget)
        self.cb_first.addItem("")
        self.cb_first.addItem("")
        self.cb_first.setObjectName(u"cb_first")
        self.cb_first.setGeometry(QRect(30, 60, 101, 41))
        self.cb_first.setFont(font1)
        self.pbtn_rule = QPushButton(self.centralwidget)
        self.pbtn_rule.setObjectName(u"pbtn_rule")
        self.pbtn_rule.setGeometry(QRect(310, 10, 181, 41))
        font2 = QFont()
        font2.setPointSize(9)
        self.pbtn_rule.setFont(font2)
        self.label_status = QLabel(self.centralwidget)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(250, 60, 81, 41))
        font3 = QFont()
        font3.setPointSize(13)
        font4 = QFont()
        font4.setPointSize(11)
        self.label_status.setFont(font4)
        self.label_moves = QLabel(self.centralwidget)
        self.label_moves.setObjectName(u"label_moves")
        self.label_moves.setGeometry(QRect(350, 60, 141, 41))
        self.label_moves.setFont(font3)
        self.pbtn_start = QPushButton(self.centralwidget)
        self.pbtn_start.setObjectName(u"pbtn_start")
        self.pbtn_start.setGeometry(QRect(140, 60, 101, 41))
        self.pbtn_start.setFont(font3)
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(60, 120, 381, 371))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pbtn_board = QButtonGroup(Isolation)
        self.pbtn_board.setObjectName(u"pbtn_board")
        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                pbtn = QPushButton(self.gridLayoutWidget)
                pbtn.setFont(font)
                self.pbtn_board.addButton(pbtn)
                self.gridLayout.addWidget(pbtn, i, j, 1, 1)
                row.append(pbtn)
            self.pbtn_list.append(row)

        Isolation.setCentralWidget(self.centralwidget)

        self.retranslateUi(Isolation)

        QMetaObject.connectSlotsByName(Isolation)
    # setupUi

    def retranslateUi(self, Isolation):
        for i in range(8):
            for j in range(8):
                if i == 0 and j == 0:
                    self.pbtn_list[i][j].setText(
                        QCoreApplication.translate("Isolation", u"X", None))
                elif i == 7 and j == 7:
                    self.pbtn_list[i][j].setText(
                        QCoreApplication.translate("Isolation", u"O", None))
                else:
                    self.pbtn_list[i][j].setText(
                        QCoreApplication.translate("Isolation", u"", None))

        Isolation.setWindowTitle(
            QCoreApplication.translate("Isolation",
                                       u"\u5b64\u7acb\u6e38\u620f", None))
        self.label_title.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u5b64\u7acb\u6e38\u620f", None))
        self.cb_level.setItemText(0,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u7b80\u5355", None))
        self.cb_level.setItemText(1,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u4e2d\u7b49", None))
        self.cb_level.setItemText(2,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u56f0\u96be", None))

        self.cb_first.setItemText(0,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u5148\u624b", None))
        self.cb_first.setItemText(1,
                                  QCoreApplication.translate("Isolation",
                                                             u"\u540e\u624b", None))

        self.pbtn_rule.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u7b2c\u4e00\u6b21\u73a9\uff1f\u83b7\u53d6\u6e38\u620f\u89c4\u5219",
                                       None))
        self.label_status.setText("")
        self.label_moves.setText("")
        self.pbtn_start.setText(
            QCoreApplication.translate("Isolation",
                                       u"\u5f00\u59cb\u6e38\u620f", None))
        # retranslateUi
