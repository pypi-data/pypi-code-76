# -*- coding: utf-8 -*-

"""Test the docdata parser."""

import unittest

from docdata import docdata, parse_docdata
from docdata.api import _strip_trailing_lines


class TestUtils(unittest.TestCase):
    """Test utilities."""

    def test_strip_trailing_lines(self):
        """Test stripping trailing lines."""
        for expected, actual in [
            ([], []),
            (['hello'], ['hello']),
            (['hello'], ['hello', '']),
            (['hello'], ['hello', '', '']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye', '']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye', '', '']),
        ]:
            with self.subTest(value=actual):
                self.assertEqual(expected, _strip_trailing_lines(actual))


class B:
    """This class has a docdata."""


class D:
    """This class has a docdata.

    :param args: Nope.
    """

    def __init__(self, *args):
        """Initialize the class with dummy args."""
        self.args = args


@parse_docdata
class C3:
    """This class has a docdata.

    :param args: Nope.



    ---
    name: A
    """

    def __init__(self, *args):
        """Initialize the class with dummy args."""
        self.args = args


@parse_docdata
class C2:
    """This class has a docdata.

    :param args: Nope.

    ---
    name: A
    """

    def __init__(self, *args):
        """Initialize the class with dummy args."""
        self.args = args


@parse_docdata
class C1:
    """This class has a docdata.

    :param args: Nope.
    ---
    name: A
    """

    def __init__(self, *args):
        """Initialize the class with dummy args."""
        self.args = args


class TestParse(unittest.TestCase):
    """Test parsing docdata."""

    def _help(self, a, b):
        self.assertEqual(a.__doc__.rstrip(), b.__doc__.rstrip())
        self.assertIsNone(docdata(b))
        self.assertEqual({'name': 'A'}, docdata(a))

    def test_parse_no_params_no_newline(self):
        """Test parsing docdata with no params, and no trailing space.."""

        @parse_docdata
        class A:
            """This class has a docdata.
            ---
            name: A
            """  # noqa: D205

        self._help(A, B)

    def test_parse_no_params_one_newline(self):
        """Test parsing docdata with no params, and a newline before the delimiter."""

        @parse_docdata
        class A:
            """This class has a docdata.

            ---
            name: A
            """

        self._help(A, B)

    def test_parse_no_params_many_newline(self):
        """Test parsing docdata with no params, and a newline before the delimiter."""

        @parse_docdata
        class A:
            """This class has a docdata.



            ---
            name: A
            """  # noqa: D205

        self._help(A, B)

    def test_parse_with_params_no_newline(self):
        """Test parsing docdata."""
        self._help(C1, D)

    def test_parse_with_params_one_newline(self):
        """Test parsing docdata."""
        self._help(C2, D)

    def test_parse_with_params_many_newline(self):
        """Test parsing docdata."""
        self._help(C3, D)
