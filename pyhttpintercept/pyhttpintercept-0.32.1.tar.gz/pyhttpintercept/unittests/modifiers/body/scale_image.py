# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import scale_image as module_to_test
from simpil import SimpilImage

logging = logging_helper.setup_logging()


response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://cdn.skyq.sky.com/uk/epg/live/media/themes/kids/v1/skylogo_large.png',
                               filter=u'media/themes',
                               params="1.5")

image = SimpilImage(response.content)
assert image.width == int(183*1.5)
assert image.height == int(245*1.5)
