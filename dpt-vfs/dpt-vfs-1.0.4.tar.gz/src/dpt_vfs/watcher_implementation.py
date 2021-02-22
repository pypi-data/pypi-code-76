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
dpt_vfs/watcher_implementation.py
"""

from dpt_module_loader import NamedClassLoader
from dpt_runtime import Binary
from dpt_runtime.exceptions import IOException, OperationNotSupportedException, ValueException
from dpt_threading import ThreadLock

from .abstract_watcher import AbstractWatcher

class WatcherImplementation(object):
    """
"WatcherImplementation" provides implementation independent methods to
access VFS watchers.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    EVENT_TYPE_CREATED = AbstractWatcher.EVENT_TYPE_CREATED
    """
Created event
    """
    EVENT_TYPE_DELETED = AbstractWatcher.EVENT_TYPE_DELETED
    """
Deleted event
    """
    EVENT_TYPE_MODIFIED = AbstractWatcher.EVENT_TYPE_MODIFIED
    """
Created event
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _classes = { }
    """
True if existing watchers have been disabled and no new ones can be
initialized.
    """
    _is_disabled = False
    """
True if existing watchers have been disabled and no new ones can be
initialized.
    """
    _lock = ThreadLock()
    """
Thread safety lock
    """

    @staticmethod
    def disable():
        """
Disables all watchers and free callbacks for garbage collection.

:since: v1.0.0
        """

        with WatcherImplementation._lock:
            if (not WatcherImplementation._is_disabled):
                WatcherImplementation._is_disabled = True

                for vfs_scheme in WatcherImplementation._classes: WatcherImplementation._classes[vfs_scheme].disable()
                WatcherImplementation._classes = None
            #
        #
    #

    @staticmethod
    def get_class(scheme):
        """
Returns an VFS watcher class for the given scheme.

:return: (object) VFS watcher class
:since:  v1.0.0
        """

        with WatcherImplementation._lock:
            if (WatcherImplementation._is_disabled): raise OperationNotSupportedException("VFS watcher creation has been disabled")

            _return = WatcherImplementation._classes.get(scheme)

            if (_return is None):
                _return = NamedClassLoader.get_class_in_namespace("dpt_vfs", "{0}.Watcher".format(scheme.replace("-", "_")))

                if (issubclass(_return, AbstractWatcher)): WatcherImplementation._classes[scheme] = _return
                else: _return = None
            #
        #

        if (_return is None): raise IOException("VFS watcher not defined for URL scheme '{0}'".format(scheme))

        return _return
    #

    @staticmethod
    def get_instance(scheme):
        """
Returns an VFS watcher instance for the given scheme.

:return: (object) VFS watcher instance
:since:  v1.0.0
        """

        vfs_watcher_class = WatcherImplementation.get_class(scheme)
        return vfs_watcher_class()
    #

    @staticmethod
    def get_scheme_from_vfs_url(vfs_url):
        """
Returns the scheme of the VFS URL given.

:param vfs_url: VFS URL to extract the scheme from.

:return: (str) VFS URL scheme
:since:  v1.0.0
        """

        vfs_url = Binary.str(vfs_url)
        if (type(vfs_url) is not str): raise ValueException("VFS URL given is invalid")

        vfs_url_data = vfs_url.split("://", 1)
        if (len(vfs_url_data) == 1): raise ValueException("VFS URL '{0}' is invalid".format(vfs_url))

        return vfs_url_data[0]
    #

    @staticmethod
    def get_scheme_from_vfs_url_if_supported(vfs_url):
        """
Returns the scheme of the VFS URL given if it is supported.

:param vfs_url: VFS URL to extract the scheme from.

:return: (str) VFS URL scheme if supported; None otherwise
:since:  v1.0.0
        """

        _return = None

        if (not WatcherImplementation.is_disabled()):
            try:
                scheme = WatcherImplementation.get_scheme_from_vfs_url(vfs_url)

                if (NamedClassLoader.is_defined_in_namespace("dpt_vfs", "{0}.Watcher".format(scheme.replace("-", "_")))):
                    _return = scheme
                #
            except ValueException: pass
        #

        return _return
    #

    @staticmethod
    def is_disabled():
        """
Returns true VFS watchers are disabled.

:return: (bool) True if disabled
:since:  v1.0.0
        """

        with WatcherImplementation._lock: return WatcherImplementation._is_disabled
    #
#
