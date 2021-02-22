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
dpt_vfs/dpt_vfs/file/watcher_pyinotify_sync.py
"""

# pylint: disable=import-error

from dpt_logging import LogLine
from pyinotify import Notifier

from .watcher_pyinotify import WatcherPyinotify
from .watcher_pyinotify_callback import WatcherPyinotifyCallback

class WatcherPyinotifySync(WatcherPyinotify):
    """
"file:///" watcher using pyinotify's (synchronous) Notifier.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=bad-option-value,slots-on-old-class
    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def check(self, _path):
        """
Checks a given path for changes if "is_synchronous()" is true.

:param _path: Filesystem path

:return: (bool) True if the given path URL has been changed since last check
         and "is_synchronous()" is true.
:since:  v1.0.0
        """

        with self._lock:
            if (self._pyinotify_instance.check_events()):
                self._pyinotify_instance.read_events()
                self._pyinotify_instance.process_events()
            #
        #

        return False
    #

    def _init_notifier(self):
        """
Initializes the pyinotify instance.

:since: v1.0.0
        """

        with self._lock:
            if (self._pyinotify_instance is None):
                LogLine.debug("{0!r} mode is synchronous", self, context = "dpt_vfs")
                self._pyinotify_instance = Notifier(self, WatcherPyinotifyCallback(self), timeout = 5)
            #
        #
    #

    def stop(self):
        """
Stops all watchers.

:since: v1.0.0
        """

        with self._lock:
            self.free()
            self._pyinotify_instance = None
        #
    #
#
