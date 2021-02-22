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
dpt_vfs/file_like_wrapper_mixin.py
"""

from dpt_runtime.exceptions import IOException

class FileLikeWrapperMixin(object):
    """
The "FileLikeWrapperMixin" redirects FileIO to the registered wrapped
instance.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=assigning-non-slot

    _FILE_WRAPPED_METHODS = ( "flush",
                              "read",
                              "seek",
                              "tell",
                              "truncate",
                              "write"
                            )
    """
File IO methods implemented by an wrapped resource.
    """

    _mixin_slots_ = [ "_wrapped_resource" ]
    """
Additional __slots__ used for inherited classes.
    """
    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(FileLikeWrapperMixin)

:since: v1.0.0
        """

        self._wrapped_resource = None
        """
Wrapped file-like resource
        """
    #

    def __getattribute__(self, name):
        """
python.org: Called unconditionally to implement attribute accesses for
instances of the class.

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  v1.0.0
        """

        # pylint: disable=protected-access

        if (name == "__class__"
            or name not in self.__class__._FILE_WRAPPED_METHODS
           ): _return = object.__getattribute__(self, name)
        else:
            if (self._wrapped_resource is None): self._open_wrapped_resource()
            if (self._wrapped_resource is None): raise IOException("'{0}' not available for {1!r}".format(name, self))

            _return = getattr(self._wrapped_resource, name)
        #

        return _return
    #

    @property
    def _is_wrapped_resource_open(self):
        """
Returns true if a wrapped resource has been opened for this object.

:return: (bool) True if wrapped resource has been opened
:since:  v1.0.0
        """

        return (self._wrapped_resource is not None)
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        if (self._wrapped_resource is not None):
            try: self._wrapped_resource.close()
            finally: self._wrapped_resource = None
        #
    #

    def _open_wrapped_resource(self):
        """
Opens the wrapped resource once needed.

:since: v1.0.0
        """

        pass
    #

    def _set_wrapped_resource(self, resource):
        """
Sets the wrapped resource for this object.

:param resource: Resource providing the file-like API

:since: v1.0.0
        """

        self._wrapped_resource = resource
    #
#
