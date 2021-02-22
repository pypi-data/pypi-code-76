# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;logging

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.1.0
dpt_logging/log_handler.py
"""

# pylint: disable=invalid-name

from os import path
from sys import stderr
from time import strftime
import os

from dpt_settings import Settings

from .abstract_log_handler import AbstractLogHandler

_API_JAVA = 1
"""
Java based log handlers
"""
_API_PYTHON = 2
"""
Python log handlers
"""

try:
    from logging import NullHandler, StreamHandler, CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
    from logging.config import dictConfig
    from logging.handlers import RotatingFileHandler
    import logging

    if (hasattr(logging, "logMultiprocessing")): logging.logMultiprocessing = False
    _api_type = _API_PYTHON
except ImportError:
    from java.util.logging import FileHandler, StreamHandler
    from java.util.logging import Logger as logging
    from java.util.logging.Level import INFO, WARNING
    from java.util.logging.Level import FINE as DEBUG
    from java.util.logging.Level import OFF as NOTSET
    from java.util.logging.Level import SEVERE as CRITICAL
    from java.util.logging.Level import SEVERE as ERROR
    _api_type = _API_JAVA
#

class LogHandler(AbstractLogHandler):
    """
"LogHandler" is the default logging endpoint writing messages to a file.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: logging
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "logger", "log_file_path_name", "log_format_datetime", "log_file_size_max", "log_file_rotates" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _log_handler = None
    """
Log file handler responsible for Python module "logging"
    """

    def __init__(self):
        """
Constructor __init__(LogHandler)

:since: v1.0.0
        """

        # global: _api_type, _API_PYTHON
        # pylint: disable=protected-access

        AbstractLogHandler.__init__(self)

        self.logger = None
        """
Logger object
        """
        self.log_file_path_name = None
        """
Path and filename of the log file
        """
        self.log_format_datetime = Settings.get("global_log_datetime", "%m/%d/%Y %H:%M:%S")
        """
Date/Time format
        """
        self.log_file_size_max = int(Settings.get("global_log_size_max", 104857600))
        """
File size a log file gets rotated
        """
        self.log_file_rotates = int(Settings.get("global_log_rotates", 5))
        """
Preserve the amount of files
        """

        self.level_map = { "debug": DEBUG,
                           "error": ERROR,
                           "info": INFO,
                           "warning": WARNING
                         }

        level = Settings.get("global_log_level")
        self.level['global'] = self.level_map.get(level, WARNING)

        self.logger = logging.getLogger(self._ident)
        self.logger.setLevel(DEBUG)

        if (LogHandler._log_handler is None):
            self._init_handler()

            if (_api_type == _API_PYTHON):
                logger_root = logging.getLogger()

                if ((hasattr(logger_root, "hasHandlers") and (not logger_root.hasHandlers())) or len(logger_root.handlers) < 1):
                    if (Settings.get("global_log_initialize_root", True)): logger_root.addHandler(self.log_handler)
                    else: logger_root.addHandler(NullHandler())
                #

                self.logger.addHandler(self.log_handler)
                self.logger.propagate = False
            else:
                self.logger.addHandler(self.log_handler)
                self.logger.setUseParentHandlers(False)
            #

            LogHandler._log_handler = self.log_handler
        else: self.log_handler = LogHandler._log_handler

        self.log_thread_id = Settings.get("global_log_thread_id", False)
    #

    def debug(self, data, *args, **kwargs):
        """
Debug message method

:param data: Debug data
:param context: Logging context

:since: v1.0.0
        """

        # pylint: disable=protected-access

        context = kwargs.get("context", "global")
        if (self._get_implementation_level(context) == DEBUG): self._write(DEBUG, data, *args)
    #

    def error(self, data, *args, **kwargs):
        """
Error message method

:param data: Error data
:param context: Logging context

:since: v1.0.0
        """

        # pylint: disable=protected-access

        context = kwargs.get("context", "global")
        if (self._get_implementation_level(context) != NOTSET): self._write(ERROR, data, *args)
    #

    def info(self, data, *args, **kwargs):
        """
Info message method

:param data: Info data
:param context: Logging context

:since: v1.0.0
        """

        # pylint: disable=protected-access

        level = self._get_implementation_level(kwargs.get("context", "global"))
        if (level in ( DEBUG, INFO )): self._write(INFO, data, *args)
    #

    def _init_handler(self):
        """
Initializes the underlying log handler.

:since: v1.0.0
        """

        # global: _api_type, _API_PYTHON

        log_file_path_name = Settings.get("global_log_path_name")

        if (log_file_path_name is not None):
            log_file_path_name = path.abspath(log_file_path_name)

            if (os.access(log_file_path_name, os.W_OK)
                or ((not os.access(log_file_path_name, os.F_OK))
                    and os.access(path.dirname(log_file_path_name), os.W_OK)
                   )
                ): self.log_file_path_name = log_file_path_name
        #

        if (self.log_file_path_name is None and Settings.is_defined("global_log_name")):
            log_file_path_name = path.join(Settings.get("path_base"), "log", Settings.get("global_log_name"))

            if (os.access(log_file_path_name, os.W_OK)
                or ((not os.access(log_file_path_name, os.F_OK))
                    and os.access(path.join(Settings.get("path_base"), "log"), os.W_OK)
                   )
                ): self.log_file_path_name = log_file_path_name
        #

        if (self.log_file_path_name is None): self.log_handler = StreamHandler(stderr)
        elif (_api_type == _API_PYTHON):
            self.log_handler = RotatingFileHandler(self.log_file_path_name,
                                                   maxBytes = self.log_file_size_max,
                                                   backupCount = self.log_file_rotates
                                                  )
        else: self.log_handler = FileHandler(self.log_file_path_name, self.log_file_size_max, self.log_file_rotates, True)
    #

    def _load_context_level(self, context):
        """
Determines the context specific log level.

:param context: Logging context

:since: v1.0.0
        """

        context_level_setting = "{0}_log_level".format(context)

        if (context != "global"):
            self.set_level((Settings.get(context_level_setting)
                            if (Settings.is_defined(context_level_setting)) else
                            self.get_level("global")
                           ),
                           context
                          )
        #
    #

    def warning(self, data, *args, **kwargs):
        """
Warning message method

:param data: Warning data
:param context: Logging context

:since: v1.0.0
        """

        # pylint: disable=protected-access

        level = self._get_implementation_level(kwargs.get("context", "global"))
        if (level not in ( ERROR, NOTSET )): self._write(WARNING, data, *args)
    #

    def _write(self, level, data, *args):
        """
"_write()" adds all messages to the logger instance.

:param level: Logging level
:param data: Logging data

:since: v1.0.0
        """

        exception = isinstance(data, BaseException)
        message = strftime(self.log_format_datetime)

        if (exception):
            level = CRITICAL
            message = "<exception> {0}".format(message)
        elif (level == ERROR): message = "<error>     {0}".format(message)
        elif (level == WARNING): message = "<warning>   {0}".format(message)
        elif (level == INFO): message = "<info>      {0}".format(message)
        elif (level == DEBUG): message = "<debug>     {0}".format(message)

        message = "{0} {1}".format(message, self._get_line(data, *args))

        if (level == CRITICAL): self.logger.critical(message)
        elif (level == ERROR): self.logger.error(message)
        elif (level == WARNING): self.logger.warning(message)
        elif (level == DEBUG): self.logger.debug(message)
        elif (level == INFO): self.logger.info(message)
    #
#
