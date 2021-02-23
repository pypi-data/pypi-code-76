# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Contains various constants for getML
"""


JOIN_KEY_SEP = "$GETML_JOIN_KEY_SEP"

MULTIPLE_JOIN_KEYS_BEGIN = "$GETML_MULTIPLE_JOIN_KEYS_BEGIN"

MULTIPLE_JOIN_KEYS_END = "$GETML_MULTIPLE_JOIN_KEYS_END"

NO_JOIN_KEY = "$GETML_NO_JOIN_KEY"

TIME_FORMATS = [
    "%Y-%m-%dT%H:%M:%s%z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S.%F",  # microsecond
    "%Y-%m-%dT%H:%M:%S.%i",  # millisecond
    "%Y-%m-%dT%H:%M:%S.%c",  # centisecond
    "%Y-%m-%d %H:%M:%S.%F",  # microsecond
    "%Y-%m-%d %H:%M:%S.%i",  # millisecond
    "%Y-%m-%d %H:%M:%S.%c",  # centisecond
    "%Y-%m-%d %H:%M:%s%z",
]
"""The default time stamp formats to be used.

Whenever a time stamp is parsed from a string,
the getML engine tries different time stamp formats.

The procedure works as follows: The engine tries to parse the string
using the first format. If that fails, it will use the second format etc.

If none of the time stamp formats work, then it tries to parse the string
as a floating point value, which it will interpret as the number of
seconds since UNIX time (January 1, 1970).

If that fails as well, the value is set to NULL.
"""
