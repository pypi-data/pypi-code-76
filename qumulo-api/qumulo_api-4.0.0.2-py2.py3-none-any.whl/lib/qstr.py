# Copyright (c) 2019 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

# qumulo_python_versions = { 2, 3 }

from __future__ import absolute_import, unicode_literals
from future.types.newstr import BaseNewStr, newstr
from future.utils import bytes_to_native_str, PY2, with_metaclass

from builtins import bytes as newbytes, isinstance, str as newstr


class BaseQstr(BaseNewStr):
    def __instancecheck__(cls, instance):
        return isinstance(instance, newstr)


# Default constructor arguments. Mapped to more meaningful defaults inside of
# __new__. Constants so that we can differentiate between no value being passed
# in verses the default value being explicitly passed in.
DEFAULT_ENCODING = object()  # mapped to 'UTF-8'
DEFAULT_ERRORS = object()  # mapped to 'strict'


class _qstr(with_metaclass(BaseQstr, newstr)):
    """
    A tweak on future's `newstr` which decodes unicode more reliably.

    There are five specific ways in which this differs from future's `newstr`:

    1) If you do not specify an encoding, `qstr` will use UTF-8. `newstr` uses
       `sys.getdefaultencoding()` by default, which is typically `'ascii'` in
       python 2 (though it can be set to something else by your `site.py`).
       Technically, `newstr` is correct that python 3's `str` defaults to
       `sys.getdefaultencoding()`. However, `sys.getdefaultencoding()` always
       returns `'UTF-8'` in python 3 (as of 3.4.1, though it can still be
       changed with some hacks). So hardcoding the default to `'UTF-8'` is more
       accurate to how `str` actually behaves in python 3.
    2) If you supply `qstr` with an encoding, it will always use that encoding
       to decode from bytes to unicode. `newstr` only uses the encoding for
       instances of python 2's `str` or its `newbytes` type.
    3) `qstr` throws a TypeError if you specify an `encoding`/`errors` when the
       first argument is already a `unicode`/python 3 `str`/`newstr`/`qstr`
       instance. This matches the behavior of python 3's `str`.
    4) `qstr` will never call `__str__` on bytes before attempting to decode
       them to unicode. `newstr` will call `__str__` on bytes if no `encoding`
       parameter is found. `newstr` does this so `newstr(newbytes()) == "b''"`,
       which matches python 3's behavior of `str(b'') == "b''"`. However,
       `newstr` is not fully matching the python3 behavior for multiple reaons:
           - `newbytes`'s `__str__` method is essentially `"b'{}'.format(self)`,
             and `newstr` will still attempt to decode the bytes into unicode
             after calling `__str__`. So `newstr(newbytes('\xfc'))` errors while
             decoding to unicode, whereas in python3 `str(b'\xfc') = "b'\\xfc'"`
           - This modification is only happening for `newbytes`, not native
             bytes (i.e. python 2's `str`). Likely `newstr` is not trying to
             modify native bytes because that would break interoperability, but
             the result is that `newstr(b)` returns different values depending
             on the implementation of bytes which `b` is using, instead of just
             the underlying data which `b` represents.
           - `newstr` does not fully respect the `errors` parameter.
             `newstr(newbytes(), errors='strict') == "b''"` whereas in python 3
             `str(b'', errors='strict') == ''`. This is likely a bug.
    5) `str(qstr_instance)` encodes using UTF-8, instead of
       `sys.getdefaultencoding()`, for the same reasons discussed in the first
       item in this list.

    The first tweak is important because it is very common for a python 2 `str`
    to be passed into `newstr` without specifying an encoding. For example:

        from builtins import str
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--name', type=str)
        arser.parse_args()

    Because `sys.argv` is an array of `str` instead of `unicode`, and `type=str`
    refers to future's `newstr`, this will cause a `UnicodeDecodeError` in
    python 2 (in most environments) if a non-ASCII character was supplied.
    """

    def __new__(cls, s=b'', encoding=DEFAULT_ENCODING, errors=DEFAULT_ERRORS):
        if not (
            encoding is DEFAULT_ENCODING and errors is DEFAULT_ERRORS
        ) and isinstance(s, newstr):
            raise TypeError('decoding str is not supported')

        if encoding is DEFAULT_ENCODING:
            encoding = 'UTF-8'
        if errors is DEFAULT_ERRORS:
            errors = 'strict'

        # If decoding from unicode is required, ensure that we've converted `s`
        # to `bytes` before passing on to `newstr.__new__`, so that it uses the
        # encoding we supply it when decoding `s.__str__`.
        if not (isinstance(s, (newstr, newbytes)) or hasattr(s, '__unicode__')):
            s = s.__str__()

        return super(_qstr, cls).__new__(cls, s, encoding=encoding, errors=errors)

    def __str__(self):
        # `newstr().encode(...)` returns a `newbytes`, so we have to convert to
        # built-in `str` before returning. `__str__` must return an instance of
        # the built-in `str` or else we'll run into subtle bugs.
        return bytes_to_native_str(self.encode('UTF-8'))


# In python 3, we export the builtin string type instead of our implementation.
qstr = _qstr if PY2 else str  # pylint: disable=str-must-be-qstr
