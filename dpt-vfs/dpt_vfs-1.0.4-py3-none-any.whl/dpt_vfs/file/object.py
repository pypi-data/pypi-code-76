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
dpt_vfs/dpt_vfs/file/object.py
"""

# pylint: disable=import-error,invalid-name,no-member,no-name-in-module

from os import path
import os

try: from urllib.parse import quote_plus, unquote_plus
except ImportError: from urllib import quote_plus, unquote_plus

from dpt_file import File
from dpt_logging import LogLine
from dpt_mime_type import MimeType
from dpt_runtime.exceptions import IOException, OperationNotSupportedException

from ...abstract import Abstract
from ...file_like_wrapper_mixin import FileLikeWrapperMixin

if (hasattr(os, "PathLike")): _PathLike = os.PathLike
else:
    class _PathLike(object): pass
#

class Object(FileLikeWrapperMixin, _PathLike, Abstract):
    """
Provides the VFS implementation for 'file' objects.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    _FILE_WRAPPED_METHODS = ( "flush",
                              "is_eof",
                              "read",
                              "seek",
                              "tell",
                              "truncate",
                              "write"
                            )
    """
File IO methods implemented by an wrapped resource.
    """

    __slots__ = [ "dir_path_name", "file_path_name", "object_readonly" ] + FileLikeWrapperMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(Object)

:since: v1.0.0
        """

        Abstract.__init__(self)
        FileLikeWrapperMixin.__init__(self)

        self.dir_path_name = None
        """
Directory path and name set for "TYPE_DIRECTORY"
        """
        self.file_path_name = None
        """
File path and name set for "TYPE_FILE"
        """
        self.object_readonly = None
        """
True to open the object and nested ones read-only
        """

        self.supported_features['filesystem_path_name'] = True
        self.supported_features['flush'] = self._supports_flush
        self.supported_features['implementing_instance'] = self._supports_implementing_instance
        self.supported_features['seek'] = self._supports_seek
        self.supported_features['time_created'] = True
        self.supported_features['time_updated'] = True
    #

    def __fspath__(self):
        """
python.org: Return the file system path representation of the object.

:return: (str) File system path representation
:since:  v1.0.0
        """

        return self.filesystem_path_name
    #

    @property
    def filesystem_path_name(self):
        """
Returns the path and name for the VFS object in the system filesystem.

:return: (str) System filesystem path and name of the VFS object
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = self.dir_path_name
        elif (self.file_path_name is not None): _return = self.file_path_name
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def implementing_instance(self):
        """
Returns the implementing instance.

:return: (mixed) Implementing instance
:since:  v1.0.0
        """

        _return = None

        if (self._wrapped_resource is None
            and self.file_path_name is not None
            ): self._open_wrapped_resource()

        if (self._wrapped_resource is not None): _return = self._wrapped_resource
        elif (self.dir_path_name is None): raise IOException("VFS object not opened")

        return _return
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
    def is_valid(self):
        """
Returns true if the object is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        _return = False

        if (self._wrapped_resource is not None): _return = self._wrapped_resource.is_valid
        elif (self.dir_path_name is not None): _return = os.access(self.dir_path_name, os.X_OK)
        elif (self.file_path_name is not None): _return = os.access(self.file_path_name, os.R_OK)

        return _return
    #

    @property
    def mimetype(self):
        """
Returns the mime type of this VFS object.

:return: (str) VFS object mime type
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = "text/directory"
        elif (self.file_path_name is not None):
            file_data = path.splitext(self.file_path_name)
            mimetype_definition = MimeType.get_instance().get(file_data[1][1:])

            _return = ("application/octet-stream" if (mimetype_definition is None) else mimetype_definition['type'])
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def name(self):
        """
Returns the name of this VFS object.

:return: (str) VFS object name
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = path.basename(self.dir_path_name)
        elif (self.file_path_name is not None): _return = path.basename(self.file_path_name)
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = 0
        elif (self.file_path_name is not None): _return = os.stat(self.file_path_name).st_size
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def time_created(self):
        """
Returns the UNIX timestamp this object was created.

:return: (int) UNIX timestamp this object was created
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = os.stat(self.dir_path_name).st_ctime
        elif (self.file_path_name is not None): _return = os.stat(self.file_path_name).st_ctime
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def time_updated(self):
        """
Returns the UNIX timestamp this object was updated.

:return: (int) UNIX timestamp this object was updated
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = os.stat(self.dir_path_name).st_mtime
        elif (self.file_path_name is not None): _return = os.stat(self.file_path_name).st_mtime
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def type(self):
        """
Returns the type of this object.

:return: (int) Object type
:since:  v1.0.0
        """

        _return = None

        if (self.dir_path_name is not None): _return = Object.TYPE_DIRECTORY
        elif (self.file_path_name is not None): _return = Object.TYPE_FILE
        else: raise IOException("VFS object not opened")

        return _return
    #

    @property
    def url(self):
        """
Returns the URL of this VFS object.

