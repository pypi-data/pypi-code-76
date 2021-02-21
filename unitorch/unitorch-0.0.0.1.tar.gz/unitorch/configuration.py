import logging
import warnings
import configparser

warnings.filterwarnings("ignore")
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %p",
    level=logging.INFO,
)


class core_configure_parser(configparser.ConfigParser):
    def __init__(self, fpath="./cfg/default.ini", params=[]):
        super().__init__(interpolation=configparser.ExtendedInterpolation())
        self.fpath = fpath
        self.read(fpath)
        for param in params:
            assert len(param) == 3
            k0, k1, v = param
            if not self.has_section(k0):
                self.add_section(k0)
            self.set(k0, k1, str(v))

        self._freeze_section = None
        self._map_dict = dict()

        self._default_section = self.getdefault("extra/config", "default_section", None)
        self._freeze_section = self.getdefault("extra/config", "freeze_section", None)
        self._map_dict = self.getdefault("extra/config", "section_map_dict", None)
        if self._map_dict is not None:
            self._map_dict = eval(self._map_dict)
        else:
            self._map_dict = dict()

    def _getdefault(self, section, option, value=None):
        if not self.has_section(section):
            return value
        if isinstance(value, bool):
            if self.has_option(section, option):
                return self.getboolean(section, option)
            return value
        if isinstance(value, int):
            if self.has_option(section, option):
                return self.getint(section, option)
            return value
        if isinstance(value, float):
            if self.has_option(section, option):
                return self.getfloat(section, option)
            return value
        if self.has_option(section, option):
            return self.get(section, option)
        return value

    def set_map_dict(self, map_dict=dict()):
        self._map_dict = map_dict

    def set_freeze_section(self, section):
        self._freeze_section = section

    def set_default_section(self, section):
        self._default_section = section

    def getdefault(self, section, option, value=None):
        value = self._getdefault(section, option, value)

        if self._freeze_section:
            value = self._getdefault(self._freeze_section, option, value)

        if self._map_dict.get(section):
            section = self._map_dict.get(section)
            value = self._getdefault(section, option, value)
        return value

    def getoption(self, option, value=None):
        return self.getdefault(self._default_section, option, value)

    def print(self):
        print("#" * 30, "Config Info".center(20, " "), "#" * 30)
        for sec, item in self.items():
            for k, v in item.items():
                print(
                    sec.rjust(10, " "),
                    ":".center(5, " "),
                    k.ljust(30, " "),
                    ":".center(5, " "),
                    v.ljust(30, " "),
                )
        print("#" * 30, "Config Info End".center(20, " "), "#" * 30)

    def save(self, save_path="./cfg/cfg.ini"):
        self.write(open(save_path, "w"))
        return save_path

    def copy(self, cfg):
        setting = [(sec, k, v) for sec in cfg.sections() for k, v in cfg[sec].items()]
        return self.__class__(self.fpath, setting)
