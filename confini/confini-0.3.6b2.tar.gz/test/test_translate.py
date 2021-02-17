#!/usr/bin/python

import os
import unittest
import logging

from confini import Config

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestTranslate(unittest.TestCase):

    wd = os.path.dirname(__file__)

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_parse_default(self):
        inidir = os.path.join(self.wd, 'files/translate')
        c = Config(inidir)
        c.process()

        self.assertTrue(c.get('TRUE_A'))
        self.assertTrue(c.get('TRUE_B'))
        self.assertTrue(c.get('TRUE_C'))

        self.assertFalse(c.true('FALSE_A'))
        self.assertFalse(c.true('FALSE_B'))
        self.assertFalse(c.true('FALSE_C'))
        self.assertIsNone(c.get('FALSE_D'))

        o = {
            'TRUE_A': True,
            'FALSE_A': False,
                }
        c.dict_override(o, 'test')
        self.assertTrue(c.true('TRUE_A'))
        self.assertFalse(c.true('FALSE_A'))

     
if __name__ == '__main__':
    unittest.main()
