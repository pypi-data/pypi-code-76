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
unittest
"""

import unittest

from dpt_runtime import StackedDict

class TestStackedDict(unittest.TestCase):
    """
UnitTest for StackedDict

:since: v1.0.4
    """

    def test_nested_dicts(self):
        test = StackedDict({ "test": "value" })
        test.add_dict({ "test": "value2", "nested": "value2" })
        test.add_dict({ "nested": "value" })

        self.assertEqual(2, len(test.keys()))
        self.assertEqual("value", test['test'])
        self.assertEqual("value2", test['nested'])
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
