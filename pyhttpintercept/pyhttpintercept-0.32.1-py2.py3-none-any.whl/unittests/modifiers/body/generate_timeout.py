# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import generate_timeout as module_to_test
from timingsutil import Stopwatch


logging = logging_helper.setup_logging()

stopwatch = Stopwatch()

TEST_URL = u'http://echo.jsontest.com/key/value/one/two'

response = run_ad_hoc_modifier(module=module_to_test,
                               request=TEST_URL,
                               filter=u'google',  # Non matching string
                               params="5")
assert stopwatch.glance < 5

stopwatch.reset()
response = run_ad_hoc_modifier(module=module_to_test,
                               request=TEST_URL,
                               filter=u'jsontest',  # Matching the string
                               params="5")
assert stopwatch.glance > 5

stopwatch.reset()
response = run_ad_hoc_modifier(module=module_to_test,
                               request=TEST_URL,
                               filter=u'.+json.+t',  # Match using a regular expression
                               params="6")
assert stopwatch.glance > 6

stopwatch.reset()
response = run_ad_hoc_modifier(module=module_to_test,
                               request=TEST_URL,
                               filter=u'*',  # Bad regex
                               params="6")
assert stopwatch.glance < 6
