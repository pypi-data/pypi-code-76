# encoding=utf8
# -*- coding: utf-8 -*-

from .batch import *
from .udf import *
from .env import *
from .ipython_magic_command import *
from .pipeline import *
from .stream import *
from .common.types.conversion.type_converters import collectToDataframes, dataframeToOperator
from .common.types import *
from .config import AlinkGlobalConfiguration
from .plugin_downloader import PluginDownloader

print("""
Use one of the following commands to start using PyAlink:
 - useLocalEnv(parallelism, flinkHome=None, config=None)
 - useRemoteEnv(host, port, parallelism, flinkHome=None, localIp="localhost", config=None)
Call resetEnv() to reset environment and switch to another.
""")
