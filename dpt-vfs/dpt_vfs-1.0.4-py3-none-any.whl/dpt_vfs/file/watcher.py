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
dpt_vfs/dpt_vfs/file/watcher.py
"""

# pylint: disable=import-error,invalid-name,no-name-in-module

try: from urllib.parse import unquote_plus, urlsplit
except ImportError:
    from urllib import unquote_plus
    from urlparse import urlsplit
#

from dpt_logging import LogLine
from dpt_threading import InstanceLock

from ...abstract_watcher import AbstractWatcher
from .watcher_mtime import WatcherMtime

_IMPLEMENTATION_INOTIFY = 1
"""
pyinotify implementation
"""
_IMPLEMENTATION_INOTIFY_SYNC = 2
"""
Synchronous pyinotify implementation
"""
_IMPLEMENTATION_MTIME = 3
"""
Filesystem mtime implementation
"""

try:
    from .watcher_pyinotify import WatcherPyinotify
    from .watcher_pyinotify_sync import WatcherPyinotifySync
    _mode = _IMPLEMENTATION_INOTIFY
except ImportError:
    _mode = _IMPLEMENTATION_MTIME
    WatcherPyinotify = None
#

class Watcher(AbstractWatcher):
    """
"file:///" watcher for change events.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    IMPLEMENTATION_INOTIFY = _IMPLEMENTATION_INOTIFY
    """
pyinotify implementation
    """
    IMPLEMENTATION_INOTIFY_SYNC = _IMPLEMENTATION_INOTIFY_SYNC
    """
Synchronous pyinotify implementation
    """
    IMPLEMENTATION_MTIME = _IMPLEMENTATION_MTIME
    """
Filesystem mtime implementation
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _implementation = None
    """
Watcher implementation instance
    """
    _instance = None
    """
Watcher implementation instance
    """
    _lock = InstanceLock()
    """
Thread safety lock
    """

    def __init__(self):
        """
Constructor __init__(Watcher)

:since: v1.0.0
        """

        if (Watcher._instance is None):
            with Watcher._lock:
                if (Watcher._instance is None): self.set_implementation()
            #
        #
    #

    @property
    def implementing_scheme(self):
        """
Returns the implementing scheme name.

:return: (str) Implementing scheme name
:since:  v1.0.0
        """

        return "file"
    #

    @property
    def is_synchronous(self):
        """
Returns true if changes are only detected after "check()" has been
called.

:return: (bool) True if changes are not detected automatically
:since:  v1.0.0
        """

        with Watcher._lock: return (WatcherPyinotify is None or (not isinstance(Watcher._instance, WatcherPyinotify)))
    #

    def check(self, url):
        """
Checks a given URL for changes if "is_synchronous()" is true.

:param url: Resource URL

:since: v1.0.0
        """

        _path = Watcher._get_path(url)

        with Watcher._lock:
            if (Watcher._instance is not None
                and _path is not None
                and _path.strip() != ""
               ): Watcher._instance.check(_path)
        #
    #

    def free(self):
        """
Frees all watcher callbacks for garbage collection.

:since: v1.0.0
        """

        with Watcher._lock:
            if (Watcher._instance is not None): Watcher._instance.free()
        #
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

        _path = Watcher._get_path(url)

        with Watcher._lock:
            return (False
                    if (Watcher._instance is None or _path is None or _path.strip() == "") else
                    Watcher._instance.is_watched(_path, callback)
                   )
        #
    #

    def register(self, url, callback):
        """
Handles registration of resource URL watches and its callbacks.

:param url: Resource URL to be watched

:return: (bool) True on success
:since:  v1.0.0
        """

        _path = Watcher._get_path(url)

        with Watcher._lock:
            return (False
                    if (Watcher._instance is None or _path is None or _path.strip() == "") else
                    Watcher._instance.register(_path, callback)
                   )
        #
    #

    def set_implementation(self, implementation = None):
        """
Set the filesystem watcher implementation to use.

:param implementation: Implementation identifier

:since: v1.0.0
        """

        # global: _IMPLEMENTATION_INOTIFY, _IMPLEMENTATION_INOTIFY_SYNC, _IMPLEMENTATION_MTIME, _mode

        with Watcher._lock:
            if (Watcher._instance is not None): Watcher._instance.stop()

            if (_mode == _IMPLEMENTATION_INOTIFY
                and (implementation is None or implementation == _IMPLEMENTATION_INOTIFY)
            ): Watcher._implementation = _IMPLEMENTATION_INOTIFY
            elif (_mode == _IMPLEMENTATION_INOTIFY
                and implementation == _IMPLEMENTATION_INOTIFY_SYNC
                ): Watcher._implementation = _IMPLEMENTATION_INOTIFY_SYNC
            else: Watcher._implementation = _IMPLEMENTATION_MTIME

            Watcher._init_watcher()
        #
    #

    def stop(self):
        """
Stops all watchers.

:since: v1.0.0
        """

        with Watcher._lock:
            if (Watcher._instance is not None): Watcher._instance.stop()
        #
    #

    def unregister(self, url, callback):
        """
Handles deregistration of resource URL watches.

:param url: Resource URL watched

:return: (bool) True on success
:since:  v1.0.0
        """

        _path = Watcher._get_path(url)

        with Watcher._lock:
            return (False
                    if (Watcher._instance is None or _path is None or _path.strip() == "") else
                    Watcher._instance.unregister(_path, callback)
                   )
        #
    #

    @staticmethod
    def disable():
        """
Disables this watcher and frees all callbacks for garbage collection.

:since: v1.0.0
        """

        with Watcher._lock:
            if (Watcher._instance is not None):
                Watcher._instance.stop()
                Watcher._instance = None

                LogLine.debug("dpt_vfs.file.Watcher has been disabled", context = "dpt_vfs")
            #
        #
    #

    @staticmethod
    def _get_path(url):
        """
Return the local filesystem path for the given "file:///" URL.

:param url: Filesystem URL

:return: (str) Filesystem path; None if not a "file:///" URL
:since:  v1.0.0
        """

        url_elements = urlsplit(url)
        return (unquote_plus(url_elements.path[1:]) if (url_elements.scheme == "file") else None)
    #

    @staticmethod
    def _init_watcher():
        """
Initializes the watcher instance.

:since: v1.0.0
        """

        instance_callable = WatcherMtime

        if (WatcherPyinotify is not None):
            if (Watcher._implementation == _IMPLEMENTATION_INOTIFY): instance_callable = WatcherPyinotify.get_singleton
            elif (Watcher._implementation == _IMPLEMENTATION_INOTIFY_SYNC): instance_callable = WatcherPyinotifySync.get_singleton
        #

        try: Watcher._instance = instance_callable()
        except OSError:
            if (instance_callable is WatcherMtime): raise
            Watcher._instance = WatcherMtime()
        #
    #
#
