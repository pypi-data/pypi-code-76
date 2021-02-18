# encoding: utf-8

u"""
==================================================================================
Replace entire content string
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : Key:Value pairs to replace in the response body
----------------------------------------------------------------------------------

"""
import logging_helper
from future.utils import iteritems
from pyhttpintercept.intercept.handlers.support import decorate_for_dictionary_parameters, decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_dictionary_parameters
@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    content = response.content

    for key, value in iteritems(modifier.params):
        try:
            logging.info(u'Modifying body content: Replacing {k} with {v}'.format(k=key,
                                                                                  v=value))
            content.replace(key, value)

        except Exception as err:
            logging.error(u'Failed to replace {k} with {v}: {err}'.format(k=key,
                                                                          v=value,
                                                                          err=err))

    response._content = content

    return response
