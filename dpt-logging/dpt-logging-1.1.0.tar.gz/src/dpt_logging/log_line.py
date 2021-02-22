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
dpt_logging/log_line.py
"""

from dpt_module_loader import NamedClassLoader

class LogLine(object):
    """
"LogLine" provides static methods to log a single line to the active log
handler.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: logging
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def debug(data, *args, **kwargs):
        """
Debug message method

:param data: Debug data
:param context: Logging context

:since: v1.0.0
        """

        log_handler = NamedClassLoader.get_singleton("dpt_logging.LogHandler", False)
        if (log_handler is not None): log_handler.debug(data, *args, **kwargs)
    #

    @staticmethod
    def error(data, *args, **kwargs):
        """
Error message method

:param data: Error data
:param context: Logging context

:since: v1.0.0
        """

        log_handler = NamedClassLoader.get_singleton("dpt_logging.LogHandler", False)
        if (log_handler is not None): log_handler.error(data, *args, **kwargs)
    #

    @staticmethod
    def info(data, *args, **kwargs):
        """
Info message method

:param data: Info data
:param context: Logging context

:since: v1.0.0
        """

        log_handler = NamedClassLoader.get_singleton("dpt_logging.LogHandler", False)
        if (log_handler is not None): log_handler.info(data, *args, **kwargs)
    #

    @staticmethod
    def warning(data, *args, **kwargs):
        """
Warning message method

:param data: Warning data
:param context: Logging context

:since: v1.0.0
        """

        log_handler = NamedClassLoader.get_singleton("dpt_logging.LogHandler", False)
        if (log_handler is not None): log_handler.warning(data, *args, **kwargs)
    #
#
