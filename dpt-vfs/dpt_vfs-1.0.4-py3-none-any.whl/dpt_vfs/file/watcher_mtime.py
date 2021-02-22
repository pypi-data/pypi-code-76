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
dpt_vfs/dpt_vfs/file/watcher_mtime.py
"""

# pylint: disable=import-error,no-name-in-module

import os

try: from urllib.parse import quote_plus
except ImportError: from urllib import quote_plus

from dpt_logging import ExceptionLogTrap
from dpt_threading import ThreadLock

from ...abstract_watcher import AbstractWatcher

class WatcherMtime(object):
    """
"file:///" watcher using os.stat to detect changes.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _lock = ThreadLock()
    """
Thread safety lock
    """
    _watched_callbacks = { }
    """
Callbacks for watched files
    """
    _watched_paths = { }
    """
Dict with latest modified timestamps
    """

    def check(self, _path):
        """
Checks a given path for changes if "is_synchronous()" is true.

:param _path: Filesystem path

:return: (bool) True if the given path URL has been changed since last check
         and "is_synchronous()" is true.
:since:  v1.0.0
        """

        _return = False

        event_type = None

        with WatcherMtime._lock:
            if (WatcherMtime._watched_paths is not None
                and _path in WatcherMtime._watched_paths
               ):
                modified_time = (os.stat(_path).st_mtime if (os.access(_path, os.R_OK)) else -1)

                if (modified_time < 0):
                    event_type = AbstractWatcher.EVENT_TYPE_DELETED
                    self.unregister(_path, None)
                elif (WatcherMtime._watched_paths[_path] != modified_time):
                    event_type = (AbstractWatcher.EVENT_TYPE_CREATED
                                  if (WatcherMtime._watched_paths[_path] < 0) else
                                  AbstractWatcher.EVENT_TYPE_MODIFIED
                                 )

                    WatcherMtime._watched_paths[_path] = modified_time
                #
            #
        #

        if (event_type is not None):
            _return = True

            url = "file:///{0}".format(quote_plus(_path, "/"))

            for callback in WatcherMtime._watched_callbacks[_path]:
                with ExceptionLogTrap("dpt_vfs"): callback(event_type, url)
            #
        #

        return _return
    #

    def free(self):
        """
Frees all watcher callbacks for garbage collection.

:since: v1.0.0
        """

        with WatcherMtime._lock:
            if (WatcherMtime._watched_paths is not None and len(WatcherMtime._watched_paths) > 0):
                WatcherMtime._watched_callbacks = None
                WatcherMtime._watched_paths = None
            #
        #
    #

    def is_watched(self, _path, callback = None):
        """
Returns true if the filesystem path is already watched. It will return false
if a callback is given but not defined for the watched path.

:param _path: Filesystem path
:param callback: Callback to be checked for the watched filesystem path

:return: (bool) True if watched with the defined callback or any if not
         defined.
:since:  v1.0.0
        """

        with WatcherMtime._lock:
            _return = (WatcherMtime._watched_paths is not None and _path in WatcherMtime._watched_paths)
            if (_return and callback is not None): _return = (callback in WatcherMtime._watched_callbacks[_path])
        #

        return _return
    #

    def register(self, _path, callback):
        """
Handles registration of filesystem watches and its callbacks.

:param _path: Filesystem path to be watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v1.0.0
        """

        _return = True

        with WatcherMtime._lock:
            if (WatcherMtime._watched_callbacks is not None):
                if (_path not in WatcherMtime._watched_paths):
                    WatcherMtime._watched_paths[_path] = (os.stat(_path).st_mtime if (os.access(_path, os.R_OK)) else -1)
                    WatcherMtime._watched_callbacks[_path] = [ ]
                #

                if (callback not in WatcherMtime._watched_callbacks[_path]): WatcherMtime._watched_callbacks[_path].append(callback)
            #
        #

        return _return
    #

    def stop(self):
        """
Stops all watchers.

:since: v1.0.0
        """

        self.free()
    #

    def unregister(self, _path, callback):
        """
Handles deregistration of filesystem watches.

:param _path: Filesystem path watched
:param callback: Callback for the path

:return: (bool) True on success
:since:  v1.0.0
        """

        _return = True

        with WatcherMtime._lock:
            if (WatcherMtime._watched_paths is not None and _path in WatcherMtime._watched_paths):
                if (callback is None): WatcherMtime._watched_callbacks[_path] = [ ]
                elif (callback in WatcherMtime._watched_callbacks[_path]):
                    WatcherMtime._watched_callbacks[_path].remove(callback)
                #

                if (len(WatcherMtime._watched_callbacks[_path]) < 1):
                    del(WatcherMtime._watched_callbacks[_path])
                    del(WatcherMtime._watched_paths[_path])
                #
            else: _return = False
        #

        return _return
    #
#
