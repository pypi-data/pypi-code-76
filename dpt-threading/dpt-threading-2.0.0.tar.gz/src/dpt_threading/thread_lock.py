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
dpt_threading/thread_lock.py
"""

from threading import Event, RLock
from time import time

from dpt_runtime.exceptions import IOException
from dpt_settings import Settings

class ThreadLock(object):
    """
"ThreadLock" implements a timeout aware ContextManager capable thread lock.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: threading
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "event", "lock", "_timeout" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout = None):
        """
Constructor __init__(ThreadLock)

:since: v1.0.0
        """

        self.event = None
        """
Underlying event instance
        """
        self.lock = RLock()
        """
Underlying lock instance
        """
        self._timeout = (Settings.get("global_thread_lock_timeout", 10) if (timeout is None) else timeout)
        """
Lock timeout in seconds
        """
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: v1.0.0
        """

        self.acquire()
    #

    def __exit__(self, exc_type, exc_value, traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v1.0.0
        """

        self.release()
        return False
    #

    @property
    def timeout(self):
        """
Returns the lock timeout in seconds.

:return: (float) Timeout value
:since:  v1.0.0
        """

        return self._timeout
    #

    @timeout.setter
    def timeout(self, timeout):
        """
Sets a new lock timeout.

:param timeout: New timeout value in seconds

:since: v1.0.0
        """

        self._timeout = timeout
    #

    def acquire(self):
        """
Acquire a lock.

:since: v1.0.0
        """

        # pylint: disable=unexpected-keyword-arg

        try:
            if (not self.lock.acquire(timeout = self.timeout)): raise IOException("Timeout occurred while acquiring lock")
        except TypeError:
            if (self.event is None):
                self.event = Event()
                self.event.set()
            #

            if (self.lock.acquire(False)): self.event.clear()
            else:
                timeout = self.timeout

                while (timeout > 0):
                    _time = time()
                    self.event.wait(timeout)

                    if (self.lock.acquire(False)):
                        self.event.clear()
                        break
                    else: timeout -= (time() - _time)
                #

                if (timeout <= 0): raise IOException("Timeout occurred while acquiring lock")
            #
        #
    #

    def release(self):
        """
Release a lock.

:since: v1.0.0
        """

        self.lock.release()
        if (self.event is not None): self.event.set()
    #
#
