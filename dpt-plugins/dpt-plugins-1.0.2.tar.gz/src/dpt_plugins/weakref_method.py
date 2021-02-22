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
dpt_plugins/weakref_method.py
"""

from weakref import ref

from dpt_runtime.exceptions import ValueException

class WeakrefMethod(object):
    """
This class provides a weak reference to an instance method.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: plugins
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "__weakref__", "_instance_object", "_method_name_value" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, method):
        """
Constructor __init__(WeakrefMethod)

:param method: Instance method to be bound

:since: v1.0.0
        """

        if (not hasattr(method, "__self__")): raise ValueException("Instance method given is invalid")

        self._instance_object = ref(method.__self__)
        """
Weakly referenced instance
        """
        self._method_name_value = method.__name__
        """
Instance method name
        """
    #

    def __call__(self):
        """
python.org: Called when the instance is "called" as a function [..].

:return: (object) Bound method; None if garbage collected
:since:  v1.0.0
        """

        instance = self._instance
        return (None if (instance is None) else getattr(instance, self._method_name_value))
    #

    def __eq__(self, other):
        """
python.org: The correspondence between operator symbols and method names is
as follows: x==y calls x.__eq__(y)

:param other: Object to be compaired with

:return: (bool) True if equal
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        instance = self._instance

        return (instance is not None
                and isinstance(other, WeakrefMethod)
                and instance == other._instance
                and self._method_name == other._method_name
               )
    #

    def __ne__(self, other):
        """
python.org: The correspondence between operator symbols and method names is
as follows: x!=y and x<>y call x.__ne__(y)

:param other: Object to be compaired with

:return: (bool) True if not equal
:since:  v1.0.0
        """

        return (not (self == other))
    #

    @property
    def _instance(self):
        """
Returns the bound instance.

:return: (object) Bound instance; None if garbage collected
:since:  v1.0.0
        """

        return self._instance_object()
    #

    @property
    def _method_name(self):
        """
Returns the method name of this weak reference instance.

:return: (str) Method name
:since:  v1.0.0
        """

        return self._method_name_value
    #
#
