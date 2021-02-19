#!/usr/bin/python

import os
import unittest
import logging

from confini import Config

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

class TestEnv(unittest.TestCase):

    wd = os.path.dirname(__file__)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dict_override(self):
        inidir = os.path.join(self.wd, 'files')
        c = Config(inidir)
        c.process()

        override_dict = {
                'FOO_BAR': '666',
                'XYZZY_BERT': 'oscar',
                'BAR_FOO': None,
                }
        c.dict_override(override_dict, 'arbitrary dict')

        expect = {
            'FOO_BAR': '666',
            'FOO_BAZ': '029a',
            'BAR_FOO': 'oof',
            'XYZZY_BERT': 'oscar',
                }
        self.assertDictEqual(expect, c.store)

        override_dict = {
                'BAR_FOO': 'barbarbar',
                }
        c.dict_override(override_dict, 'arbitrary dict')

        expect = {
            'FOO_BAR': '666',
            'FOO_BAZ': '029a',
            'BAR_FOO': 'barbarbar',
            'XYZZY_BERT': 'oscar',
                }
        self.assertDictEqual(expect, c.store)



    def test_env_a_override(self):
        os.environ['FOO_BAR'] = '43'
        inidir = os.path.join(self.wd, 'files')
        c = Config(inidir)
        c.process()

        os.environ['ZZZ_FOO_BAR'] = '44'
        inidir = os.path.join(self.wd, 'files')
        c = Config(inidir, 'ZZZ')
        c.process()
        expect = {
            'FOO_BAR': '44',
            'FOO_BAZ': '029a',
            'BAR_FOO': 'oof',
            'XYZZY_BERT': 'ernie',
                }
        self.assertDictEqual(expect, c.store)

        os.environ['ZZZ_FOO_BAR'] = ''
        inidir = os.path.join(self.wd, 'files')
        c = Config(inidir, 'ZZZ')
        c.process()
        expect = {
            'FOO_BAR': '42',
            'FOO_BAZ': '029a',
            'BAR_FOO': 'oof',
            'XYZZY_BERT': 'ernie',
                }
        self.assertDictEqual(expect, c.store)

if __name__ == '__main__':
    unittest.main()
