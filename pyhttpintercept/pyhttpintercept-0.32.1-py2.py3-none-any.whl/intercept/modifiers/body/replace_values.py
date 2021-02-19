# encoding: utf-8

u"""
==================================================================================
Replace strings in the body
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : json dict of key:value pairs.
----------------------------------------------------------------------------------

"""

import logging_helper
from pyhttpintercept.intercept.handlers.support import decorate_for_json_parameters, decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_json_parameters
@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    content = response.content.decode('utf-8')

    for key, value in modifier.params.items():
        try:
            logging.info(u'Modifying body content: Replacing {k} with {v}'.format(k=key,
                                                                                 v=value))
            content = content.replace(key, value)

        except Exception as err:
            logging.error(u'Failed to replace {k} with {v}: {err}'.format(k=key,
                                                                          v=value,
                                                                          err=err))

    response._content = content.encode('utf-8')

    return response
