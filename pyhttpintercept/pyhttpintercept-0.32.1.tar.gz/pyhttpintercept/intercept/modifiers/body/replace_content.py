# encoding: utf-8

u"""
==================================================================================
Replace entire content string
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : New content string
----------------------------------------------------------------------------------

"""

import logging_helper
from future.utils import iteritems
from pyhttpintercept.intercept.handlers.support import parse_dictionary_parameters, decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    response._content = modifier.params

    return response
