# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;vfs

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.4
dpt_vfs/implementation.py
"""

from dpt_module_loader import NamedClassLoader
from dpt_runtime import Binary
from dpt_runtime.exceptions import IOException

from .abstract import Abstract

class Implementation(object):
    """
"Implementation" provides implementation independent methods to access VFS
objects.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    TYPE_DIRECTORY = Abstract.TYPE_DIRECTORY
    """
Directory (or collection like) type
    """
    TYPE_FILE = Abstract.TYPE_FILE
    """
File type
    """
    TYPE_LINK = Abstract.TYPE_LINK
    """
Link type
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def get_class(scheme):
        """
Returns an VFS object class for the given scheme.

:return: (object) VFS object class
:since:  v1.0.0
        """

        _return = NamedClassLoader.get_class_in_namespace("dpt_vfs", "{0}.Object".format(scheme.replace("-", "_")))

        if (_return is None
            or (not issubclass(_return, Abstract))
           ): raise IOException("VFS object not defined for URL scheme '{0}'".format(scheme))

        return _return
    #

    @staticmethod
    def get_instance(scheme):
        """
Returns an VFS object instance for the given scheme.

:return: (object) VFS object instance
:since:  v1.0.0
        """

        vfs_object_class = Implementation.get_class(scheme)
        return vfs_object_class()
    #

    @staticmethod
    def load_vfs_url(vfs_url, readonly = False):
        """
Returns the initialized object instance for the given VFS URL.

:param vfs_url: VFS URL
:param readonly: Open object in readonly mode

:return: (object) VFS object instance
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        vfs_url = Binary.str(vfs_url)
        scheme = Abstract._get_scheme_from_vfs_url(vfs_url)

        _return = Implementation.get_instance(scheme)
        _return.open(vfs_url, readonly)

        return _return
    #

    @staticmethod
    def new_vfs_url(_type, vfs_url):
        """
Returns a new object instance for the given VFS URL.

:param _type: VFS object type
:param vfs_url: VFS URL

:return: (object) VFS object instance
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        vfs_url = Binary.str(vfs_url)
        scheme = Abstract._get_scheme_from_vfs_url(vfs_url)

        _return = Implementation.get_instance(scheme)
        _return.new(_type, vfs_url)

        return _return
    #
#
