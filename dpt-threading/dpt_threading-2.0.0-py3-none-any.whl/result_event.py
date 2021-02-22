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
dpt_threading/result_event.py
"""

from dpt_runtime.exceptions import IOException

from .event import Event

class ResultEvent(Event):
    """
"ResultEvent" implements a result delivering event.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: threading
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "_result", "result_set" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout = None):
        """
Constructor __init__(ResultEvent)

:param timeout: Default timeout in seconds to wait for results

:since: v1.0.0
        """

        Event.__init__(self)

        self._result = None
        """
Result set
        """
        self.result_set = False
        """
Flag indicating that a result was set.
        """

        if (timeout is not None): self.timeout = timeout
    #

    @property
    def is_result_set(self):
        """
Returns true after a result has been set.

:return: (bool) True if a result is set
:since:  v1.0.0
        """

        return self.result_set
    #

    @property
    def result(self):
        """
Returns the result being set previously.

:return: (mixed) Result set
:since:  v1.0.0
        """

        if (not self.result_set): raise IOException("No result has been set for this ResultEvent.")
        return self._result
    #

    def clear(self):
        """
python.org: Reset the internal flag to false.

:since: v1.0.0
        """

        if (self.result_set): raise IOException("A ResultEvent can not be cleared after a result was set.")
        Event.clear(self)
    #

    def set(self):
        """
python.org: Set the internal flag to true.

:since: v1.0.0
        """

        self.set_result(None)
    #

    def set_result(self, result):
        """
Sets a result for this event and notifies all waiting threads afterwards.

:param result: Result

:since: v1.0.0
        """

        self._result = result
        self.result_set = True

        Event.set(self)
    #
#
