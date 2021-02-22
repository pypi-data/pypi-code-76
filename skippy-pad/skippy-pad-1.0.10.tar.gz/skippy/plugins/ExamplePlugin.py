import utils.plugin


class Plugin(utils.plugin.PluginBase):
    __alias__ = "ExamplePlugin"

    __description__ = "I am a example plugin."
    __author__ = "MrNereof"
    __version__ = "1.0.0"

    def proccess(self):
        """do something"""
        pass
