#! /usr/bin/env python3

"""
Copyright (c) 2020 Deutsches Elektronen-Synchrotron DESY

See LICENSE.txt for license details.
"""

import enum
import sys
import unittest

from systemrdl.rdltypes import AccessType

from hectare._hectare_types import Field, Register
from hectare._HectareCHeaderGen import HectareCHeaderGen


class TestHectareCHeaderGen(unittest.TestCase):
    def test_gen_single_addr(self):
        reg = Register("myreg", 8)
        s = HectareCHeaderGen._gen_single_addr("MY_COMP", reg)
        self.assertEqual(s, "#define MY_COMP_ADDR_MYREG (8)")
    
if __name__ == "__main__":
    unittest.main()
