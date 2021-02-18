import config

import sys
import os


class PluginBase:
    __alias__ = "Plugin"

    __description__ = ""
    __author__ = ""
    __version__ = "1.0.0"

    def __init__(self, app):
        self.app = app

    def proccess(self):
        pass


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
