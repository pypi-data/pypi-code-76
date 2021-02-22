# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;plugins

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.2
dpt_plugins/hookable_settings.py
"""

from dpt_settings import Settings

from .hook import Hook

class HookableSettings(object):
    """
"HookableSettings" provide a hook based solution to set custom values for
requested settings in a given context and fall back to the default value
otherwise. Please note that None is not supported as a valid setting value.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: plugins
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "hook", "params", "settings" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, hook, **kwargs):
        """
Constructor __init__(HookableSettings)

:since: v1.0.0
        """

        self.hook = hook
        """
Hook called to get custom values
        """
        self.params = kwargs
        """
Hook parameters used to provide context relevant information
        """
        self.settings = Settings.get_dict()
        """
Settings instance
        """
    #

    def is_defined(self, key):
        """
Checks if a given key is a defined setting.

:param key: Settings key

:return: (bool) True if defined
:since:  v1.0.0
        """

        _return = True
        if (Hook.call(self.hook, **self.params) is None): _return = (key in self.settings)

        return _return
    #

    def get(self, key = None, default = None):
        """
Returns the value with the specified key.

:param key: Settings key
:param default: Default value if not set

:return: (mixed) Value
:since:  v1.0.0
        """

        _return = Hook.call(self.hook, **self.params)
        if (_return is None): _return = self.settings.get(key)
        if (_return is None and default is not None): _return = default

        return _return
    #
#
