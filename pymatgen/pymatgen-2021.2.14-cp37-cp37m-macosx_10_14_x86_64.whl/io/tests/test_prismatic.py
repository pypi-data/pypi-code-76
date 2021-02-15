# coding: utf-8
# Copyright (c) Pymatgen Development Team.
# Distributed under the terms of the MIT License.


import os
import unittest

from pymatgen.core.structure import Structure
from pymatgen.io.prismatic import Prismatic
from pymatgen.util.testing import PymatgenTest


class PrismaticTest(unittest.TestCase):
    def test_to_string(self):

        structure = Structure.from_file(os.path.join(PymatgenTest.TEST_FILES_DIR, "CuCl.cif"))
        prismatic = Prismatic(structure)
        prismatic_str = prismatic.to_string()
        self.assertTrue(
            prismatic_str.startswith(
                """Generated by pymatgen
6.52372159 6.52372159 6.52372159
29"""
            )
        )
        self.assertTrue(prismatic_str.endswith("-1"))
