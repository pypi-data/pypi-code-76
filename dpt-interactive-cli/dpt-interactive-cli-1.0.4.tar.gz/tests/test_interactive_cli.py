# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;interactive_cli

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
unittest
"""

import unittest

from dpt_interactive_cli import InteractiveCli

class TestInteractiveCli(unittest.TestCase):
    """
Unittest for InteractiveCli

:since: v1.0.0
    """

    def test_html_output(self):
        """
Tests HTML special characters.
        """

        interactive_cli = InteractiveCli()
        interactive_cli.output_info("<this> is HTML")
        interactive_cli.output_error("<this> is HTML as well")
        interactive_cli.output_info("<{0}> is still HTML", "this")
        interactive_cli.output_error("<{0}> is still HTML as well", "this")
    #
#

if (__name__ == "__main__"):
    unittest.main()
#
