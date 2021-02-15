# Originally auto-generated on 2019-09-09-11:35:02 -0400 Eastern Daylight Time
# By 'C:/Users/glenn/PycharmProjects/devtools/maketests/maketests.py -v -f testing.annotations'

from unittest import TestCase
from x7.lib.annotations import tests, tested_by
from x7.lib.inspect_more import item_name


@tests(tests, tested_by)
def something_or_other():
    pass


@tests(something_or_other)
def something_or_other_tester():
    pass


@tests(tests, tested_by)
def dummy(_a, _b):
    pass


def nothing_here():
    pass


@tests('x7.lib.annotations')
class TestModAnnotations(TestCase):
    """Tests for stand-alone functions in testing.annotations module"""

    @tests(tested_by, tests)
    def test_tested_by(self):
        something_or_other_set = {
            'x7.lib.annotations.tests',
            'x7.lib.annotations.tested_by'
        }
        self.assertSetEqual(something_or_other_set, tested_by(something_or_other))
        self.assertSetEqual({'tests.x7.lib.test_annotations.something_or_other'},
                            tested_by(something_or_other_tester))
        self.assertSetEqual(something_or_other_set, tested_by(dummy))
        self.assertSetEqual({'x7.lib.annotations.tested_by', 'x7.lib.annotations.tests'},
                            tested_by(type(self).test_tested_by))
        self.assertSetEqual(set(), tested_by(nothing_here))

    @tests(tests)
    def test_tests(self):
        # Note: additional cases tested by test_tested_by
        def dummy1(): pass

        def dummy2(): pass

        @tests(dummy1)
        def dummy3(): pass

        @tests(dummy1, dummy2, dummy3)
        def dummy_123(): pass

        @tests(dummy3)
        @tests(dummy1)
        @tests(dummy2)
        def dummy_312(): pass

        self.assertEqual(tests(dummy2)(dummy1), dummy1)
        self.assertEqual({item_name(dummy1)}, tested_by(dummy3))
        self.assertEqual(tested_by(dummy_123), tested_by(dummy_312))

        with self.assertRaises(FileNotFoundError):
            wrapper = tests('gg.devtools.maketests.not_loaded_module.item')
            wrapper(lambda: 1)  # pragma: no cover

        # Coverage only
        dummy1()
        dummy2()
        dummy3()
        dummy_123()
        dummy_312()
        something_or_other()
        something_or_other_tester()
        dummy(1, 2)
        nothing_here()
