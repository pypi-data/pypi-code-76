# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v2.0.0
dpt_runtime/environment.py
"""

import os

from .binary import Binary

class Environment(object):
    """
The "Environment" class provides support to access runtime specific paths
and names defined by an implementing application.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _base_path = None
    """
Base path for runtime specific files.
    """
    _short_name = None
    """
Short application name
    """
    _vendor = None
    """
Application vendor name
    """

    @staticmethod
    def get_application_short_name():
        """
Returns the short application name.

:return: (str) Short application name
:since:  v1.0.0
        """

        _return = Environment._short_name

        if (_return is None):
            _return = (Binary.str(os.environ['DPT_APP_NAME']) if ("DPT_APP_NAME" in os.environ) else "dNGpy")
        #

        return _return
    #

    @staticmethod
    def get_application_vendor():
        """
Returns the application vendor name.

:return: (str) Application vendor name
:since:  v1.0.0
        """

        _return = Environment._vendor

        if (_return is None):
            _return = (Binary.str(os.environ['DPT_APP_VENDOR']) if ("DPT_APP_VENDOR" in os.environ) else "dNG")
        #

        return _return
    #

    @staticmethod
    def is_application_short_name_defined():
        """
Returns true if an short application name is defined.

:return: (bool) True if short application name is defined
:since:  v1.0.0
        """

        return (Environment._short_name is not None or "DPT_APP_NAME" in os.environ)
    #

    @staticmethod
    def is_application_vendor_defined():
        """
Returns true if an application vendor name is defined.

:return: (bool) True if application vendor name is defined
:since:  v1.0.0
        """

        return (Environment._vendor is not None or "DPT_APP_VENDOR" in os.environ)
    #

    @staticmethod
    def set_application_short_name(name):
        """
Sets the short application name.

:param name: Short application name

:since: v1.0.0
        """

        Environment._short_name = Binary.str(name)
    #

    @staticmethod
    def set_application_vendor(name):
        """
Sets the application vendor name.

:param name: Application vendor name

:since: v1.0.0
        """

        Environment._vendor = Binary.str(name)
    #

    @staticmethod
    def get_base_path():
        """
Returns the base path for runtime specific files.

:return: (str) Base path of runtime files
:since:  v1.0.0
        """

        _return = Environment._base_path

        if (_return is None):
            _return = (Binary.str(os.environ['DPT_PATH'])
                       if ("DPT_PATH" in os.environ) else
                       os.getcwd()
                      )
        #

        return _return
    #

    @staticmethod
    def set_base_path(_path):
        """
Sets the base path for runtime specific files.

:param _path: Base path of runtime files

:since: v1.0.0
        """

        Environment._base_path = Binary.str(_path)
    #
#
