from unittest import TestCase
import tempfile
import os
import pandas as pd

from pysmm.GEE_wrappers import GEE_pt

class TestGEEWrappers(TestCase):
    def test_LC(self):
        testlon = 12.31
        testlat = 48.89
        tempdir = tempfile.mkdtemp()
        test_inst = GEE_pt(testlon, testlat, tempdir)
        test_inst.extr_LC()
        self.assertTrue(isinstance(test_inst.LC, float))
        os.rmdir(tempdir)

    def test_MOD13Q1(self):
        testlon = 12.31
        testlat = 48.89
        tempdir = tempfile.mkdtemp()
        test_inst = GEE_pt(testlon, testlat, tempdir)
        test_ser = test_inst.extr_MODIS_MOD13Q1()
        self.assertTrue(isinstance(test_ser, pd.Series))

    # TODO complete tests for all methods in GEE_wrappers