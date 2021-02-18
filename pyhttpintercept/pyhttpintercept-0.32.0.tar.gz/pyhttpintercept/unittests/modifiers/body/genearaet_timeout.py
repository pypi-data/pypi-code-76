# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import generate_timeout as module_to_test
from timingsutil import Stopwatch


logging = logging_helper.setup_logging()

stopwatch = Stopwatch()

response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://www.google.co.uk',
                               filter=u'bing',  # simply match the string
                               params="5")
assert stopwatch.glance < 5

stopwatch.reset()
response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://www.google.co.uk',
                               filter=u'google',  # simply match the string
                               params="5")
assert stopwatch.glance > 5

stopwatch.reset()
response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://www.google.co.uk',
                               filter=u'.+goo.+k',  # simply match the string
                               params="6")
assert stopwatch.glance > 6
