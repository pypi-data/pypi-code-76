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
dpt_threading/instance_lock.py
"""

from dpt_settings import Settings

from .thread_lock import ThreadLock

class InstanceLock(ThreadLock):
    """
"InstanceLock" is used to protect manipulation of a singleton.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: threading
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, timeout = None):
        """
Constructor __init__(InstanceLock)

:since: v1.0.0
        """

        ThreadLock.__init__(self)

        self._timeout = (Settings.get("pas_global_singleton_lock_timeout", 3) if (timeout is None) else timeout)
    #
#
