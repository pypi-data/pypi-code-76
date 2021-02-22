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
dpt_logging/exception_log_trap.py
"""

import traceback

from .log_line import LogLine

class ExceptionLogTrap(object):
    """
"ExceptionLogTrap" provides a context where exceptions are catched, logged and
suppressed.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    dpt
:subpackage: logging
:since:      v1.1.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "context" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, context = None):
        """
Constructor __init__(ExceptionLogTrap)

:param context: Logging context

:since: v1.1.0
        """

        self.context = context
        """
Logging context
        """
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: v1.1.0
        """

        pass
    #

    def __exit__(self, exc_type, exc_value, _traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v1.1.0
        """

        if (exc_type is not None or exc_value is not None):
            traceback_string = "".join(traceback.format_exception(exc_type, exc_value, _traceback))
            LogLine.error("Exception: {0}\n{1}".format(exc_value, traceback_string), context = self.context)
        #

        return True
    #
#
