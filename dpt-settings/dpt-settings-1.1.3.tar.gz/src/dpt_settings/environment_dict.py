# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;settings

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.1.3
dpt_settings/environment_dict.py
"""

# pylint: disable=import-error

from os import environ
import re

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

class EnvironmentDict(Mapping):
    """
The "Environment" mapping is used to read settings from environment
variables.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: settings
:since:      v1.1.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    RE_SPECIAL_CHARACTERS = re.compile("\\W+")
    """
RegExp to find non-word characters
    """

    __slots__ = [ "_prefix" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, prefix = None):
        """
Constructor __init__(EnvironmentDict)

:since: v1.1.0
        """

        self._prefix = None
        """
Environment variable names prefix
        """

        if (isinstance(prefix, str)
            and prefix != ""
           ): self._prefix = "{0}_".format(EnvironmentDict.RE_SPECIAL_CHARACTERS.sub("_", prefix)).upper()
    #

    def __eq__(self, other):
        """
python.org: The correspondence between operator symbols and method names is
as follows: x==y calls x.__eq__(y)

:param other: Object to be compaired with

:return: (bool) True if equal
:since:  v1.1.0
        """

        return (isinstance(other, EnvironmentDict) and Mapping.__eq__(self, other))
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param key: Database instance to access

:return: (mixed) Database attribute value
:since:  v1.1.0
        """

        return environ[self._get_variable_name_for_key(key)]
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v1.1.0
        """

        for key in self.variable_names: yield key
    #

    def __len__(self):
        """
python.org: Called to implement the built-in function len().

:return: (int) Number of database instance attributes
:since: v1.1.0
        """

        return len(self.variable_names)
    #

    @property
    def variable_names(self):
        """
Returns all environment variables matching the configured prefix or all.

:return: (list) Matched environment variable names
:since:  v1.1.0
        """

        prefix_len = (0 if (self._prefix is None) else len(self._prefix))

        return [ key[prefix_len:]
                 for key in environ if ((self._prefix is None
                                         or key.upper().startswith(self._prefix)
                                        )
                                        and EnvironmentDict.RE_SPECIAL_CHARACTERS.search(key) is None
                                       )
               ]
    #

    def _get_variable_name_for_key(self, key):
        """
Returns the environment variable name for the given key.

:return: (str) Environment variable name
:since:  v1.1.0
        """

        name = EnvironmentDict.RE_SPECIAL_CHARACTERS.sub("_", key.upper())
        return (name if (self._prefix is None) else self._prefix + name)
    #
#
