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
Base class - not meant for the end user.
"""

import numbers

import numpy as np

from getml.helpers import _str


class _Preprocessor:
    """
    Base class - not meant for the end user.
    """

    def __init__(self):
        self.type = "PreprocessorBaseClass"

    def __eq__(self, other):
        if not isinstance(other, _Preprocessor):
            raise TypeError("A preprocessor can only compared to another preprocessor!")

        # ------------------------------------------------------------

        # Check whether both objects have the same number of instance
        # variables.
        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False

        # ------------------------------------------------------------

        for kkey in self.__dict__:

            if kkey not in other.__dict__:
                return False

            # Take special care when comparing numbers.
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False

            elif self.__dict__[kkey] != other.__dict__[kkey]:
                return False

        # ------------------------------------------------------------

        return True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return _str(self.__dict__)

    def _getml_deserialize(self):
        # To ensure the getML can handle all keys, we have to add
        # a trailing underscore.
        encoding_dict = dict()

        for kkey in self.__dict__:
            encoding_dict[kkey + "_"] = self.__dict__[kkey]

        return encoding_dict
