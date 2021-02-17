from unittest import TestCase
from typing import NamedTuple
from x7.lib.annotations import tests
from x7.testing.maketests import parse, types
from x7.testing.support import Capture
from tests.x7.testing.maketests.test_mod_support import cm


class NoSubclasses(object):
    IgnoreThisNamedTuple = NamedTuple('IgnoreThisNamedTuple', a=int, b=str)


class WithSubsubclass(object):
    class WithSubclass(object):
        class TheSubclass(object):
            pass

        AlsoIgnoreThisNamedTuple = NamedTuple('AlsoIgnoreThisNamedTuple', a=int, b=str)


@tests(parse)
class Test0parse(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.parse module"""

    @tests(parse.expand_subclasses)
    def test_expand_subclasses(self):
        def do_expand(cls):
            found = {}
            parse.expand_subclasses(cls.__qualname__, cls, found)
            return found
        self.assertEqual({}, do_expand(NoSubclasses))
        self.assertEqual({
                'WithSubsubclass.WithSubclass':  WithSubsubclass.WithSubclass,
                'WithSubsubclass.WithSubclass.TheSubclass': WithSubsubclass.WithSubclass.TheSubclass,
            },
            do_expand(WithSubsubclass))
        self.assertEqual({}, do_expand(WithSubsubclass.WithSubclass.TheSubclass))

    @tests(parse.parse_module)
    def test_parse_module(self):
        from test_inputs import parse_basic
        parsed = parse.parse_module(cm(parse_basic), False, False)
        self.assertEqual({'TestModExample', 'TestModExample2', 'ClassGotImported'}, set(parsed.classes.keys()), )
        self.assertEqual({'a_function', 'func_got_imported'}, set(parsed.functions.keys()))

    @tests(parse.parse_module)
    def test_parse_module_verbose(self):
        from test_inputs import parse_basic
        with Capture() as capture:
            parsed = parse.parse_module(cm(parse_basic), True, False)
        self.assertEqual({'TestModExample', 'TestModExample2', 'ClassGotImported'}, set(parsed.classes.keys()), )
        self.assertEqual({'a_function', 'func_got_imported'}, set(parsed.functions.keys()))
        self.assertEqual(capture.stderr(), '')
        self.assertEqual('ParseModule:  test_inputs.parse_basic', capture.stdout())

    @tests(parse.parse_module)
    def test_parse_module_fails(self):
        from test_inputs import parse_missing
        with self.assertRaisesRegex(types.MaketestsError, 'INCLUDE.*NotFound.*EXCLUDE.*AlsoNotFound'):
            parse.parse_module(cm(parse_missing), False, False)
