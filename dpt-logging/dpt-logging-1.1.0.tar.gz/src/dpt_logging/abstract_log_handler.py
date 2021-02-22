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
dpt_logging/abstract_log_handler.py
"""

from threading import current_thread
from weakref import ref
import logging
import re
import sys
import traceback

from dpt_runtime import Binary, Environment
from dpt_runtime.exceptions import NotImplementedException, TracedException, ValueException
from dpt_threading import InstanceLock

class AbstractLogHandler(object):
    """
The abstract log handler provides common variables and methods.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: logging
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "__weakref__", "_ident", "level", "level_map", "log_handler", "log_thread_id", "_version" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _weakref_instance = None
    """
LogHandler weakref instance
    """
    _weakref_lock = InstanceLock()
    """
Thread safety weakref lock
    """

    def __init__(self):
        """
Constructor __init__(AbstractLogHandler)

:since: v1.0.0
        """

        self._ident = Environment.get_application_short_name()
        """
Log identifier
        """
        self.level = { }
        """
Log level
        """
        self.level_map = { }
        """
Mapped log levels
        """
        self.log_handler = None
        """
The configured log handler
        """
        self.log_thread_id = False
        """
True to add the thread ID to each log line as well
        """
        self._version = "v1.1.0"
        """
Version identifier
        """
    #

    @property
    def log_identifier(self):
        """
Returns the log identifier of the LogHandler in use.

:return: (str) Log identifier
:since:  v1.0.0
        """

        return self._ident
    #

    @log_identifier.setter
    def log_identifier(self, ident):
        """
Sets the log identifier of the LogHandler in use.

:param ident: Log identifier

:since: v1.0.0
        """

        self._ident = ident
    #

    @property
    def version_identifier(self):
        """
Returns the version identifier of the LogHandler in use.

:return: (str) Version identifier
:since:  v1.0.0
        """

        return self._version
    #

    @version_identifier.setter
    def version_identifier(self, version):
        """
Sets the version identifier of the LogHandler in use.

:param version: Version identifier

:since: v1.0.0
        """

        self._version = version
    #

    def add_logger(self, name):
        """
Add the logger name given to the active log handler.

:return: (object) Log handler
:since:  v1.0.0
        """

        logging.getLogger(name).addHandler(self.log_handler)
    #

    def debug(self, data, *args, **kwargs):
        """
Debug message method

:param data: Debug data
:param context: Logging context

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def error(self, data, *args, **kwargs):
        """
Error message method

:param data: Error data
:param context: Logging context

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def _get_implementation_level(self, context = "global"):
        """
Returns the log implementation specific level value.

:param context: Logging context

:return: (mixed) Log implementation specific level value
:since:  v1.0.0
        """

        if (context not in self.level): self._load_context_level(context)
        return self.level[context]
    #

    def get_level(self, context = "global"):
        """
Get the log level.

:param context: Logging context

:return: (mixed) Log level
:since:  v1.0.0
        """

        if (context not in self.level): self._load_context_level(context)

        level_matches = [ k for k, v in self.level_map.items() if self.level[context] == v ]

        if (len(level_matches) > 0): _return = level_matches[0]
        elif (context != "global" and len(level_matches) < 0): _return = self.get_level("global")
        else: raise ValueException("Log level can not be identified")

        return _return
    #

    def _get_line(self, data, *args):
        """
Get the formatted log message.

:param data: Log data

:return: (str) Formatted log line
:since:  v1.0.0
        """

        # pylint: disable=broad-except

        if (isinstance(data, TracedException)): data = data.printable_trace
        elif (isinstance(data, BaseException)):
            try:
                # Try to extract exception - might result in the wrong one
                ( exc_type, exc_value, exc_traceback ) = sys.exc_info()
                data = "{0} {1}".format(repr(data), "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            except Exception: data = repr(data)
        else:
            data = Binary.str(data)

            if (type(data) is not str): data = repr(data)
            elif (len(args) > 0): data = data.format(*args)
        #

        if ("\n" in data or "\r" in data): data = "\"" + re.sub("[\n\r]", "\"; \"", data) + "\""

        ident = self._ident
        if (self.log_thread_id): ident += " [Thread {0}]".format(current_thread().ident)

        _return = "{0} {1} {2}".format(ident, data, self._version)

        return _return
    #

    def info(self, data, *args, **kwargs):
        """
Info message method

:param data: Info data
:param context: Logging context

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def _load_context_level(self, context):
        """
Determines the context specific log level.

:param context: Logging context

:since: v1.0.0
        """

        if (context != "global"): self.level[context] = self.level['global']
    #

    def set_level(self, level, context = "global"):
        """
Sets the log level.

:param level: Log level identifier
:param context: Logging context

:since: v1.0.0
        """

        if (level in self.level_map): self.level[context] = self.level_map[level]
    #

    def warning(self, data, *args, **kwargs):
        """
Warning message method

:param data: Warning data
:param context: Logging context

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """
Get the log handler singleton.

:param cls: Python class

:return: (object) Log handler instance on success
:since:  v1.0.0
        """

        # pylint: disable=not-callable

        _return = None

        with AbstractLogHandler._weakref_lock:
            if (AbstractLogHandler._weakref_instance is not None): _return = AbstractLogHandler._weakref_instance()

            if (_return is None and cls is not AbstractLogHandler):
                _return = cls(*args, **kwargs)
                AbstractLogHandler._weakref_instance = ref(_return)
            #
        #

        return _return
    #
#
