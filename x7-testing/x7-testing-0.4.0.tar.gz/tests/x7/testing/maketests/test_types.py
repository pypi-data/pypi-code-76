from unittest import TestCase
from x7.lib.annotations import tests
from x7.testing.maketests import types


@tests('x7.testing.maketests.types.MaketestsError')
class TestMaketestsError(TestCase):
    def test_simple(self):
        self.assertTrue('If it parsed, then it works')


@tests('x7.testing.maketests.types')
class Test0types(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.types module"""

    @tests('x7.testing.maketests.types.is_namedtuple')
    def test_is_namedtuple(self):
        self.assertTrue(types.is_namedtuple(types.ParsedModule))
        self.assertFalse(types.is_namedtuple(Test0types))
