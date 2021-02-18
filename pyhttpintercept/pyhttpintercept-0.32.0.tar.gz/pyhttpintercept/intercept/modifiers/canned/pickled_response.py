# encoding: utf-8

u"""
====================================================
Used to return a response that has already been made
and pickled. This includes headers, status etc.

Modifiers that change the URI have no effect.

Modifiers that change the response will still be
applied

To get the pickler below

----------------------------------------------------
Filter     : String to match in the request URI
Override   :
Parameters : string containing a pickled requests
             object representing the canned response
====================================================
"""

import pickle
import logging_helper

logging = logging_helper.setup_logging()


def modify(uri,
           modifier):

    if modifier.passes_filter(value=uri,
                              wildcards=u'*'):
        # Raw bytes were pasted for the pickled response.
        # By the time it gets to us, it's a unicode string.
        # This can cause unpickling to fail.
        # We need to convert it back to raw bytes
        pickled = r''.join([chr(ord(b)) for b in modifier.params])
        logging.info(u'replacing original with pickled response')
        return pickle.loads(pickled)

    return None

