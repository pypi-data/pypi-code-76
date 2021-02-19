import sys
from typing import DefaultDict
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg

#修正ui在不同分辨率屏幕上的尺寸问题
qtc.QCoreApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling)
app = qtw.QApplication(sys.argv)


class CodeQt(qtw.QMainWindow):
    def __init__(self, myui):
        super().__init__(parent=None)
        if hasattr(myui, 'Ui_Form'):
            self.ui = myui.Ui_Form()
        else:
            self.ui = myui
        # 引用QApplication对象
        self.app = app
        # 自定义Widget，防止出现重名
        self.mywidgets = {}
        # 添加在QMainWindow上的事件及该事件对应的处理函数
        self.mysignals = DefaultDict(list)
        # 委托给QMainWindow进行事件和处理的QMainWindow上的其它组件
        self.watchedwidgets = DefaultDict(dict)
        # Ui_Form执行setupUi，完成ui布局文件控件的创建和引用
        self.setup()

    def eventFilter(self, a0, e) -> bool:
        if a0 in self.watchedwidgets:
            if e.type() in self.watchedwidgets[a0]:
                func = self.watchedwidgets[a0][e.type()]
                func(e)

        return super().eventFilter(a0, e)

    def watch_widget(self, widget, event, func):
        widget.installEventFilter(self)
        self.watchedwidgets[widget][event] = func

    def event(self, e):
        if e.type() in self.mysignals.keys():
            for func in self.mysignals[e.type()]:
                func(e)
        return super().event(e)

    # 注册在窗体上发生的事件和处理函数
    def window_event(self, e, func):
        self.mysignals[e].append(func)

    # 注销在窗体上发生的事件和处理函数
    def remove_window_event(self, e, func):
        self.mysignals[e].remove(func)

    # 注册在窗体上发生的事件和处理函数
    def window_siganl(self, signal, func):
        self.mysignals[signal].append(func)

    # 注销在窗体上发生的事件和处理函数
    def remove_window_siganl(self, signal, func):
        self.mysignals[signal].remove(func)

    def setup(self):
        '''
        ui布局文件控件的创建和引用
        '''
        self.ui.setupUi(self)

    def on_value_changed_do(self, widgt, func):
        if isinstance(widgt, qtw.QWidget):
            widgt.valueChanged.connect(func)

    def on_click_do(self, widgt, func):
        '''
        完成组件clicked信号的槽联接
        '''
        if isinstance(widgt, qtw.QWidget):
            widgt.clicked.connect(func)

    def draw_image(self, imagename, x0, y0, w=0, h=0):
        '''
        创建自定义控件Widget，通过重写其paintEvent
        该自定义Widget外形是在paintEvent中绘制的图像
        '''
        class MyImage(qtw.QWidget):
            def __init__(self, parent) -> None:
                super().__init__(parent=parent)
                self.img = qtg.QPixmap(imagename)
                if w and h:
                    self.imgw = w
                    self.imgh = h
                else:
                    self.imgw = self.img.width()
                    self.imgh = self.img.height()

            def paintEvent(self, a0: qtg.QPaintEvent):
                p = qtg.QPainter(self)
                p.drawPixmap(0, 0, self.imgw, self.imgh, self.img)

        mywidget = MyImage(self)
        mywidget.setGeometry(qtc.QRect(x0, y0, mywidget.imgw, mywidget.imgh))
        return mywidget

    def add_widget(self, WidgetClazz, objname, x0, y0, w, h):
        '''
        动态添加Widget
        '''
        if objname not in self.mywidgets.keys():
            mywidget = WidgetClazz(self)
            mywidget.setObjectName(objname)
            mywidget.setGeometry(qtc.QRect(x0, y0, w, h))
            self.mywidgets[objname] = mywidget
            setattr(self.ui, objname, mywidget)
        else:
            raise SystemExit('重复的objname')

    def set_title(self, title):
        self.setWindowTitle(title)

    def run(self):
        self.show()
        sys.exit(app.exec())