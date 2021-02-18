# encoding: utf-8

u"""
================================================================================
Replaces the response text with the text in the provided file
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   :
Parameters : Local file containing replacement JSON
==================================================================================
"""

import logging_helper
import codecs
from pyhttpintercept.config.constants import ModifierConstant
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(response,
           modifier,
           **_):
    try:
        with codecs.open(modifier[ModifierConstant.params].strip(), encoding=u'utf-8') as t:
            content = t.read()
    except IOError:
        logging.error(u'Could not read from "{fn}"'
                      .format(fn=modifier[ModifierConstant.params].strip()))
    else:
        response._content = content.encode('utf-8')
        logging.info(u'Replaced content with: {c}'.format(c=content))

    return response
