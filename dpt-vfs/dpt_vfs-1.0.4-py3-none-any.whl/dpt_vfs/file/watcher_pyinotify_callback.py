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
dpt_vfs/dpt_vfs/file/watcher_pyinotify_callback.py
"""

# pylint: disable=import-error,no-name-in-module

from os import path
from weakref import ref

try: from urllib.parse import quote_plus
except ImportError: from urllib import quote_plus

from dpt_logging import ExceptionLogTrap
from dpt_runtime import Binary
from pyinotify import ProcessEvent

from ...abstract_watcher import AbstractWatcher

class WatcherPyinotifyCallback(ProcessEvent):
    """
Processes pyinotify events and calls defined callbacks.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=invalid-name

    # pylint: disable=bad-option-value,slots-on-old-class
    __slots__ = [ "manager_weakref" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, manager):
        """
Constructor __init__(WatcherPyinotifyCallback)

:since: v1.0.0
        """

        ProcessEvent.__init__(self)

        self.manager_weakref = ref(manager)
        """
pyinotify manager instance
        """
    #

    def _process_callbacks(self, event_type, _path, changed_value = None):
        """
Handles all inotify events.

:param event_type: Event type defined in AbstractWatcher
:param _path: Filesystem path
:param changed_value: Changed value (e.g. name of deleted or created file)

:since: v1.0.0
        """

        changed_value = Binary.str(changed_value)
        manager = self.manager_weakref()
        _path = Binary.str(_path)

        changed_path = (_path if (changed_value is None) else path.join(_path, changed_value))

        if (manager and manager.is_watched(changed_path)):
            callbacks = manager.get_callbacks(changed_path)
            url = "file:///{0}".format(quote_plus(_path, "/"))

            for callback in callbacks:
                with ExceptionLogTrap("dpt_vfs"): callback(event_type, url, changed_value)
            #
        #
    #

    def process_IN_ATTRIB(self, event):
        """
Handles "IN_ATTRIB" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_MODIFIED, event.pathname)
    #

    def process_IN_CLOSE_WRITE(self, event):
        """
Handles "IN_CLOSE_WRITE" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_MODIFIED, event.pathname)
    #

    def process_IN_CREATE(self, event):
        """
Handles "IN_CREATE" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        dir_path = path.dirname(event.pathname)
        name = path.basename(event.pathname)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_CREATED, dir_path, name)
    #

    def process_IN_DELETE(self, event):
        """
Handles "IN_DELETE" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        dir_path = path.dirname(event.pathname)
        name = path.basename(event.pathname)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, dir_path, name)
    #

    def process_IN_DELETE_SELF(self, event):
        """
Handles "IN_DELETE_SELF" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        manager = self.manager_weakref()
        if (manager): manager.unregister(event.pathname, None, True)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.pathname)
    #

    def process_IN_MOVE_SELF(self, event):
        """
Handles "IN_MOVE_SELF" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        manager = self.manager_weakref()
        if (manager): manager.unregister(event.pathname, None, True)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, event.pathname)
    #

    def process_IN_MOVED_FROM(self, event):
        """
Handles "IN_MOVED_FROM" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        dir_path = path.dirname(event.pathname)
        name = path.basename(event.pathname)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_DELETED, dir_path, name)
    #

    def process_IN_MOVED_TO(self, event):
        """
Handles "IN_MOVED_TO" inotify events.

:param event: pyinotify event

:since: v1.0.0
        """

        dir_path = path.dirname(event.pathname)
        name = path.basename(event.pathname)

        self._process_callbacks(AbstractWatcher.EVENT_TYPE_CREATED, dir_path, name)
    #
#
