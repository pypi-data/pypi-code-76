# encoding: utf-8

import unittest
import pyhttpintercept
from pyhttpintercept import _metadata
import logging_helper
import json
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import replace_values as modifier
logging = logging_helper.setup_logging()


class TestConfiguration(unittest.TestCase):

    REPLACEMENTS = {u"milliseconds_since_epoch": u"flàpdoodle",
                    u"time": u"thyme"}

    PARAMS = json.dumps(REPLACEMENTS)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Instantiation
    def test_replace_values(self):
        response = run_ad_hoc_modifier(module=modifier,
                                       request="http://date.jsontest.com/",
                                       filter="j",
                                       params=self.PARAMS)
        for original, replacement in self.REPLACEMENTS.items():
            self.assertFalse(original in response.content)
            self.assertTrue(replacement in response.content)

    # Instantiation
    def test_replace_values_fails_filter(self):
        response = run_ad_hoc_modifier(module=modifier,
                                       request="http://date.jsontest.com/",
                                       filter="mismatch",
                                       params=self.PARAMS)
        for original, replacement in self.REPLACEMENTS.items():
            self.assertTrue(original in response.content)
            self.assertFalse(replacement in response.content)


if __name__ == u'__main__':
    unittest.main()
