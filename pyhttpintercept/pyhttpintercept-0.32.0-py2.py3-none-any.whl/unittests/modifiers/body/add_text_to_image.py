# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_modifier
from pyhttpintercept.intercept.modifiers.body import add_text_to_image as module_to_test
from simpil import SimpilImage

logging = logging_helper.setup_logging()


response = run_ad_hoc_modifier(module=module_to_test,
                               request=u'http://images.metadata.sky.com/pd-image/e6c1b884-5802-4efe-a669-eee522bd3b99/16-9/456?sid=4075',
                               filter=u'pd-image',
                               params="add text to\nimage")

image = SimpilImage(response.content)
image.save('temp.png')