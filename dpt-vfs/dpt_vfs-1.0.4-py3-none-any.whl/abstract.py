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
dpt_vfs/abstract.py
"""

# pylint: disable=unused-argument

from dpt_runtime import SupportsMixin
from dpt_runtime.exceptions import IOException, NotImplementedException, OperationNotSupportedException, ValueException
from dpt_runtime.io import FileLikeCopyMixin

class Abstract(FileLikeCopyMixin, SupportsMixin):
    """
Provides the abstract VFS implementation for an object.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: vfs
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    TYPE_DIRECTORY = 1 << 1
    """
Directory (or collection like) type
    """
    TYPE_FILE = 1
    """
File type
    """
    TYPE_LINK = 1 << 2
    """
Link type
    """

    # pylint: disable=invalid-name

    __slots__ = [ "__weakref__" ] + FileLikeCopyMixin._mixin_slots_ + SupportsMixin._mixin_slots_
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(Abstract)

:since: v1.0.0
        """

        FileLikeCopyMixin.__init__(self)
        SupportsMixin.__init__(self)
    #

    def __del__(self):
        """
Destructor __del__(Abstract)

:since: v1.0.0
        """

        self.close()
    #

    @property
    def implementing_instance(self):
        """
Returns the implementing instance.

:return: (mixed) Implementing instance or "None"
:since:  v1.0.0
        """

        # pylint: disable=bad-option-value,useless-return

        if (not self.is_valid): raise IOException("VFS object not opened")
        return None
    #

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
    def is_directory(self):
        """
Returns true if the object is representing a directory (or collection).

:return: (bool) True if directory
:since:  v1.0.0
        """

        return bool(self.type & Abstract.TYPE_DIRECTORY)
    #

    @property
    def is_eof(self):
        """
Checks if the pointer is at EOF.

:return: (bool) True on success
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    @property
    def is_file(self):
        """
Returns true if the object is representing a file.

:return: (bool) True if file
:since:  v1.0.0
        """

        return bool(self.type & Abstract.TYPE_FILE)
    #

    @property
    def is_link(self):
        """
Returns true if the object is representing a link to another object.

:return: (bool) True if link
:since:  v1.0.0
        """

        return bool(self.type & Abstract.TYPE_LINK)
    #

    @property
    def is_valid(self):
        """
Returns true if the object is available.

:return: (bool) True on success
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def mimetype(self):
        """
Returns the mime type of this VFS object.

:return: (str) VFS object mime type
:since:  v1.0.0
        """

        if (not self.is_valid): raise IOException("VFS object not opened")
        return ("text/directory" if (self.is_directory) else "application/octet-stream")
    #

    @property
    def name(self):
        """
Returns the name of this VFS object.

:return: (str) VFS object name
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    @property
    def size(self):
        """
Returns the size in bytes.

:return: (int) Size in bytes
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def time_created(self):
        """
Returns the UNIX timestamp this object was created.

:return: (int) UNIX timestamp this object was created
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    @property
    def time_updated(self):
        """
Returns the UNIX timestamp this object was updated.

:return: (int) UNIX timestamp this object was updated
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    @property
    def type(self):
        """
Returns the type of this object.

:return: (int) Object type
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    @property
    def url(self):
        """
Returns the URL of this VFS object.

:return: (str) VFS URL
:since:  v1.0.0
        """

        raise NotImplementedException()
    #

    def close(self):
        """
python.org: Flush and close this stream.

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def flush(self):
        """
python.org: Flush the write buffers of the stream if applicable.

:since: v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def new(self, _type, vfs_url):
        """
Creates a new VFS object.

:param _type: VFS object type
:param vfs_url: VFS URL

:since: v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def open(self, vfs_url, readonly = False):
        """
Opens a VFS object. The handle is set at the beginning of the object.

:param vfs_url: VFS URL
:param readonly: Open object in readonly mode

:since: v1.0.0
        """

        raise NotImplementedException()
    #

    def read(self, n = 0, timeout = -1):
        """
python.org: Read up to n bytes from the object and return them.

:param n: How many bytes to read from the current position (0 means until
          EOF)
:param timeout: Timeout to use (if supported by implementation)

:return: (bytes) Data; None if EOF
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def scan(self):
        """
Scan over objects of a collection like a directory.

:return: (list) Child VFS objects
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def seek(self, offset):
        """
python.org: Change the stream position to the given byte offset.

:param offset: Seek to the given offset

:return: (int) Return the new absolute position.
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def tell(self):
        """
python.org: Return the current stream position as an opaque number.

:return: (int) Stream position
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def truncate(self, new_size):
        """
python.org: Resize the stream to the given size in bytes.

:param new_size: Cut file at the given byte position

:return: (int) New file size
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    def write(self, b, timeout = -1):
        """
python.org: Write the given bytes or bytearray object, b, to the underlying
raw stream and return the number of bytes written.

:param b: (Over)write file with the given data at the current position
:param timeout: Timeout to use (defaults to construction time value)

:return: (int) Number of bytes written
:since:  v1.0.0
        """

        raise OperationNotSupportedException()
    #

    @staticmethod
    def _get_id_from_vfs_url(vfs_url):
        """
Returns the ID part of the VFS URL given.

:return: (str) VFS URL ID
:since:  v1.0.0
        """

        if (type(vfs_url) is not str): raise ValueException("VFS URL given is invalid")

        vfs_url_data = vfs_url.split("://", 1)
        if (len(vfs_url_data) == 1): raise ValueException("VFS URL '{0}' is invalid".format(vfs_url))

        _return = vfs_url_data[1]

        if (_return in ( "", "/" )): _return = ""
        else: _return = (_return[1:] if (_return[:1] == "/") else _return).strip()

        return _return
    #

    @staticmethod
    def _get_scheme_from_vfs_url(vfs_url):
        """
Returns the scheme of the VFS URL given.

:return: (str) VFS URL scheme
:since:  v1.0.0
        """

        if (type(vfs_url) is not str): raise ValueException("VFS URL given is invalid")

        vfs_url_data = vfs_url.split("://", 1)
        if (len(vfs_url_data) == 1): raise ValueException("VFS URL '{0}' is invalid".format(vfs_url))

        return vfs_url_data[0].lower()
    #
#
