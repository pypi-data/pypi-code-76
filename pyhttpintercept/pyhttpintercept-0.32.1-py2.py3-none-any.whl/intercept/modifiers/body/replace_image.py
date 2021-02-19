# encoding: utf-8

u"""
==================================================================================
replace_image settings
----------------------------------------------------------------------------------
Replace the image with another. The replacement should be of the same type.
e.g. replace a JPG with a JPG
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   :
Parameters : Path or URI of image
==================================================================================
"""

from simpil import SimpilImage

import logging_helper
from pyhttpintercept.config.constants import ModifierConstant
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(response,
           modifier,
           **_):

    path = modifier[ModifierConstant.params]

    logging.info(response.url)

    try:
        replacement_image = SimpilImage(path)

    except Exception as err:
        logging.exception(err)
        raise err

    response._content = replacement_image.image_data()

    return response
