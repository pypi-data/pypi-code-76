# encoding: utf-8

u"""
==================================================================================
add_text_to_image settings
----------------------------------------------------------------------------------
Adds text to the image. Test will be centred and using the largest available font
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   :
Parameters : Text to add to the image
==================================================================================
"""


import logging_helper
from pyhttpintercept.config.constants import ModifierConstant
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter
from pyhttpintercept.intercept.handlers.support import (FIXED_WIDTH_FONTS,
                                                        FIXED_WIDTH_36,
                                                        FIXED_WIDTH_24,
                                                        decorate_for_uri_filter,
                                                        add_text_to_image_response)

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(response,
           modifier,
           **_):

    text = modifier[ModifierConstant.params]

    logging.info(response.url)

    add_text_to_image_response(response=response,
                               text=text)

    return response
