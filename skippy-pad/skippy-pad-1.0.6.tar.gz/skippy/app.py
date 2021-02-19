from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import qtmodern.styles
import collections

import utils.critical
import utils.session
import utils.profile
import utils.plugin
import config
from widget import *

import pyscp
import json
import os
import sys


class App(QMainWindow):
    def __init__(self, app):
        super(App, self).__init__()
        self.app = app

        self.tab = ProjectList(self)
        self.tab.tabs.currentChanged.connect(self.update_title)

        self.session = utils.session.Session(self)

        self.toolbar = ToolbarWidget(self)

        self.login_status = LoginStatusWidget(self)
        self.login_status.move(500, -14)

        self.setCentralWidget(self.tab)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.update_title()
        self.setWindowIcon(QIcon(os.path.join(config.ASSETS_FOLDER, "skippy.ico")))
        self.move(200, 200)
        self.resize(700, 700)
        self.font = QFont("Arial", 10)
        self.setFont(self.font)

    def update_title(self):
        self.setWindowTitle(
            f"{self.tab.tabs.tabText(self.tab.tabs.currentIndex())} | skippy - {config.version}"
        )

    @utils.critical.critical
    def download(self, *args):
        dDialog = DownloadDialog(self)

    @utils.critical.critical
    def upload(self, widget):
        if widget.data["parent"] != None:
            wiki = pyscp.wikidot.Wiki(widget.data["parent"][0])
            profile = utils.profile.get_profile()
            wiki.auth(profile[0], profile[1])
            p = wiki(widget.data["parent"][1])
            p.edit(
                source=widget.data["source"],
                title=widget.data["title"],
                comment="Edit using Skippy",
            )
            p.set_tags(widget.data["tags"])
            for file in widget.data["files"]:
                p.upload(file, base64.b64decode(widget.data["files"][file]))
            for file in p.files:
                if file.name not in widget.data["files"]:
                    p.remove_file(file.name)
        else:
            self.upload_as(widget)

    @utils.critical.critical
    def upload_as(self, widget):
        uDialog = UploadDialog(widget, self)

    @utils.critical.critical
    def login(self, *args):
        lDialog = LoginDialog(self)

    @utils.critical.critical
    def logout(self, *args):
        utils.profile.set_profile('','')
        self.hide()
        lDialod = LoginDialog(self)

    @utils.critical.critical
    def save_session(self, *args):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "JSON file (*.json)\nAll files (*.*)"
        )
        if path != "":
            self.session.save(path)

    @utils.critical.critical
    def load_session(self, *args):
        path, _ = QFileDialog.getOpenFileName(
            self, "Save file", "", "JSON file (*.json)\nAll files (*.*)"
        )
        if path != "":
            self.session.load(path)

    @utils.critical.critical
    def toggle_theme(self, *args):
        if config.settings["theme"] == "light":
            config.settings["theme"] = "dark"
            qtmodern.styles.dark(self.app)
        elif config.settings["theme"] == "dark":
            config.settings["theme"] = "light"
            qtmodern.styles.light(self.app)
        with open(os.path.join(config.PROPERTY_FOLDER, "settings.json"), "w") as f:
            f.write(json.dumps(config.settings))
        for i in self.action_list:
            i.setIcon(
                QIcon(
                    os.path.join(
                        config.ASSETS_FOLDER,
                        config.settings["theme"],
                        f"{self.action_list[i]}.png",
                    )
                )
            )
    
    def resizeEvent(self, event):
        self.login_status.move(self.width()-200,-14)
        if self.width() < 350:
            self.login_status.hide()
        else:
            self.login_status.show()


def start_ui():
    app = QApplication(sys.argv)
    app.setApplicationName("skippy")
    
    window = App(app)
    
    utils.plugin.PluginLoader(app)
    
    if config.settings["theme"] != "dark":
        qtmodern.styles.light(app)
    else:
        qtmodern.styles.dark(app)
    
    if utils.profile.get_profile()[0] == '' or utils.profile.get_profile()[1] == '':
        lDialod = LoginDialog(window)
    else:
        window.show()
    
    app.exec_()
    window.session.save()
