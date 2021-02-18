# encoding: utf-8

u"""
==================================================================================
scale settings
----------------------------------------------------------------------------------
Adds text to the image. Test will be centred and using the largest available font
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   :
Parameters : scale factor
==================================================================================
"""


import logging_helper
from pyhttpintercept.config.constants import ModifierConstant
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter
from simpil import SimpilImage

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(response,
           modifier,
           **_):

    scale = float(modifier[ModifierConstant.params])

    logging.info(response.url)

    try:
        original_image = SimpilImage(response.content)
    except Exception as err:
        logging.exception(err)
        raise err

    original_image.scale(scale)

    response._content = original_image.image_data()

    return response
