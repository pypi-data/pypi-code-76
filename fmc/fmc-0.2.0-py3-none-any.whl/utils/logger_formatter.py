#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import logging
from .misc import is_debug_mode

def setup_console_log_format():

    logger = logging.getLogger()

    # set log format & color
    handler = logging.StreamHandler()
    handler.setFormatter(ConsoleFormatter())
    logger.addHandler(handler)

    # set level based on mode
    if is_debug_mode():
        logger.setLevel(logging.DEBUG)
        logging.warning("Running in debug mode!!!")
    else:
        logger.setLevel(logging.INFO)

class ConsoleFormatter(logging.Formatter):

    default_formatter = logging.Formatter("%(message)s")
    detailed_formatter = logging.Formatter("%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s")

    def format(self, record):

        if record.levelno in (logging.INFO, logging.WARNING):
            formatter = self.default_formatter
        else:
            formatter = self.detailed_formatter

        res = formatter.format(record)
        res = self.__color(res, record.levelno)

        return res

    def __color(self, res, levelno):
        BLUE_COLOR = '\x1b[34;1m'
        RED_COLOR = '\x1b[31;1m'
        GREEN_COLOR = '\x1b[32;1m'
        YELLOW_COLOR = '\x1b[33;1m'
        DEFAULT_COLOR = '\x1b[0m'

        if(levelno >= logging.CRITICAL):
            color = RED_COLOR
        elif(levelno >= logging.ERROR):
            color = RED_COLOR
        elif(levelno >= logging.WARNING):
            color = YELLOW_COLOR
        elif(levelno >= logging.INFO):
            color = GREEN_COLOR
        elif(levelno >= logging.DEBUG):
            color = BLUE_COLOR
        else:
            color = DEFAULT_COLOR

        return "%s%s%s" % (color, res, DEFAULT_COLOR)
