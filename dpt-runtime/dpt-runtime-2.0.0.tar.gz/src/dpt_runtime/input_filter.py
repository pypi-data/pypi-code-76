# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;runtime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v2.0.0
dpt_runtime/input_filter.py
"""

# pylint: disable=import-error,no-name-in-module

from unicodedata import category as unicode_category
import re

try: from collections.abc import Sequence
except ImportError: from collections import Sequence

try: from urllib.parse import quote
except ImportError: from urllib import quote

from .binary import Binary

class InputFilter(object):
    """
"InputFilter" provides basic input filter functions.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: runtime
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = [ ]
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    @staticmethod
    def filter_control_chars(data, tab_allowed = False):
        """
There are some persons out there that may want to inject control characters
into our system. The function "filter_control_chars()" will remove these
characters.

:param data: Input string

:return: (str) Filtered string
:since:  v1.0.0
        """

        data = Binary.utf8(data)

        if (isinstance(data, Binary.UNICODE_TYPE)):
            data_position = 0
            data_length = len(data)

            while (data_position < data_length):
                value = data[data_position]
                value_unicode_category = unicode_category(value)

                if ((value_unicode_category == "Cc" and value != "\n" and ((not tab_allowed) or value != "\t")) or value_unicode_category == "Cn" or value_unicode_category == "Co"):
                    data = data[:data_position] + data[1 + data_position:]
                    data_length -= 1
                else: data_position += 1
            #

            data = Binary.str(data)
        else: data = ""

        return data
    #

    @staticmethod
    def filter_email_address(data):
        """
Checks a eMail address if it's valid (RFC822) and returns the (unfolded)
ASCII address if it is. Does not recognize comments.

:param data: Input eMail

:return: (str) Filtered eMail address or empty string if the address is not
         valid
:since:  v1.0.0
        """

        # pylint: disable=broad-except

        email_address = InputFilter.filter_control_chars(data)
        email_address = re.sub("\\r\\n([\\x09\\x20])+", "\\1", email_address)

        is_valid = True
        quote_count = 0

        data_parts = email_address.split("\"")
        domain_part = ""
        local_part = ""
        quoted_part = ""

        re_char_escaped = re.compile("([\\\\]+)$")
        re_valid_chars = re.compile("^[\\x00-\\x0c\\x0e-\\x7f]+$")
        re_invalid_chars = re.compile("[\\x00-\\x20\\x22\\x28\\x29\\x2c\\x3a-\\x3c\\x3e\\x40\\x5b-\\x5d\\x7f-\\xff]")

        for data_part in data_parts:
            # Is it a unquoted part?
            if ((quote_count % 2) == 0):
                if ("@" in data_part):
                    at_splitted = data_part.split("@")
                    if (re_valid_chars.match(at_splitted[0]) is None): at_splitted[0] = quote(at_splitted[0])

                    if (domain_part == ""
                        and len(at_splitted) < 3
                        and re_invalid_chars.search(at_splitted[0]) is None
                        and ".." not in at_splitted[0]
                        and ".." not in at_splitted[1]
                       ):
                        local_part += at_splitted[0]
                        domain_part = at_splitted[1]
                    else:
                        is_valid = False
                        break
                    #
                elif (".." in data_part or re_invalid_chars.search(data_part) is not None):
                    is_valid = False
                    break
                else: local_part += data_part

                quote_count += 1
            else:
                quoted_part += data_part
                re_result = re_char_escaped.search(data_part)

                # Is it escaped?
                if (re_result is not None and (len(re_result.group(1)) % 2) == 1):
                    is_valid = False
                    quoted_part += "\""
                else:
                    is_valid = True
                    quote_count += 1

                    local_part += (quote(quoted_part) if (re_valid_chars.match(quoted_part) is None) else "\"{0}\"".format(quoted_part))
                    quoted_part = ""
                #
            #

            if (quote_count > 3): quote_count = 0
        #

        if (domain_part == ""): is_valid = False
        elif (is_valid
              and (re_invalid_chars.search(domain_part[1:-1]) is not None
                   if (domain_part[:1] == "[" and domain_part[-1:] == "]") else
                   re_invalid_chars.search(domain_part) is not None
                  )
             ):
            domain_part = Binary.utf8(domain_part)

            try: domain_part = Binary.raw_str(domain_part.encode("idna"))
            except Exception: is_valid = False
        #

        return ("{0}@{1}".format(local_part, domain_part) if (is_valid) else "")
    #

    @staticmethod
    def filter_file_path(data, uprefs_allowed = False):
        """
File paths should never contain target definitions like directory
traversals. We will filter them using "filterFilePath()".

:param data: Input path
:param uprefs_allowed: True to not remove references that leave the current
                       base directory

:return: (str) Filtered output path
:since:  v1.0.0
        """

        data = InputFilter.filter_control_chars(data)

        if (isinstance(data, str)):
            data = re.sub("^(\\w{3,5})://", "", data)

            data = data.replace("/./", "/")
            data = data.replace("\\", "")
            data = re.sub("\\w/[./]", "", data)

            if ((not uprefs_allowed) and data != "."):
                data = re.sub("^[./]+", "", data)
                data = re.sub("[./]+$", "", data)
            #
        #

        return data
    #

    @staticmethod
    def filter_float(data):
        """
Check and convert to float.

:param data: Input string

:return: (float) Filtered output float; None on error
:since:  v1.0.0
        """

        try:
            if (data is not None): data = float(data)
        except ValueError: data = None

        return data
    #

    @staticmethod
    def filter_int(data):
        """
Check and convert to int.

:param data: Input string

:return: (int) Filtered output integer; None on error
:since:  v1.0.0
        """

        try:
            if (data is not None): data = int(data)
        except ValueError: data = None

        return data
    #

    @staticmethod
    def filter_unique_list(_list):
        """
Returns a list where each entry is unique.

:return: (list) Unique list of entries given
:since:  v1.0.0
        """

        _return = [ ]

        if (isinstance(_list, Sequence)):
            try: _return = list(set(_list))
            except TypeError:
                for entry in _list:
                    if entry not in _return: _return.append(entry)
                #
            #
        #

        return _return
    #
#
