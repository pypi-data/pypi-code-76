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
dpt_cache/file_content.py
"""

from dpt_file import File
from dpt_logging import LogLine
from dpt_module_loader import NamedClassLoader
from dpt_runtime.exceptions import IOException

from .abstract_file_content import AbstractFileContent

class FileContent(object):
    """
"FileContent" provides generic access to files on disk or cached.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: cache
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def is_changed(file_path_name):
        """
Returns true if the file is not cached or modified.

:param file_path_name: File path and name

:return: (bool) True if not cached or modified
:since:  v1.0.0
        """

        cache_instance = NamedClassLoader.get_singleton("dpt_cache.Content", False)
        return (not (isinstance(cache_instance, AbstractFileContent) and cache_instance.is_file_cached(file_path_name)))
    #

    @staticmethod
    def get(file_path_name, required = False):
        """
Get file content from cache or file.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v1.0.0
        """

        _return = FileContent._get_cached_file(file_path_name)
        if (_return is None): _return = FileContent._read_file(file_path_name, required)

        return _return
    #

    @staticmethod
    def _get_cached_file(file_path_name):
        """
Read data from cache.

:param file_path_name: File path and name

:return: (mixed) File data; None on error
:since:  v1.0.0
        """

        cache_instance = NamedClassLoader.get_singleton("dpt_cache.Content", False)
        return (cache_instance.get_from_file(file_path_name) if (isinstance(cache_instance, AbstractFileContent)) else None)
    #

    @staticmethod
    def _read_file(file_path_name, required):
        """
Read data from the given file or from cache.

:param file_path_name: File path and name
:param required: True if missing files should throw an exception

:return: (mixed) File data; None on error
:since:  v1.0.0
        """

        _return = None

        file_object = File()

        if (file_object.open(file_path_name, True, "r")):
            _return = file_object.read()
            file_object.close()

            if (_return is not None): _return = _return.replace("\r", "")
        elif (required): raise IOException("{0} not found".format(file_path_name))
        else: LogLine.debug("{0} not found", file_path_name, context = "dpt_cache")

        return _return
    #
#
