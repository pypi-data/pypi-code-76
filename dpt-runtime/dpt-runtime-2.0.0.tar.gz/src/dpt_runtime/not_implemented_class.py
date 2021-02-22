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
dpt_runtime/not_implemented_class.py
"""

# pylint: disable=invalid-name

try: from types import new_class
except ImportError: new_class = None

from .exceptions import NotImplementedException

class _NotImplementedMetaClass(type):
    """
The "_NotImplementedMetaClass" is used as a Python 2 and Python 3 compatible
metaclass to raise "dpt_runtime.NotImplementedException" for class methods.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __getattr__(cls, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param cls: Python class
:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v1.0.0
        """

        raise NotImplementedException()
    #
#

class _NotImplementedClass(object):
    """
The "_NotImplementedClass" is used in connection with the
"_NotImplementedMetaClass" to raise "dpt_runtime.NotImplementedException"
for all class and instance method calls.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
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

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v1.0.0
        """

        raise NotImplementedException()
    #
#

NotImplementedClass = (_NotImplementedMetaClass("NotImplementedClass", ( _NotImplementedClass, ), { })
                       if (new_class is None) else
                       new_class("NotImplementedClass",
                                 ( _NotImplementedClass, ),
                                 { "metaclass": _NotImplementedMetaClass }
                                )
                      )
"""
The "NotImplementedClass" is used for features not available or implemented
on a specific installation.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
"""
