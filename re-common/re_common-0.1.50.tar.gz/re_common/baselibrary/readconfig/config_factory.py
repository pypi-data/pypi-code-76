from re_common.baselibrary import BaseAbs


class ConfigFactory(BaseAbs):

    @staticmethod
    def ini_factory(type='ini'):
        from re_common.baselibrary import IniConfig
        if type == 'ini':
            return IniConfig()
        assert 0, "err sql type please check: %s" % type

    @staticmethod
    def toml_factory(type='toml'):
        from re_common.baselibrary.readconfig.toml_config import TomlConfig
        if type == 'toml':
            return TomlConfig()
        assert 0, "err sql type please check: %s" % type
