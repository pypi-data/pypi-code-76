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
dpt_runtime/stacked_dict.py
"""

try: from collections.abc import MutableMapping
except ImportError: from collections import MutableMapping

from .input_filter import InputFilter

class StackedDict(MutableMapping):
    """
A stacked dictionary consists of a regular Python dict and stacked
additional ones used for key lookups.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.1
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ "_dict", "stacked_dicts" ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, *args, **kwargs):
        """
Constructor __init__(StackedDict)

:since: v1.0.1
        """

        MutableMapping.__init__(self)

        self._dict = dict(*args, **kwargs)
        """
Base of the stacked dict instance.
        """
        self.stacked_dicts = [ ]
        """
Stacked additional dicts to be looked in.
        """
    #

    def __contains__(self, item):
        """
python.org: Called to implement membership test operators.

:param item: Item to be looked up

:return: (bool) True if item is in self or a stacked dict.
:since:  v1.0.1
        """

        _return = (item in self._dict.keys())

        if (not _return):
            for _dict in self.stacked_dicts:
                if (item in _dict):
                    _return = True
                    break
                #
            #
        #

        return _return
    #

    def __delitem__(self, key):
        """
python.org: Called to implement deletion of self[key].

:param key: Key

:since: v1.0.1
        """

        del(self._dict[key])
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v1.0.1
        """

        for key in self._get_unique_keys(): yield key
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param key: Key

:return: (mixed) Value
:since:  v1.0.1
        """

        _return = None

        is_found = False

        if (key in self._dict.keys()):
            _return = self._dict[key]
            is_found = True
        #

        if (not is_found):
            for _dict in self.stacked_dicts:
                if (key in _dict):
                    is_found = True
                    _return = _dict[key]

                    break
                #
            #
        #

        if (not is_found): raise KeyError(key)
        return _return
    #

    def __len__(self):
        """
python.org: Called to implement the built-in function len().

:return: (int) Number of dict items
:since:  v1.0.1
        """

        return len(self._get_unique_keys())
    #

    def __setitem__(self, key, value):
        """
python.org: Called to implement assignment to self[key].

:param key: Key
:param value: Value

:since: v1.0.1
        """

        self._dict[key] = value
    #

    def add_dict(self, _dict, prepend = False):
        """
Adds the given Python dictionary to the stack.

:param _dict: Dictionary
:param prepend: Prepend dictionary

:since: v1.0.1
        """

        if (_dict is not self._dict and _dict not in self.stacked_dicts):
            if (prepend): self.stacked_dicts.insert(0, _dict)
            else: self.stacked_dicts.append(_dict)
        #
    #

    def get(self, key, default = None):
        """
python.org: Return the value for key if key is in the dictionary, else
default.

:param key: Key
:param default: Default return value

:return: (mixed) Value
:since:  v1.0.1
        """

        _return = default

        try: _return = self[key]
        except KeyError: pass

        return _return
    #

    def _get_unique_keys(self):
        """
Returns a list of unique keys for this stacked dictionary.

:return: (list) Keys
:since:  v1.0.4
        """

        keys = list(self._dict.keys())
        for _dict in self.stacked_dicts: keys += list(_dict.keys())

        return InputFilter.filter_unique_list(keys)
    #

    def remove_dict(self, _dict):
        """
Removes the given Python dictionary from the stack.

:param _dict: Dictionary

:since: v1.0.1
        """

        if (_dict in self.stacked_dicts): self.stacked_dicts.remove(_dict)
    #
#
