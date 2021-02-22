# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v2.0.0
dpt_runtime/io/file_like_copy_mixin.py
"""

from time import time

from dpt_settings import Settings

from ..exceptions import IOException

class FileLikeCopyMixin(object):
    """
The "FileLikeCopyMixin" instance provides a method to copy the file data to
a given target. "is_eof()", "read()" and "seek()" methods must be
implemented for the source.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=assigning-non-slot

    _mixin_slots_ = [ "file_like_copy_io_chunk_size" ]
    """
Additional __slots__ used for inherited classes.
    """
    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self):
        """
Constructor __init__(FileLikeCopyMixin)

:since: v2.0.0
        """

        self.file_like_copy_io_chunk_size = int(Settings.get("global_io_chunk_size_local", 524288))
        """
IO chunk size for copying
        """
    #

    def copy_data(self, target, timeout = None):
        """
Copy data to the target.

:param target: Any object providing a "write()" method
:param timeout: Timeout for copying data

:since: v2.0.0
        """

        timeout_time = (0 if (timeout is None) else time() + timeout)
        self.seek(0)

        while ((not self.is_eof)
               and (timeout_time < 1 or time() < timeout_time)
              ): target.write(self.read(self.file_like_copy_io_chunk_size))

        if (not self.is_eof): raise IOException("Timeout occurred before EOF")
    #
#
