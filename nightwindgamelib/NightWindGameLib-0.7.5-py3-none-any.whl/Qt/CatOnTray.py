import sys
from PySide2.QtWidgets import*
from PySide2.QtCore import*
from PySide2.QtGui import*
from PySide2.QtMultimedia import QSound

from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Tray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setup()
        self.show()

    def setup(self):
        self.index = 0
        self.tips = ["我叫编程猫", "很高兴认识你", "很开心能一起学习Python"]
        self.icon = QIcon("images_cat/sit.png")
        self.setIcon(self.icon)
        self.setToolTip("使用鼠标点击我吧")
        self.activated.connect(self.process)
        self.sound1 = QSound("images_cat/sound1.wav")
        self.sound2 = QSound("images_cat/sound2.wav")
        self.icon2 = QIcon("images_cat/stand.png")
        self.timer = QTimer()
        self.icons = [f"images_cat/{i}.png" for i in range(0, 5)]
        self.icon_index = 0
        self.change_icon()
    
    def process(self, key):
        if key == self.Trigger:
            self.sound1.play()
            self.setIcon(self.icon)
        elif key == self.Context or key == self.MiddleClick:
            self.sound2.play()
            self.setIcon(self.icon2)
        self.setToolTip(self.tips[self.index % 3])
        self.index += 1

    def change_icon(self):
        self.setIcon(QIcon(self.icons[self.icon_index % 5]))
        self.icon_index += 1
        self.timer.singleShot(100, self.change_icon)


def main():
    app = QApplication(sys.argv)
    tray = Tray()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
