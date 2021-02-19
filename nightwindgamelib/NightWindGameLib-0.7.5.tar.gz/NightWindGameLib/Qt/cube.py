from PIL import Image, ImageQt
import random
from PySide2.QtWidgets import*
from PySide2.QtGui import*
import sys

from NightWindGameLib.Qt.fixQt import FixPySide2
fix = FixPySide2()
fix.start_fix()


class Pic:
    def __init__(self):
        self.color_out = self.randomColor()
        self.board = Image.new("HSV", (500, 500), self.color_out)
        self.randx = random.randint(0, 9) * 50
        self.randy = random.randint(0, 9) * 50
        self.gen_pic()

    def randomColor(self):
        color = (
            random.randint(0, 360),
            random.randint(0, 255), 255
        )
        return color

    def color_in(self):
        self.res = list(self.color_out)
        self.res[0] += random.randint(10, 15)
        self.res = tuple(self.res)
        return self.res

    def colorBright(self):
        self.res = list(self.color_out)
        self.res[2] -= random.randint(0, 15)
        self.res = tuple(self.res)
        return self.res

    def gen_pic(self):
        for y in range(0, 500, 50):
            for x in range(0, 500, 50):
                if x == self.randx and y == self.randy:
                    new_block = Image.new("HSV", (50, 50), self.color_in())
                    self.board.paste(new_block, (x, y))
                else:
                    new_block = Image.new("HSV", (50, 50), self.colorBright())
                    self.board.paste(new_block, (x, y))


class OpsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        self.setup()

    def setup(self):
        self.new_pic()
        self.width = self.img.width()
        self.height = self.img.height()
        self.resize(self.width, self.height)
        self.painter = QPainter()

    def new_pic(self):
        self.pic = Pic()
        self.img = ImageQt.ImageQt(self.pic.board.convert("RGBA"))
        self.img = QPixmap.fromImage(self.img)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.img)
        self.painter.end()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        tar_x = self.pic.randx
        tar_y = self.pic.randy
        if tar_x <= x <= tar_x + 50 and tar_y <= y <= tar_y + 50:
            QMessageBox.about(self, "恭喜", "correct")
            self.new_pic()
            self.update()
        else:
            QMessageBox.warning(self, "注意", "wrong")


def main():
    app = QApplication(sys.argv)
    window = OpsWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
