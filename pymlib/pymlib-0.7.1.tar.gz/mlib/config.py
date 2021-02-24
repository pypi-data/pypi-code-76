# -*- coding: utf-8 -*-

import yaml

RESOURCES = {}

ALL = [
    "initConfig",
    "getConfig"
]

class ConfigExcept(Exception):
    pass

def initConfig(config_path):
    """
    config_path: 配置文件目录
    """
    with open(config_path, "r", encoding='utf-8') as fp:
        conf = yaml.load(fp, Loader=yaml.FullLoader)
        RESOURCES["conf"] = conf

def getConfig():
    """
    获取配置文件
    """
    conf = RESOURCES.get("conf")
    if not conf:
        raise ConfigExcept("配置文件未初始化")
    return conf


