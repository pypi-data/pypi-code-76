#!/usr/data/env python3
# -*- coding: utf-8 -*-

import unittest
import hydrogen.HydroGen as hy
import hydrogen.tools.tools as tt
from hydrogen.EventClass import event
import pandas as pd
import numpy as np

class TestTools(unittest.TestCase):

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
        self.d = tt.initRead('./testInit.in')
        #self.df, self.df_seconds, self.df_freq = hy.readConvert_Distribution(self.d.distroFile, self.d.totSimTime, False)
        pass

    def tearDown(self):
        #Code after any single test
        pass

    def test_initRead(self):
        d = tt.initRead('./testInit.in')
        self.assertIsInstance(d, object)
        self.assertIsNotNone(d) #test if callable

    def test_Flow2Freq(self):
        df_seconds = hy.readConvert_Distribution(self.d.distroFile, self.d.totSimTime, False)[1]
        df_freq = tt.Flow2Freq(df_seconds)
        self.assertIsInstance(df_freq, pd.DataFrame) #check if returns DataFrame
        for column in df_freq:
            self.assertEqual(round(df_freq[column].sum(), 3),1) #sum of columns must be equal to one as frequencies

    def test_convert2Seconds(self):
        df = hy.readConvert_Distribution(self.d.distroFile, self.d.totSimTime, False)[0]
        df_seconds = tt.convert2Seconds(df, self.d.totSimTime)
        self.assertIsInstance(df_seconds, pd.DataFrame) #check if returns DataFrame
        self.assertEqual(df_seconds.index[-1], len(df_seconds)-1) #each row should represent one single second

        with self.assertRaises(Exception): #check if exception is raised if reversing dataframe (non-monotonic increasing df)
            df_seconds = tt.convert2Seconds(df.iloc[::-1], self.d.totSimTime)

    # def test_cfdRandomPick(self):
        # self.assertIsNotNone(someFunction(*args))
        #
        # with self.assertRaises(ValueError):
        #     tt.function()



if __name__=="__main__":
    unittest.main()
