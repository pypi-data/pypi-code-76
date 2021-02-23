#!/usr/data/env python3
# -*- coding: utf-8 -*-

import unittest
import hydrogen.HydroGen as hy
import hydrogen.tools.tools as tt
from hydrogen.EventClass import event

class TestEventClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Code before all tests
        pass

    @classmethod
    def tearDownClass(cls):
        #Code after all tests
        pass

    def setUp(self):
        #Code before any single test
        pass

    def tearDown(self):
        #Code after any single test
        pass

    # def test_someMethod(self):
    #     self.assertIsNotNone(someFunction(*args))
    #
    #     with self.assertRaises(ValueError):
    #         tt.function()


if __name__=="__main__":
    unittest.main()
