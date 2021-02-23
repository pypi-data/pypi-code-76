from .py4j_util import get_java_class
from .common.types.bases.j_obj_wrapper import JavaObjectWrapperWithAutoTypeConversion


class PluginDownloader(JavaObjectWrapperWithAutoTypeConversion):
    j_cls_name = "com.alibaba.alink.common.io.plugin.PluginDownloader"

    def __init__(self):
        j_obj = get_java_class(self.j_cls_name)()
        self._j_obj = j_obj

    def get_j_obj(self):
        return self._j_obj

    def loadConfig(self, configFileName: str = None):
        if configFileName is None:
            return self.loadConfig()
        else:
            return self.loadConfig(configFileName)

    def listAvailablePlugins(self):
        return self.listAvailablePlugins()

    def listAvailablePluginVersions(self, pluginName: str):
        return self.listAvailablePluginVersions(pluginName)

    def downloadPlugin(self, pluginName: str, pluginVersion: str = None):
        if pluginVersion is None:
            return self.downloadPlugin(pluginName)
        else:
            return self.downloadPlugin(pluginName, pluginVersion)

    def downloadAll(self):
        return self.downloadAll()

    def upgrade(self):
        return self.upgrade()
