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
dpt_runtime/io/socket_reader.py
"""

from time import time

from dpt_settings import Settings

from .descriptor_selector import DescriptorSelector
from ..exceptions import IOException

class SocketReader(object):
    """
"SocketReader" provides a "recv()" method implementing time limited read
operations from blocking and non-blocking sockets.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "__weakref__", "socket", "_timeout" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, socket, timeout = None):
        """
Constructor __init__(SocketReader)

:since: v2.0.0
        """

        self.socket = socket
        """
Underlying lock instance
        """
        self._timeout = timeout
        """
Lock timeout in seconds
        """

        if (self._timeout is None or self._timeout <= 0):
            self._timeout = int(Settings.get("global_socket_data_timeout", 30))
        #
    #

    @property
    def timeout(self):
        """
Returns the lock timeout in seconds.

:return: (float) Timeout value
:since:  v2.0.0
        """

        return self._timeout
    #

    @timeout.setter
    def timeout(self, timeout):
        """
Sets a new lock timeout.

:param timeout: New timeout value in seconds

:since: v2.0.0
        """

        self._timeout = timeout
    #

    def recv(self, size):
        """
Read data from socket.

:param size: Size to receive

:return: (bytes) Socket data received; Socket reached EOF (closed) if
         len(returned) < size
:since:  v2.0.0
        """

        _return = None

        data_size = 0
        is_socket_valid = True
        selector = DescriptorSelector([ self.socket.fileno() ])
        timeout_time = time() + self.timeout

        while (is_socket_valid and data_size < size and time() < timeout_time):
            if (len(selector.select(self.timeout, False)[0]) < 1): raise IOException("Failed to receive data")

            data = self.socket.recv(size - data_size)
            data_size_received = len(data)

            if (_return is None): _return = data
            elif (data_size_received > 0): _return += data

            data_size += data_size_received
            if (data_size_received == 0): is_socket_valid = False
        #

        return _return
    #
#
