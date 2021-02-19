from abc import ABCMeta, abstractmethod
from PyQt5.QtWidgets import *
import sys
import os

import config

class PluginBase(metaclass=ABCMeta):
    __alias__ = "Plugin"

    __description__ = ""
    __author__ = ""
    __version__ = "1.0.0"

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def proccess(self):
        pass
    
    @property
    def widgets(self):
        widgets = []
        for widget in self.app.topLevelWidgets():
            widgets.append(widget)
        return widgets
    
    @property
    def mainwindow(self):
        for widget in self.widgets:
            if isinstance(widget, QMainWindow):
                return widget
    
    def replace_window(self, old, new):
        old.close()
        new.show()


class PluginLoader:
    def __init__(self, app):
        self.app = app

        self.plugins = []

        self.load()

    @staticmethod
    def files():
        return [
            os.path.splitext(f)[0]
            for f in os.listdir(config.PLUGINS_FOLDER)
            if os.path.isfile(os.path.join(config.PLUGINS_FOLDER, f))
            if os.path.splitext(f)[1] == ".py"
        ]

    def load(self):
        sys.path.append(config.PLUGINS_FOLDER)
        for file in self.files():
            plugin = __import__(file).Plugin(self.app)
            self.plugins.append(plugin)
            plugin.proccess()
