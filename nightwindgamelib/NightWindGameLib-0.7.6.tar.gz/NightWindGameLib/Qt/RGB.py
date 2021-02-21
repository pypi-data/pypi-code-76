import sys
from PySide2.QtCore import*
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PIL import Image, ImageQt

from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Ui_RGB(object):
    def setupUi(self, RGB):
        if not RGB.objectName():
            RGB.setObjectName(u"RGB")
        RGB.resize(332, 389)
        self.centralwidget = QWidget(RGB)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(31, 20, 271, 181))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(22, 220, 291, 31))
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 260, 291, 121))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slider_r = QSlider(self.widget)
        self.slider_r.setObjectName(u"slider_r")
        self.slider_r.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider_r)

        self.label_r = QLabel(self.widget)
        self.label_r.setObjectName(u"label_r")
        self.slider_r.setMaximum(255)
        self.slider_r.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.label_r)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slider_g = QSlider(self.widget)
        self.slider_g.setObjectName(u"slider_g")
        self.slider_g.setMaximum(255)
        self.slider_g.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_g)

        self.label_g = QLabel(self.widget)
        self.label_g.setObjectName(u"label_g")

        self.horizontalLayout_2.addWidget(self.label_g)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.slider_b = QSlider(self.widget)
        self.slider_b.setObjectName(u"slider_b")
        self.slider_b.setMaximum(255)
        self.slider_b.setOrientation(Qt.Horizontal)
        self.slider_b.setTickPosition(QSlider.NoTicks)

        self.horizontalLayout_3.addWidget(self.slider_b)

        self.label_b = QLabel(self.widget)
        self.label_b.setObjectName(u"label_b")

        self.horizontalLayout_3.addWidget(self.label_b)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        RGB.setCentralWidget(self.centralwidget)

        self.retranslateUi(RGB)

        QMetaObject.connectSlotsByName(RGB)
    # setupUi

    def retranslateUi(self, RGB):
        RGB.setWindowTitle(
            QCoreApplication.translate("RGB", u"RGB\u8c03\u8272\u677f", None))
        self.label.setText(QCoreApplication.translate("RGB", u"", None))
        self.label_r.setText(QCoreApplication.translate("RGB", u"0", None))
        self.label_g.setText(QCoreApplication.translate("RGB", u"0", None))
        self.label_b.setText(QCoreApplication.translate("RGB", u"0", None))
    # retranslateUi


class RGB(QMainWindow, Ui_RGB):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()
        self.show()

    def setup(self):
        self.slider_b.valueChanged.connect(self.process)
        self.slider_r.valueChanged.connect(self.process)
        self.slider_g.valueChanged.connect(self.process)
        self.label.setScaledContents(True)

    def process(self):
        value_r = self.slider_r.value()
        value_g = self.slider_g.value()
        value_b = self.slider_b.value()
        self.label_b.setText(str(value_b))
        self.label_g.setText(str(value_g))
        self.label_r.setText(str(value_r))
        rgb = (value_r, value_g, value_b)
        self.lineEdit.setText(str(rgb))
        img = Image.new("RGBA", (100, 100), rgb)
        img = ImageQt.ImageQt(img)
        img = QPixmap.fromImage(img)
        self.label.setPixmap(img)


def main():
    app = QApplication(sys.argv)
    window = RGB()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