:return: (str) VFS URL
:since:  v1.0.0
        """

        object_id = None

        if (self.dir_path_name is not None): object_id = quote_plus(self.dir_path_name, "/")
        elif (self.file_path_name is not None): object_id = quote_plus(self.file_path_name, "/")

        if (object_id is None): raise IOException("VFS object not opened")

        return "file:///{0}".format(object_id)
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        if (self.dir_path_name is not None): self.dir_path_name = None
        else:
            try: FileLikeWrapperMixin.close(self)
            finally: self.file_path_name = None
        #
    #

    def _ensure_directory_readable(self, vfs_url, dir_path_name):
        """
Ensures that the given directory path readable.

:param vfs_url: VFS URL
:param dir_path_name: Directory path and name

:since: v1.0.0
        """

        if (not os.access(dir_path_name, os.X_OK)): raise IOException("VFS URL '{0}' is invalid".format(vfs_url))
    #

    def _ensure_directory_writable(self, vfs_url, dir_path_name):
        """
Ensures that the given directory path writable.

:param vfs_url: VFS URL
:param dir_path_name: Directory path and name

:since: v1.0.0
        """

        if (not os.access(dir_path_name, os.X_OK)): raise IOException("VFS URL '{0}' is invalid".format(vfs_url))
    #

    def new(self, _type, vfs_url):
        """
Creates a new VFS object.

:param _type: VFS object type
:param vfs_url: VFS URL

:since: v1.0.0
        """

        if (_type == Object.TYPE_DIRECTORY): self._new_directory(vfs_url)
        elif (_type == Object.TYPE_FILE): self._new_file(vfs_url)
        else: raise OperationNotSupportedException()
    #

    def _new_file(self, vfs_url):
        """
Creates a new VFS file object.

:param vfs_url: VFS URL

:since: v1.0.0
        """

        file_path_name = unquote_plus(Abstract._get_id_from_vfs_url(vfs_url))
        self._ensure_directory_writable(vfs_url, path.dirname(file_path_name))

        self._open_file(vfs_url, file_path_name)
    #

    def open(self, vfs_url, readonly = False):
        """
Opens a VFS object. The handle is set at the beginning of the object.

:param vfs_url: VFS URL
:param readonly: Open object in readonly mode

:since: v1.0.0
        """

        if (self.dir_path_name is not None
            or self.file_path_name is not None
           ): raise IOException("Can't create new VFS object on already opened instance")

        object_path_name = unquote_plus(Abstract._get_id_from_vfs_url(vfs_url))

        if (path.isdir(object_path_name)): self._open_directory(vfs_url, object_path_name, readonly)
        else: self._open_file(vfs_url, object_path_name, readonly)
    #

    def _open_directory(self, vfs_url, dir_path_name, readonly = False):
        """
Opens a VFS directory object.

:param vfs_url: VFS URL
:param dir_path_name: Directory path and name

:since: v1.0.0
        """

        self._ensure_directory_readable(vfs_url, dir_path_name)

        self.dir_path_name = path.abspath(dir_path_name)
        self.object_readonly = readonly
    #

    def _open_file(self, vfs_url, file_path_name, readonly = True):
        """
Opens (and creates) a VFS file object.

:param vfs_url: VFS URL
:param file_path_name: File path and name
:param readonly: Open file in readonly mode

:since: v1.0.0
        """

        self.file_path_name = path.abspath(file_path_name)
        self.object_readonly = readonly
    #

    def _open_wrapped_resource(self):
        """
Opens the wrapped resource once needed for an file IO request.

:since: v1.0.0
        """

        if (self.file_path_name is None): raise IOException("VFS object not opened")

        file_mode = ("rb" if (self.object_readonly) else "r+b")

        _file = File()
        if (_file.open(self.file_path_name, self.object_readonly, file_mode)): self._set_wrapped_resource(_file)
    #

    def scan(self):
        """
Scan over objects of a collection like a directory.

:return: (list) Child VFS objects
:since:  v1.0.0
        """

        if (self.file_path_name is not None): raise OperationNotSupportedException("VFS object can not be scanned")
        if (self.dir_path_name is None): raise IOException("VFS object not opened")

        _return = [ ]

        entry_list = os.listdir(self.dir_path_name)
        entry_list.sort()

        dir_path_url = self.url

        for entry in entry_list:
            if (entry[0] != "."):
                vfs_child_object = Object()

                try:
                    vfs_child_object.open("{0}/{1}".format(dir_path_url, entry), self.object_readonly)
                    _return.append(vfs_child_object)
                except IOException as handled_exception: LogLine.error(handled_exception, context = "dpt_vfs")
            #
        #

        return _return
    #

    def _supports_flush(self):
        """
Returns false if flushing buffers is not supported.

:return: (bool) True if flushing buffers is supported
:since:  v1.0.0
        """

        return (self.file_path_name is not None and (not self.object_readonly))
    #

    def _supports_implementing_instance(self):
        """
Returns false if no underlying, implementing instance can be returned.

:return: (bool) True if an implementing instance can be returned.
:since:  v1.0.0
        """

        return (self._wrapped_resource is not None)
    #

    def _supports_seek(self):
        """
Returns false if seek is not supported.

:return: (bool) True if seek is supported
:since:  v1.0.0
        """

        return (self.file_path_name is not None)
    #
#
