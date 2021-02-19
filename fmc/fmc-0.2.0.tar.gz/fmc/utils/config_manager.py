#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import logging
import os
from plumbum import cli
from .misc import is_debug_mode

class ConfigManager():

    def __get_config_path(self):
        if is_debug_mode():
            filename = "fmc_debug.conf"
        else:
            filename = "fmc.conf"
        return os.path.expanduser("~/%s" % filename)

    def __read_config_once(self):
        if not hasattr(self, 'config'):
            self.config = cli.Config(self.__get_config_path())
            self.config.read()
            logging.debug("Read config file first time.")
        
    def get(self, section, key):
        self.__read_config_once()
        logging.debug("Getting config section=%s, key=%s" % (section, key))
        value = self.config.get("%s.%s" % (section, key), "")
        if value == "":
            return None
        else:
            return value

    def set(self, section, key, value):
        self.__read_config_once()
        logging.debug("Setting config %s - %s" % (section, key))
        self.config.set("%s.%s" % (section, key), value)
        if self.config.changed:
            self.config.write()

    def get_config_info(self):
        config_path = self.__get_config_path()
        if not os.path.isfile(config_path):
            return "No config file"
        else:
            with open(config_path) as f:
                content = f.read()
            return "config file: %s\n%s" % (config_path, content)