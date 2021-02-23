from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineProfile

from AnyQt.QtWidgets import QVBoxLayout

from orangewidget.utils.webview import WebviewWidget

from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.settings import Setting
from Orange.widgets import gui

__all__ = ['MainWindow']


class MainWindow(OWWidget):
    name = '蓝鲸浏览器'
    want_basic_layout = True
    want_main_area = True
    want_control_area = False
    auto_commit = Setting(True)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.window_layout = QVBoxLayout()
        self.session = args[0] if len(args) > 0 else {}

        self.tabWidget = gui.widgetBox(self.mainArea, orientation=self.window_layout)

        self.webview = WebEngineView(self)
        self.webview.load(QUrl('https://bo.dashenglab.com/client'))
        self.window_layout.addWidget(self.webview)
        self.webview.show()

        self.mainArea.layout().addWidget(self.tabWidget)
        self.webview.urlChanged.connect(self.renew_bar)

    # 响应输入的地址
    def renew_bar(self):
        if self.webview.page().url().toString() == "https://bo.dashenglab.com/client/success":
            self.session.update({'SESSION': self.webview.get_session()})
            self.webview.close()
            self.close()


class WebEngineView(WebviewWidget):
    def __init__(self, main_window, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.main_window = main_window
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.cookie_change)
        self.cookies = {}

    def cookie_change(self, cookie):
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        if cookie.domain() == "bo.dashenglab.com":
            self.cookies.update({name: value})

    def get_session(self):
        user_session = self.cookies.get('SESSION')
        return user_session


if __name__ == "__main__":
    WidgetPreview(MainWindow).run()
