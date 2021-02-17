import os
import unittest
from typing import cast
from unittest.mock import patch

from x7.testing.maketests.types import Module
from x7.lib.annotations import tests
from x7.testing.maketests import mod_support


class MockModule(object):
    def __init__(self, name, package, root):
        self.__name__ = name
        self.__package__ = package
        self.__file__ = root + '/' + name.replace('.', '/') + '.py'

    def __str__(self):
        return 'MockModule(%s,%s,%s)' % (self.__name__, self.__package__, self.__file__)


def cm(obj):
    """Bogus cast to module required because PyCharm gets confused somewhere in type checking"""
    return cast(Module, obj)


@tests(mod_support)
class TestModModSupport(unittest.TestCase):
    """Tests for stand-alone functions in maketests.mod_support module"""

    @tests(mod_support.is_package)
    def test_is_package(self):
        # is_package(mod: module)
        self.assertTrue(mod_support.is_package(cm(MockModule('a.b.c', 'a.b.c', ''))))
        self.assertFalse(mod_support.is_package(cm(MockModule('a.b.c', 'a.b', ''))))
        self.assertTrue(mod_support.is_package(cm(unittest)))
        self.assertFalse(mod_support.is_package(cm(mod_support)))

    def test_MockModule(self):
        # Make sure coverage is 100%
        m = MockModule('a', 'b', 'c')
        self.assertIn('MockModule', str(m))

    @tests(mod_support.locate_output)
    def test_locate_output(self):
        # locate_output(input_module: module) -> str

        cases = (
            # module,  package,     test-dir,       expected,               expected-module
            ('a',       'a',        '',             ValueError,             None),
            ('a',       '',         '/tests',       '/tests/test_a.py',     'tests.test_a'),
            ('a.b',     'a',        '/a/tests',     '/a/tests/test_b.py',   'a.tests.test_b'),
            ('a.b',     'a',        '/tests',       '/tests/a/test_b.py',   'tests.a.test_b'),
            ('a.b',     'a',        '/a/b/tests',   FileNotFoundError,      None),
            ('tests.a', 'tests',    '/tests',       ValueError,             None),
        )

        def fix_path(p):
            return os.path.normcase(os.path.normpath(p))

        for root in ['', '/some/dir']:
            for mod_name, package_name, test_dir, expected, expected_module in cases:
                with self.subTest(module=mod_name, package=package_name, test_dir=test_dir, root=root):
                    full_test_dir = root + test_dir
                    mod = cm(MockModule(mod_name, package_name, root))
                    with patch('os.path.isdir', lambda s: fix_path(s) == fix_path(full_test_dir)):
                        if isinstance(expected, str):
                            out, out_mod = mod_support.locate_output(mod)
                            self.assertEqual(fix_path(out), fix_path(root+expected))
                            self.assertEqual(out_mod, expected_module)
                        else:
                            with self.assertRaises(expected):
                                mod_support.locate_output(mod)

    @tests(mod_support.gen_test_class_name)
    def test_gen_test_class_name(self):
        self.assertEqual('TestFooBar', mod_support.gen_test_class_name('FooBar'))
        self.assertEqual('TestFooBar', mod_support.gen_test_class_name('fooBar'))
        self.assertEqual('Test0fooBar', mod_support.gen_test_class_name('_fooBar'))

    @tests(mod_support.is_local)
    def test_is_local(self):
        self.assertTrue(mod_support.is_local(mod_support.is_local, cm(mod_support)))
        self.assertFalse(mod_support.is_local(self.test_is_local, cm(mod_support)))

    @tests(mod_support.mod_split)
    def test_mod_split(self):
        self.assertEqual(('head.part', 'tail'), mod_support.mod_split('head.part.tail'))
        self.assertEqual(('', 'tail_only'), mod_support.mod_split('tail_only'))
        self.assertEqual(('', 'os'), mod_support.mod_split(cm(os)))
        self.assertEqual(('x7.testing.maketests', 'mod_support'), mod_support.mod_split(cm(mod_support)))

    @tests(mod_support.mod_tail_join)
    def test_mod_tail_join(self):
        self.assertEqual('foo.bar.spam', mod_support.mod_tail_join('module.foo', 'bar.spam'))
        self.assertEqual('foo.bar.spam', mod_support.mod_tail_join('module.foo', 'bar', 'spam'))
