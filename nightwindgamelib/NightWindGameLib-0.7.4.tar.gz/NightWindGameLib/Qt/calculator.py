import sys
import math
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from sympy import *
from sympy.abc import *
from PySide2.QtGui import *
from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


def prime(n: int):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_prime_factor(num):
    number = num
    List = []
    if num >= 2:
        while number > 1:
            for i in range(2, number + 1):
                if prime(i) and number % i == 0:
                    List.append(str(i))
                    number = number // i
                    break
    return List


class Ui_Calculator(object):
    def setupUi(self, Calculator):
        if not Calculator.objectName():
            Calculator.setObjectName(u"Calculator")
        Calculator.resize(762, 652)
        font = QFont()
        font.setPointSize(11)
        Calculator.setFont(font)
        self.centralwidget = QWidget(Calculator)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pbtn_start = QPushButton(self.centralwidget)
        self.pbtn_start.setObjectName(u"pbtn_start")
        self.pbtn_start.setGeometry(QRect(470, 200, 201, 41))
        font1 = QFont()
        font1.setPointSize(15)
        self.pbtn_start.setFont(font1)
        self.lb_title = QLabel(self.centralwidget)
        self.lb_title.setObjectName(u"lb_title")
        self.lb_title.setGeometry(QRect(111, 50, 561, 101))
        font2 = QFont()
        font2.setPointSize(25)
        self.lb_title.setFont(font2)
        self.lb_title.setAlignment(Qt.AlignCenter)
        self.cb_mode = QComboBox(self.centralwidget)
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.addItem("")
        self.cb_mode.setObjectName(u"cb_mode")
        self.cb_mode.setGeometry(QRect(100, 200, 231, 41))
        self.cb_mode.setFont(font1)
        self.le_input = QLineEdit(self.centralwidget)
        self.le_input.setObjectName(u"le_input")
        self.le_input.setGeometry(QRect(80, 280, 611, 41))
        font3 = QFont()
        font3.setPointSize(12)
        self.le_input.setFont(font3)
        self.tb_result = QTextBrowser(self.centralwidget)
        self.tb_result.setObjectName(u"tb_result")
        self.tb_result.setGeometry(QRect(85, 380, 611, 241))
        Calculator.setCentralWidget(self.centralwidget)

        self.retranslateUi(Calculator)

        QMetaObject.connectSlotsByName(Calculator)

    # setupUi

    def retranslateUi(self, Calculator):
        Calculator.setWindowTitle(
            QCoreApplication.translate("Calculator",
                                       u"\u6570\u5b66\u8ba1\u7b97\u5668", None))
        self.pbtn_start.setText(
            QCoreApplication.translate("Calculator",
                                       u"\u5f00\u59cb\u8fd0\u7b97", None))
        self.lb_title.setText(
            QCoreApplication.translate("Calculator",
                                       u"\u6570\u5b66\u8ba1\u7b97\u5668", None))
        self.cb_mode.setItemText(
            0, QCoreApplication.translate("Calculator",
                                          u"\u5206\u89e3\u8d28\u56e0\u6570", None))
        self.cb_mode.setItemText(
            1, QCoreApplication.translate("Calculator",
                                          u"\u5206\u5f0f\u901a\u5206", None))
        self.cb_mode.setItemText(
            2, QCoreApplication.translate("Calculator",
                                          u"\u6574\u5f0f\u5927\u9664\u6cd5", None))
        self.cb_mode.setItemText(
            3, QCoreApplication.translate("Calculator",
                                          u"\u591a\u9879\u5f0f\u5c55\u5f00", None))
        self.cb_mode.setItemText(
            4, QCoreApplication.translate("Calculator",
                                          u"\u591a\u9879\u5f0f\u56e0\u5f0f\u5206\u89e3",
                                          None))
        self.cb_mode.setItemText(
            5, QCoreApplication.translate("Calculator",
                                          u"\u7ed8\u5236\u51fd\u6570\u56fe\u50cf",
                                          None))
        self.cb_mode.setItemText(
            6, QCoreApplication.translate("Calculator",
                                          u"\u6c42\u89e3\u65b9\u7a0b\u65b9\u7a0b\u7ec4",
                                          None))

        self.le_input.setText("")
    # retranslateUi


# 多功能数学计算器
class Calculator(QMainWindow, Ui_Calculator):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.expressions = []
        self.expression = None
        self.mode = None
        self.pbtn_start.clicked.connect(self.get_expression)
        self.show()

    # 获取输入的式子
    def get_expression(self):
        try:
            if self.le_input.text() != "":
                self.expressions = str(self.le_input.text()).split(",")
                self.start_calculate()
            else:
                QMessageBox.warning(self, "注意", "你没有输入数学式，请重新输入")
        except TypeError:
            # print(self.expressions)
            if self.le_input.text() != "":
                QMessageBox.warning(self, "注意", "输入有误")

    # 开始运算
    def start_calculate(self):
        self.expression = eval(str(self.expressions[0]))
        self.mode = self.cb_mode.currentText()
        if self.mode == "分解质因数":
            lst_prime = "*".join(get_prime_factor(self.expression))
            string = ""
            for i in lst_prime:
                string += i
            self.tb_result.setText(str(self.expression) + " = " + string)

        elif self.mode == "多项式展开":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(expand(self.expression)))

        elif self.mode == "多项式因式分解":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(factor(self.expression)))

        elif self.mode == "分式通分":
            self.tb_result.setText(str(self.expression) + " = " +
                                   str(together(self.expression)))

        elif self.mode == "绘制函数图像":
            pass

        elif self.mode == "求解方程/方程组":
            pass

        elif self.mode == "整式大除法":
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.get_expression()


# 开始运行
def main():
    app = QApplication(sys.argv)
    window = Calculator()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
