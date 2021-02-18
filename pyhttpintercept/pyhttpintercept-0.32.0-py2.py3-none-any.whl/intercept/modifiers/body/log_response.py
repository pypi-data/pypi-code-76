# encoding: utf-8

u"""
================================================================================
Logs the response.  Use before modifying to see the original response or after
modifying to see the response sent to the box
----------------------------------------------------------------------------------
Filter     : A string or regular expression to match in the request.
             Leave blank to modify for all requests.
Override   : N/A
Parameters : N/A
==================================================================================
"""

import json
import logging_helper
from xml.etree import ElementTree
from fdutil.parse_xml import format_element_tree
from pyhttpintercept.intercept.handlers.support import decorate_for_uri_filter

logging = logging_helper.setup_logging()


@decorate_for_uri_filter
def modify(request,
           response,
           modifier,
           **_):

    content = response.content

    try:
        # Try to parse JSON
        json_data = json.loads(str(content))
        json_string = json.dumps(json_data, indent=4)

        log = logging_helper.LogLines(u'Response (JSON): ')
        log.extend(json_string.splitlines())

    except ValueError:

        try:
            # Try to parse XML
            root = ElementTree.fromstring(str(content))

            format_element_tree(root)

            xml_formatted_string = ElementTree.tostring(root)

            log = logging_helper.LogLines(u'Response (XML): ')
            log.extend(xml_formatted_string.splitlines())

        except ElementTree.ParseError:

            try:
                # Try to parse String
                logging.info(u'Response: {r}'.format(r=str(content)))

            except UnicodeDecodeError:
                logging.info(u'Response: <UnicodeDecodeError>')

    return response
