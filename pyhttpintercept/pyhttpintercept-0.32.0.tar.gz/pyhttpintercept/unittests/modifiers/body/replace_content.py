# encoding: utf-8

import unittest
import pyhttpintercept
from pyhttpintercept import _metadata
import logging_helper
import json
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import replace_content as modifier
logging = logging_helper.setup_logging()


class TestConfiguration(unittest.TestCase):

    REPLACEMENT = "replaced content"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Instantiation
    def test_replace_values(self):
        response = run_ad_hoc_modifier(module=modifier,
                                       request="http://date.jsontest.com/",
                                       filter="j",
                                       params=self.REPLACEMENT)
        self.assertEqual(response.content, self.REPLACEMENT)

    # Instantiation
    def test_replace_values_fails_filter(self):
        response = run_ad_hoc_modifier(module=modifier,
                                       request="http://date.jsontest.com/",
                                       filter="mismatch",
                                       params=self.REPLACEMENT)
        self.assertNotEqual(response.content, self.REPLACEMENT)


if __name__ == u'__main__':
    unittest.main()
