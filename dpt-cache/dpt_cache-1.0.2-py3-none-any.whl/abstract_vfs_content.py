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
dpt_cache/abstract_vfs_content.py
"""

from os import path

from dpt_runtime.exceptions import NotImplementedException

from .abstract_file_content import AbstractFileContent

class AbstractVfsContent(AbstractFileContent):
    """
The abstract vfs cache defines methods to access cached data.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: cache
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def get_from_file(self, file_path_name):
        """
Get the content for the given file path and name cached.

:param file_path_name: File path and name

:return: (mixed) File content cached
:since:  v1.0.0
        """

        return self.get_from_vfs_url("file:///{0}".format(path.abspath(file_path_name)))
    #

    def get_from_vfs_url(self, vfs_url):
        """
Get the content for the given VFS URL cached.

:param vfs_url: VFS URL

:return: (mixed) VFS URL content cached
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def is_file_cached(self, file_path_name):
        """
Return true if the given file path and name is cached.

:param file_path_name: Cached file path and name

:return: (bool) True if currently cached
:since:  v1.0.0
        """

        return self.is_vfs_url_cached("file:///{0}".format(path.abspath(file_path_name)))
    #

    def is_vfs_url_cached(self, vfs_url):
        """
Return true if the given VFS URL is cached.

:param vfs_url: VFS URL

:return: (bool) True if currently cached
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def set_file(self, file_path_name, content, content_size = None):
        """
Fill the cache for the given file path and name with the given cached
content.

:param file_path_name: File path and name
:param content: Cached entry content
:param content_size: Size of the cached entry content

:since: v1.0.0
        """

        return self.set_vfs_url("file:///{0}".format(path.abspath(file_path_name)), content, content_size, True)
    #

    def set_vfs_url(self, vfs_url, content, content_size = None, is_compatibility_checked = False):
        """
Fill the cache for the given VFS URL with the given cached content.

:param vfs_url: VFS URL
:param content: Cached entry content
:param content_size: Size of the cached entry content

:since: v1.0.0
        """

        raise NotImplementedException()
    #
#
