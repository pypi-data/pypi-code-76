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
dpt_runtime/io/descriptor_selector.py
"""

import select

class DescriptorSelector(object):
    """
python.org: The poll() system call, supported on most Unix systems, provides
better scalability for network servers that service many, many clients at
the same time.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v2.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    LOST_BITS = select.POLLERR | select.POLLHUP | select.POLLNVAL
    """
Additional poll signals to be handled.
    """

    __slots__ = [ "_poller", "_selectors", "_selectors_polled" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, rlist = None, wlist = None, xlist = None):
        """
Constructor __init__(DescriptorSelector)

:param rlist: List of selectors to be read from
:param wlist: List of selectors to write to
:param xlist: List of selectors to listen for exceptional conditions

:since: v2.0.0
        """

        if (rlist is None): rlist = [ ]
        if (wlist is None): wlist = [ ]
        if (xlist is None): xlist = [ ]

        self._poller = (select.poll() if (hasattr(select, "poll")) else None)
        """
Poll object if supported
        """
        self._selectors = ( rlist, wlist, xlist )
        """
List of descriptors
        """
        self._selectors_polled = ( 0, 0, 0 )
        """
Number of descriptors polled
        """
    #

    def __del__(self):
        """
Destructor __del__(DescriptorSelector)

:since: v2.0.0
        """

        self._unregister_from_polling()
    #

    def select(self, timeout = -1, unregister = True, is_readable = True, is_writable = True):
        """
Selects descriptors matching expected events.

:return: (tuple) Tuple of descriptors matching expected events
:since:  v2.0.0
        """

        rlist = (self._selectors[0] if (is_readable) else [ ])
        wlist = (self._selectors[1] if (is_writable) else [ ])
        xlist = self._selectors[2]

        if (self._poller is None): _return = select.select(rlist, wlist, xlist, timeout)
        else:
            self._register_for_polling(rlist, wlist, xlist)

            waiting_list = (self._poller.poll() if (timeout < 0) else self._poller.poll(timeout * 1000))
            _return = ( [ ], [ ], [ ] )

            for descriptor_data in waiting_list:
                if (descriptor_data[1] & select.POLLIN): _return[0].append(descriptor_data[0])
                if (descriptor_data[1] & select.POLLOUT): _return[1].append(descriptor_data[0])
                if (descriptor_data[1] & select.POLLPRI): _return[2].append(descriptor_data[0])
            #

            if (unregister): self._unregister_from_polling()
        #

        return _return
    #

    def _register_for_polling(self, rlist, wlist, xlist):
        """
Destructor __del__(Abstract)

:since: v2.0.0
        """

        if (self._selectors_polled[0] != len(rlist)):
            if (self._selectors_polled[0] > 0): self._unregister_from_polling(rlist)
            for descriptor in rlist: self._poller.register(descriptor, select.POLLIN | DescriptorSelector.LOST_BITS)
        #

        if (self._selectors_polled[1] != len(wlist)):
            if (self._selectors_polled[1] > 0): self._unregister_from_polling(wlist)
            for descriptor in wlist: self._poller.register(descriptor, select.POLLOUT | DescriptorSelector.LOST_BITS)
        #

        if (self._selectors_polled[2] != len(xlist)):
            if (self._selectors_polled[2] > 0): self._unregister_from_polling(xlist)
            for descriptor in xlist: self._poller.register(descriptor, select.POLLPRI | DescriptorSelector.LOST_BITS)
        #
    #

    def _unregister_from_polling(self, dlist = None):
        """
Destructor __del__(Abstract)

:since: v2.0.0
        """

        if (dlist is None):
            if (self._selectors_polled[0] > 0): self._unregister_from_polling(self._selectors[0])
            if (self._selectors_polled[1] > 0): self._unregister_from_polling(self._selectors[1])
            if (self._selectors_polled[2] > 0): self._unregister_from_polling(self._selectors[2])
        else:
            for descriptor in dlist: self._poller.unregister(descriptor)
        #
    #
#
