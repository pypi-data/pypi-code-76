# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;cache

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.2
dpt_cache/content.py
"""

from weakref import ref

from dpt_settings import Settings
from dpt_threading import ThreadLock
from dpt_vfs import Implementation as VfsImplementation
from dpt_vfs import WatcherImplementation as VfsWatcherImplementation

#from .abstract_value import AbstractValue
from .abstract_vfs_content import AbstractVfsContent

class Content(AbstractVfsContent):
    """
The cache singleton for content provides memory-based caching mechanisms for
files as well as timestamp based content.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: cache
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    __slots__ = [ "__weakref__", "_cache", "_history", "_lock", "max_size", "size" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """
    _weakref_instance = None
    """
Cache weakref instance
    """

    def __init__(self):
        """
Constructor __init__(Content)

:since: v1.0.0
        """

        #AbstractValue.__init__(self)
        AbstractVfsContent.__init__(self)

        self._cache = { }
        """
Dictionary of cached entries
        """
        self._history = [ ]
        """
Holds a history of requests and updates (newest first)
        """
        self._lock = ThreadLock()
        """
Thread safety lock
        """
        self.max_size = int(Settings.get("global_cache_memory_max_size", 104857600))
        """
Max size of the cache
        """
        self.size = 0
        """
Size in bytes
        """
    #

    def get_from_vfs_url(self, vfs_url):
        """
Get the content for the given VFS URL cached.

:param vfs_url: VFS URL

:return: (mixed) VFS URL content cached
:since:  v1.0.0
        """

        _return = None

        vfs_scheme = VfsWatcherImplementation.get_scheme_from_vfs_url_if_supported(vfs_url)
        watcher = None

        if (vfs_scheme is not None):
            watcher = VfsWatcherImplementation.get_instance(vfs_scheme)
            if (watcher.is_synchronous): watcher.check(vfs_url)
        #

        if (vfs_url in self._cache):
            with self._lock:
                # Thread safety
                if (vfs_url in self._cache):
                    _return = self._cache[vfs_url]['entry']
                    self._history.remove(vfs_url)
                    self._history.insert(0, vfs_url)
                #
            #

            if (_return is not None and hasattr(_return, "copy")): _return = _return.copy()
        #

        if (_return is None):
            vfs_object = VfsImplementation.load_vfs_url(vfs_url, True)

            try:
                if ((watcher is None or vfs_object.is_supported("time_updated")) and vfs_object.is_valid):
                    vfs_object_size = vfs_object.size

                    if (vfs_object_size <= self.max_size):
                        _return = vfs_object.read()
                        self.set_vfs_url(vfs_url, _return, vfs_object_size, True)
                    #
                #
            finally: vfs_object.close()
        #

        return _return
    #

    def is_vfs_url_cached(self, vfs_url):
        """
Return true if the given VFS URL is cached.

:param vfs_url: VFS URL

:return: (bool) True if currently cached
:since:  v1.0.0
        """

        vfs_scheme = VfsWatcherImplementation.get_scheme_from_vfs_url_if_supported(vfs_url)
        watcher = (None if (vfs_scheme is None) else VfsWatcherImplementation.get_instance(vfs_scheme))
        if (watcher is not None and watcher.is_synchronous): watcher.check(vfs_url)

        return (vfs_url in self._cache)
    #

    def set_vfs_url(self, vfs_url, content, content_size = None, is_compatibility_checked = False):
        """
Fill the cache for the given VFS URL with the given cached content.

:param vfs_url: VFS URL
:param content: Cached entry content
:param content_size: Size of the cached entry content

:since: v1.0.0
        """

        if (content_size is None): content_size = len(content)

        vfs_scheme = VfsWatcherImplementation.get_scheme_from_vfs_url_if_supported(vfs_url)
        watcher = (None if (vfs_scheme is None) else VfsWatcherImplementation.get_instance(vfs_scheme))

        is_compatible = True

        if (watcher is not None and (not is_compatibility_checked)):
            vfs_object = VfsImplementation.load_vfs_url(vfs_url, True)
            is_compatible = (vfs_object.is_supported("time_updated") and vfs_object.is_valid)
        #

        if (is_compatible and content_size <= self.max_size):
            with self._lock:
                if (vfs_url not in self._cache):
                    if (watcher is not None
                        and (not watcher.is_watched(vfs_url, self._uncache_changed))
                       ): watcher.register(vfs_url, self._uncache_changed)

                    self._cache[vfs_url] = { "entry": content, "size": content_size }
                    self._history.insert(0, vfs_url)
                    self.size += content_size

                    while (self.size > self.max_size):
                        key = self._history.pop()

                        self.size -= len(self._cache[key]['size'])
                        del(self._cache[key])
                    #
                elif (self._cache[vfs_url]['entry'] != content):
                    self.size -= self._cache[vfs_url]['size']
                    self._history.remove(vfs_url)

                    self._cache[vfs_url] = { "entry": content, "size": content_size }
                    self._history.insert(0, vfs_url)
                    self.size += content_size
                #
            #
        #
    #

    def _uncache_changed(self, event_type, url, changed_value = None):
        """
Remove changed files from the cache.

:param event_type: Filesystem watcher event type
:param url: Filesystem URL watched
:param changed_value: Changed filesystem value

:since: v1.0.0
        """

        vfs_scheme = VfsWatcherImplementation.get_scheme_from_vfs_url(url)
        watcher = VfsWatcherImplementation.get_instance(vfs_scheme)

        vfs_url = (url if (changed_value is None) else "{0}/{1}".format(url, changed_value))

        if (vfs_url in self._cache):
            with self._lock:
                # Thread safety
                if (vfs_url in self._cache):
                    self.size -= self._cache[vfs_url]['size']
                    self._history.remove(vfs_url)
                    del(self._cache[vfs_url])

                    watcher.unregister(vfs_url, self._uncache_changed)
                #
            #
        #
    #

    @staticmethod
    def get_instance():
        """
Get the Content singleton.

:return: (Content) Object on success
:since:  v1.0.0
        """

        # pylint: disable=not-callable

        _return = (None if (Content._weakref_instance is None) else Content._weakref_instance())

        if (_return is None):
            _return = Content()
            Content._weakref_instance = ref(_return)
        #

        return _return
    #
#
