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
dpt_vfs/abstract_watcher.py
"""

# pylint: disable=unused-argument

from dpt_runtime.exceptions import NotImplementedException

class AbstractWatcher(object):
    """
Abstract watcher for change events.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    EVENT_TYPE_CREATED = 1
    """
Created event
    """
    EVENT_TYPE_DELETED = 2
    """
Deleted event
    """
    EVENT_TYPE_MODIFIED = 3
    """
Created event
    """

    __slots__ = [ "__weakref__" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @property
    def implementing_scheme(self):
        """
Returns the implementing scheme name.

:return: (str) Implementing scheme name
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def is_synchronous(self):
        """
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v1.0.0
        """

        return True
    #

    def check(self, url):
        """
Checks a given URL for changes if "is_synchronous()" is true.

:param url: Resource URL

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def free(self):
        """
Frees all watcher callbacks for garbage collection.

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def is_watched(self, url, callback = None):
        """
Returns true if the resource URL is already watched. It will return false
if a callback is given but not defined for the watched URL.

:param url: Resource URL
:param callback: Callback to be checked for the watched resource URL

:return: (bool) True if watched with the defined callback or any if not
         defined.
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def register(self, url, callback):
        """
Handles registration of resource URL watches and its callbacks.

:param url: Resource URL to be watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def stop(self):
        """
Stops all watchers.

:since: v1.0.0
        """

        pass
    #

    def unregister(self, url, callback):
        """
Handles deregistration of resource URL watches.

:param url: Resource URL watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @staticmethod
    def disable():
        """
Disables this watcher and frees all callbacks for garbage collection.

:since: v1.0.0
        """

        raise NotImplementedException()
    #
#
