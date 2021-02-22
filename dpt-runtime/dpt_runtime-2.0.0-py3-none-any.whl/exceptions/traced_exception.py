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
dpt_runtime/exceptions/traced_exception.py
"""

# pylint: disable=invalid-name

try: from types import new_class
except ImportError: new_class = None

from .traced_exception_mixin import TracedExceptionMixin

class TracedExceptionMetaClass(type):
    """
The "TracedExceptionMetaClass" is used as a Python 2 and Python 3 compatible
metaclass to return true for all inherited classes implementing
"dpt_runtime.TracedExceptionMixin".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __instancecheck__(cls, instance):
        """
python.org: Return true if instance should be considered a (direct or
indirect) instance of class.

:param cls: Python class
:param instance: Instance to check

:return: (bool) True if instance of "TracedExceptionMixin" for
         "TracedException"
:since:  v2.0.0
        """

        return ((cls is TracedException and issubclass(instance.__class__, cls))
                or isinstance(instance, _TracedException)
               )
    #

    def __subclasscheck__(cls, subclass):
        """
python.org: Return true if subclass should be considered a (direct or
indirect) subclass of class.

:param cls: Python class
:param subclass: Class to check

:return: (bool) True if subclass of "TracedExceptionMixin" for
         "TracedException"
:since:  v2.0.0
        """

        return ((cls is TracedException and issubclass(subclass, TracedExceptionMixin))
                or issubclass(subclass, _TracedException)
               )
    #
#

class _TracedException(RuntimeError, TracedExceptionMixin):
    """
"_TracedException" class extends "RuntimeError" to implement
"TracedExceptionMixin".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = TracedExceptionMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, value, _exception = None):
        """
Constructor __init__(TracedException)

:param value: Exception message value
:param _exception: Inner exception

:since: v2.0.0
        """

        super(_TracedException, self).__init__(value)
        TracedExceptionMixin.__init__(self, _exception)
    #

    __str__ = TracedExceptionMixin.__str__
    """
python.org: Called by the str(object) and the built-in functions format()
and print() to compute the "informal" or nicely printable string
representation of an object.

:return: (str) The "informal" or nicely printable string representation
:since:  v2.0.0
    """

    with_traceback = TracedExceptionMixin.with_traceback
    """
python.org: This method sets tb as the new traceback for the exception and
returns the exception object.

:param tb: New traceback for the exception

:return: (object) Manipulated exception instance
:since:  v2.0.0
    """
#

TracedException = (TracedExceptionMetaClass("TracedException", ( _TracedException, ), { })
                   if (new_class is None) else
                   new_class("TracedException", ( _TracedException, ), { "metaclass": TracedExceptionMetaClass })
                  )
"""
The "TracedException" class is used in connection with the
"TracedExceptionMetaClass" to return true for all inherited ones
implementing "TracedExceptionMixin".

To derive from "TracedException" use "_TracedException".

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
            Mozilla Public License, v. 2.0
"""
