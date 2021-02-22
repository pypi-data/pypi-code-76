# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;threading

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v2.0.0
dpt_threading/event.py
"""

from threading import Event as _Event

from dpt_settings import Settings

class Event(object):
    """
python.org: An event manages a flag that can be set to true with the set()
method and reset to false with the clear() method.

This implementation falls back to a default timeout value if "wait()" is
called without specifing one.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: threading
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "_event", "timeout" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, *args, **kwargs):
        """
Constructor __init__(ResultEvent)

:since: v1.0.0
        """

        self._event = _Event(*args, **kwargs)
        """
Encapsulated event implementation
        """
        self.timeout = Settings.get("global_event_timeout", 10)
        """
Event waiting timeout in seconds
        """
    #

    @property
    def is_set(self):
        """
Returns true if the internal flag is true.

:return: (bool) True if set
:since:  v1.0.0
        """

        return self._event.is_set()
    #

    def clear(self):
        """
python.org: Reset the internal flag to false.

:since: v1.0.0
        """

        self._event.clear()
    #

    def set(self):
        """
python.org: Set the internal flag to true.

:since: v1.0.0
        """

        self._event.set()
    #

    def wait(self, timeout = None):
        """
python.org: Block until the internal flag is true.

:param timeout: Timeout value in seconds. If zero or below the call blocks
                indefinitely.

:return: (bool) This method returns true if and only if the internal flag
         has been set to true, either before the wait call or after the wait
         starts, so it will always return True except if a timeout is given
         and the operation times out
:since:  v1.0.0
        """

        if (timeout is None): timeout = self.timeout
        elif (timeout <= 0): timeout = None

        return self._event.wait(timeout)
    #
#
