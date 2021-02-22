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
dpt_plugins/hook_context.py
"""

from functools import wraps

from .hook import Hook

class HookContext(object):
    """
Provides an call context to provide "before", "after" and "exception" hooks.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: plugins
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=invalid-name

    __slots__ = [ "hook_prefix", "kwargs" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, hook_prefix, **kwargs):
        """
Constructor __init__(HookContext)

:since: v1.0.0
        """

        self.hook_prefix = hook_prefix
        """
Prefix used for ".before", ".after" and ".exception" calls
        """
        self.kwargs = kwargs
        """
Keyword arguments used for hook calls
        """
    #

    def __call__(self, f):
        """
python.org: Called when the instance is "called" as a function [..].

:since: v1.0.0
        """

        @wraps(f)
        def decorator(*args, **kwargs):
            """
Decorator for wrapping a function or method with a call context.
            """

            with self: return f(*args, **kwargs)
        #

        return decorator
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: v1.0.0
        """

        Hook.call("{0}.before".format(self.hook_prefix), **self.kwargs)
    #

    def __exit__(self, exc_type, exc_value, traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v1.0.0
        """

        if (exc_type is None and exc_value is None): Hook.call("{0}.after".format(self.hook_prefix), **self.kwargs)
        else: Hook.call("{0}.exception".format(self.hook_prefix), **self.kwargs)

        return False
    #
#
