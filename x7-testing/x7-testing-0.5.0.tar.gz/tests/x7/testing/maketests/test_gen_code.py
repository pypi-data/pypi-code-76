import importlib
import inspect
import re
from unittest import TestCase
from x7.testing.maketests import gen_code, outmap
from x7.testing.maketests.types import ParsedModule
from x7.testing.support import Capture
from x7.lib.annotations import tests

EXPECTED_FUNC_PLAIN = """
    @tests(test_gen_code.func_under_test)
    def test_func_under_test(self):
        # func_under_test()
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.func_under_test test
""".strip('\n')
EXPECTED_FUNC_IN_CLASS = """
    @tests(test_gen_code.TestModGenCode.func_under_test)
    def test_func_under_test(self):
        # func_under_test()
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.TestModGenCode.func_under_test test
""".strip('\n')
EXPECTED_GEN_MOD_CLASS = '''
@tests(bar)
class TestModBar(TestCase):
    """Tests for stand-alone functions in foo.bar module"""

    @tests(test_gen_code.member)
    def test_member(self):
        # member()
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.member test
'''.strip('\n')
EXPECTED_CLASS = """
*   @tests(test_gen_code.Klass)
*   class TestKlass(TestCase):
h
h       @classmethod
h       def setUpClass(cls):
h           pass
h
h       @classmethod
h       def tearDownClass(cls):
h           pass
h
h       def setUp(self):
h           # Once per test
h           pass
h
h       def tearDown(self):
h           pass
h
p       pass
Z
a       @tests(test_gen_code.Klass.a_func)
a       def test_a_func(self):
a           # a_func(self)
a           pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.Klass.a_func test
A
b       @tests(test_gen_code.Klass.b_func)
b       def test_b_func(self):
b           # b_func(self, x, y)
b           pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.Klass.b_func test
""".lstrip('\n')
EXPECTED_PARSE_EMPTY = '''
# HEADER

from unittest import TestCase
from x7.lib.annotations import tests
from test_inputs import parse_empty


@tests(parse_empty)
class TestModParseEmpty(TestCase):
    """Tests for stand-alone functions in test_inputs.parse_empty module"""

    @tests(parse_empty.just_one_function)
    def test_just_one_function(self):
        # just_one_function()
        pass  # TODO-impl test_inputs.parse_empty.just_one_function test
'''.lstrip('\n')
EXPECTED_PARSE_EMPTY_STDOUT = """
Items to add:
    funcs in module:test_inputs.parse_empty
        test_inputs.parse_empty.just_one_function
""".strip('\n')
EXPECTED_PARSE_EMPTY_DRYRUN_STDOUT = '''
ParseModule:  test_inputs.parse_empty
Testmap:
Tested:
Added: test_inputs.parse_empty.just_one_function
Items to add:
    funcs in module:test_inputs.parse_empty
        test_inputs.parse_empty.just_one_function
# HEADER

from unittest import TestCase
from x7.lib.annotations import tests
from test_inputs import parse_empty


@tests(parse_empty)
class TestModParseEmpty(TestCase):
    """Tests for stand-alone functions in test_inputs.parse_empty module"""

    @tests(parse_empty.just_one_function)
    def test_just_one_function(self):
        # just_one_function()
        pass  # TODO-impl test_inputs.parse_empty.just_one_function test
'''.strip('\n')
EXPECTED_GEN_MODULE_EXAMPLE_VERBOSE = '''
ParseModule:  test_inputs.example
Testmap:
Tested:
Added: test_inputs.example.AClass, test_inputs.example.AClass.AClassSubclass, test_inputs.example.AClass.AClassSubclass.nothing,
    test_inputs.example.AClass.__init__, test_inputs.example.AClass.__str__, test_inputs.example.AClass.ab, test_inputs.example.AClass.add,
    test_inputs.example.a_function, test_inputs.example_imported.ClassGotImported, test_inputs.example_imported.ClassGotImported.__init__,
    test_inputs.example_imported.ClassGotImported.show, test_inputs.example_imported.another_func_got_imported, test_inputs.example_imported.func_got_imported
Items to add:
    class test_inputs.example.AClass:
    class test_inputs.example.AClass.AClassSubclass:
        test_inputs.example.AClass.AClassSubclass.nothing
    funcs in test_inputs.example.AClass
        test_inputs.example.AClass.__init__
        test_inputs.example.AClass.__str__
        test_inputs.example.AClass.ab
        test_inputs.example.AClass.add
    class test_inputs.example_imported.ClassGotImported:
        test_inputs.example_imported.ClassGotImported.__init__
        test_inputs.example_imported.ClassGotImported.show
    funcs in module:test_inputs.example
        test_inputs.example.a_function
    funcs in module:test_inputs.example_imported
        test_inputs.example_imported.another_func_got_imported
        test_inputs.example_imported.func_got_imported
'''.strip('\n')
EXPECTED_GEN_MODULE_EXAMPLE_EXISTS_VERBOSE = '''
ParseModule:  test_inputs.example
  Class: TestAClass -> tests test_inputs.example.AClass
  Class: TestAClass0AClassSubclass -> tests test_inputs.example.AClass.AClassSubclass
  Class: TestClassGotImported -> tests test_inputs.example_imported.ClassGotImported
  Class: TestModExample -> tests test_inputs.example
Classes:
  TestAClass: ClassSrcInfo(cls=<class 'test_inputs.output_example.TestAClass'>, start=9, last=30)
  TestAClass0AClassSubclass: ClassSrcInfo(cls=<class 'test_inputs.output_example.TestAClass0AClassSubclass'>, start=32, last=38)
  TestClassGotImported: ClassSrcInfo(cls=<class 'test_inputs.output_example.TestClassGotImported'>, start=40, last=51)
  TestModExample: ClassSrcInfo(cls=<class 'test_inputs.output_example.TestModExample'>, start=53, last=71)
Testmap:
  test_inputs.example.AClass: TestAClass
  test_inputs.example.AClass.AClassSubclass: TestAClass0AClassSubclass
  test_inputs.example_imported.ClassGotImported: TestClassGotImported
  test_inputs.example: TestModExample
Testmap: test_inputs.example, test_inputs.example.AClass, test_inputs.example.AClass.AClassSubclass, test_inputs.example_imported.ClassGotImported
Tested: test_inputs.example, test_inputs.example.AClass, test_inputs.example.AClass.AClassSubclass, test_inputs.example.AClass.AClassSubclass.nothing,
    test_inputs.example.AClass.__init__, test_inputs.example.AClass.__str__, test_inputs.example.AClass.ab, test_inputs.example.AClass.add,
    test_inputs.example.a_function, test_inputs.example_imported.ClassGotImported, test_inputs.example_imported.ClassGotImported.__init__,
    test_inputs.example_imported.ClassGotImported.show, test_inputs.example_imported.another_func_got_imported, test_inputs.example_imported.func_got_imported
Added:
'''.strip('\n')
EXPECTED_CLASS_EXTRA = '''
@tests(test_gen_code.KlassExtra)
class TestKlassExtra(TestCase):
    @tests(test_gen_code.KlassExtra.class_method)
    def test_class_method(self):
        # class_method()
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.class_method test

    @tests(test_gen_code.KlassExtra.get_and_set)
    def test_get_and_set(self):
        # value = self.get_and_set
        # self.get_and_set = value
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set test

    @tests(test_gen_code.KlassExtra.get_and_set_and_del)
    def test_get_and_set_and_del(self):
        # value = self.get_and_set_and_del
        # self.get_and_set_and_del = value
        # del self.get_and_set_and_del
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set_and_del test

    @tests(test_gen_code.KlassExtra.get_only)
    def test_get_only(self):
        # value = self.get_only
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.get_only test

    @tests(test_gen_code.KlassExtra.standard_method)
    def test_standard_method(self):
        # standard_method(self)
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.standard_method test

    @tests(test_gen_code.KlassExtra.static_method)
    def test_static_method(self):
        # static_method()
        pass  # TODO-impl tests.x7.testing.maketests.test_gen_code.KlassExtra.static_method test
'''.strip('\n')


def expected_class(filt='*ab'):
    return '\n'.join(l[4:] for l in EXPECTED_CLASS.splitlines() if l[0] in filt)


def remove_comments(text: str):
    """Remove single-line comments, replace TO+DO with TO_DO to avoid it getting 'caught'"""
    return '\n'.join(l.replace('# TODO', '# TO_DO') for l in text.splitlines() if not l.startswith('#'))


def func_under_test():
    pass


class BaseKlass(object):
    def ignore_this(self):
        pass


class Klass(BaseKlass):
    IGNORE_ME = 'not a class or function'
    AndMe = Capture

    class IgnoreThisToo(object):
        pass

    def a_func(self):
        pass

    def b_func(self, x, y):
        pass


class Klazz(BaseKlass):
    """Empty class for testing no member functions"""


class KlassExtraBase:
    @property
    def prop_inherited(self):
        return 1


class KlassExtra(KlassExtraBase):
    """Example to test class properties, static- and class- methods"""
    value = 1

    def standard_method(self):
        return self.value

    @staticmethod
    def static_method():
        return 4

    @classmethod
    def class_method(cls):
        pass

    @property
    def get_only(self):
        return self.value

    @property
    def get_and_set(self):
        return self.value

    @get_and_set.setter
    def get_and_set(self, value):
        self.value = value

    @property
    def get_and_set_and_del(self):
        return self.value

    @get_and_set_and_del.setter
    def get_and_set_and_del(self, value):
        self.value = value

    @get_and_set_and_del.deleter
    def get_and_set_and_del(self):
        del self.value


@tests(gen_code)
class TestModGenCode(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.gen_code module"""
    @tests(gen_code.gen_func)
    def test_gen_func_plain(self):
        added = dict()
        tested = dict()
        result = gen_code.gen_func('func_under_test', func_under_test, None, added, tested)
        self.assertEqual(EXPECTED_FUNC_PLAIN, result)
        self.assertEqual(
            {
                'tests.x7.testing.maketests.test_gen_code.func_under_test':
                'module:tests.x7.testing.maketests.test_gen_code',
            },
            added)
        self.assertEqual({}, tested)

    @tests(gen_code.gen_func)
    def test_gen_func_in_class(self):
        added = dict()
        tested = dict()
        result = gen_code.gen_func('func_under_test', func_under_test, TestModGenCode, added, tested)
        self.assertEqual(EXPECTED_FUNC_IN_CLASS, result)
        self.assertEqual(
            {
                'tests.x7.testing.maketests.test_gen_code.TestModGenCode.func_under_test':
                'tests.x7.testing.maketests.test_gen_code.TestModGenCode',
            },
            added)
        self.assertEqual({}, tested)

    @tests(gen_code.gen_func)
    def test_gen_func_already_tested(self):
        added = dict()
        tested = {'tests.x7.testing.maketests.test_gen_code.func_under_test': 'any-str'}
        tested_orig = dict(**tested)
        result = gen_code.gen_func('func_under_test', func_under_test, None, added, tested)
        self.assertIsNone(result)
        self.assertEqual({}, added)
        self.assertEqual(tested_orig, tested)

    @tests(gen_code.gen_class)
    def test_gen_class_verbose(self):
        with Capture() as capture:
            self.test_gen_class(True)
        lines = [
            '? gen_class(tests.x7.testing.maketests.test_gen_code.Klass)-what is IGNORE_ME:not a class or function',
            'found class-local class: tests.x7.testing.maketests.test_gen_code.Klass.IgnoreThisToo, should already be handled',
            'skipping apparently inherited function: ignore_this in tests.x7.testing.maketests.test_gen_code.Klass',
        ]
        self.assertEqual('\n'.join(lines), capture.stdout())
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_class)
    @tests(gen_code.gen_property)
    def test_gen_class_extra_verbose(self):
        with Capture() as capture:
            self.test_gen_class_extra(True)
        lines = [
            '.get_and_set: found property: <property object at 0x7fe7701cd5e0>',
            '   with fget=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set fset=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set fdel=None',
            '.get_and_set_and_del: found property: <property object at 0x7fe7701cd590>',
            '   with fget=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set_and_del fset=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set_and_del fdel=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_and_set_and_del',
            '.get_only: found property: <property object at 0x7fe7701cd540>',
            '   with fget=tests.x7.testing.maketests.test_gen_code.KlassExtra.get_only fset=None fdel=None',
            '.prop_inherited: found property: <property object at 0x7fe7701cd4a0>',
            '   with fget=tests.x7.testing.maketests.test_gen_code.KlassExtraBase.prop_inherited fset=None fdel=None',
            'skipping apparently inherited property: prop_inherited in tests.x7.testing.maketests.test_gen_code.KlassExtra',
            '? gen_class(tests.x7.testing.maketests.test_gen_code.KlassExtra)-what is value:1'
        ]

        stdout = capture.stdout()
        # import pprint; pprint.pp(stdout.splitlines(), width=160)
        lines = '\n'.join(lines)
        hex_pat = re.compile('0x([0-9A-Fa-f]+)')
        self.assertEqual(hex_pat.sub('0x...', lines), hex_pat.sub('0x...', stdout))
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_class)
    def test_gen_class(self, verbose=False):
        added = {}
        tested = {}
        text, isnew = gen_code.gen_class('Klass', Klass, added, tested, verbose)
        self.assertEqual(True, isnew)
        self.assertEqual(expected_class('*abA'), text)
        self.assertEqual({
                'tests.x7.testing.maketests.test_gen_code.Klass': 'class',
                'tests.x7.testing.maketests.test_gen_code.Klass.a_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
                'tests.x7.testing.maketests.test_gen_code.Klass.b_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
            },
            added)
        self.assertEqual({}, tested)

    @tests(gen_code.gen_class)
    def test_gen_class_exists(self, verbose=False):
        added = {}
        tested = {'tests.x7.testing.maketests.test_gen_code.Klass': 'class'}
        text, isnew = gen_code.gen_class('Klass', Klass, added, tested, verbose)
        self.assertEqual(False, isnew)
        self.assertEqual(expected_class('abA'), text)
        self.assertEqual({
                'tests.x7.testing.maketests.test_gen_code.Klass.a_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
                'tests.x7.testing.maketests.test_gen_code.Klass.b_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
            },
            added)
        self.assertEqual({'tests.x7.testing.maketests.test_gen_code.Klass': 'class'}, tested)

    @tests(gen_code.gen_class)
    def test_gen_class_and_func_exist(self, verbose=False):
        added = {}
        tested_orig = {
            'tests.x7.testing.maketests.test_gen_code.Klass': 'class',
            'tests.x7.testing.maketests.test_gen_code.Klass.a_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
        }
        tested = dict(**tested_orig)
        text, isnew = gen_code.gen_class('Klass', Klass, added, tested, verbose)
        self.assertEqual(False, isnew)
        self.assertEqual(expected_class('b'), text)
        self.assertEqual({
                'tests.x7.testing.maketests.test_gen_code.Klass.b_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
            },
            added)
        self.assertEqual(tested_orig, tested)

    @tests(gen_code.gen_class)
    def test_gen_class_all_exist(self, verbose=False):
        added = {}
        tested_orig = {
            'tests.x7.testing.maketests.test_gen_code.Klass': 'class',
            'tests.x7.testing.maketests.test_gen_code.Klass.a_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
            'tests.x7.testing.maketests.test_gen_code.Klass.b_func': 'tests.x7.testing.maketests.test_gen_code.Klass',
        }
        tested = dict(**tested_orig)
        text, isnew = gen_code.gen_class('Klass', Klass, added, tested, verbose)
        self.assertEqual(False, isnew)
        self.assertEqual('', text)
        self.assertEqual({
            },
            added)
        self.assertEqual(tested_orig, tested)

    @tests(gen_code.gen_class)
    def test_gen_class_empty(self, verbose=False):
        added = {}
        tested = {}
        text, isnew = gen_code.gen_class('Klazz', Klazz, added, tested, verbose)
        self.assertEqual(True, isnew)
        self.assertEqual(expected_class('*p').replace('Klass', 'Klazz'), text)
        self.assertEqual({'tests.x7.testing.maketests.test_gen_code.Klazz': 'class'}, added)
        self.assertEqual({}, tested)

    @tests(gen_code.gen_class)
    @tests(gen_code.gen_property)
    def test_gen_class_extra(self, verbose=False):
        added = {}
        tested = {}

        debug = False
        if debug:
            for member, value in inspect.getmembers(KlassExtra):
                is_set = set()
                for is_method in [ism for ism in dir(inspect) if ism.startswith('is')]:
                    if getattr(inspect, is_method)(value):
                        is_set.add(is_method)
                print('KlassExtra.%s (%s) is %s' % (member, value, ', '.join(sorted(is_set))))
                if qualname := getattr(value, '__qualname__', None):
                    print('   ', qualname)

        text, isnew = gen_code.gen_class('KlassExtra', KlassExtra, added, tested, verbose)
        self.assertEqual(True, isnew)
        self.assertEqual(EXPECTED_CLASS_EXTRA, text)
        base = 'tests.x7.testing.maketests.test_gen_code.KlassExtra'
        keys = ',.class_method,.get_and_set,.get_and_set_and_del,.get_only,.standard_method,.static_method'.split(',')
        expected_added = dict((base+key, base if key else 'class') for key in keys)
        self.assertEqual(expected_added, added)
        self.assertEqual({}, tested)

    def test_force_coverage(self):
        """Just call dummy functions to force coverage"""
        func_under_test()
        BaseKlass().ignore_this()
        k = Klass()
        k.a_func()
        k.b_func(1, 2)

    @tests(gen_code.coverage_gets_confused)
    def test_coverage_gets_confused(self):
        gen_code.coverage_gets_confused()

    @tests(gen_code.gen_mod_class_test)
    def test_gen_mod_class_test(self):
        dst = outmap.OutputMap(verbose=False)
        src = ParsedModule({}, {'member': self.test_gen_mod_class_test}, 'any.mod', set())
        text = gen_code.gen_mod_class_test('foo.bar', dst, src)
        self.assertEqual(EXPECTED_GEN_MOD_CLASS, text)


@tests(gen_code)        # TODO-should be able to say @tests(gen_code.gen_module) and apply to all tests
class TestFuncGenModule(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.gen_code module"""

    def assertCodeEqual(self, raw_expected, raw_actual):
        """Compare code without comments"""

        expected = remove_comments(raw_expected)
        actual = remove_comments(raw_actual)
        if expected != actual and False:    # pragma: no cover
            import difflib
            diffs = difflib.context_diff(expected.splitlines(), actual.splitlines(), 'Expected', 'Actual')
            print('\n'.join(diffs))
        self.maxDiff = 10000
        self.assertEqual(expected, actual)

    def assertEqualsExampleOutput(self, out_mod_name, stdout=None,
                                  verbose=False, dryrun=False, doprint=False, debug=False):
        testmod = importlib.import_module('test_inputs.example')
        with Capture() as capture:
            text = gen_code.gen_module(
                testmod, out_mod_name, '# HEADER',
                verbose=verbose, dryrun=dryrun, doprint=doprint, debug=debug)
        expected = inspect.getsource(importlib.import_module('test_inputs.output_example'))
        self.assertCodeEqual(expected, text)
        self.assertNotIn('error', text.lower())
        if stdout:
            self.assertEqual(stdout, capture.stdout())
        else:
            self.assertNotIn('error', capture.stdout().lower())
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_module)
    def test_gen_module_empty(self):
        testmod = importlib.import_module('test_inputs.parse_empty')
        with Capture() as capture:
            text = gen_code.gen_module(testmod, 'tests.test_output_module', '# HEADER')
        self.assertEqual(EXPECTED_PARSE_EMPTY, text)
        self.assertEqual(EXPECTED_PARSE_EMPTY_STDOUT, capture.stdout())
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_module)
    def test_gen_module_empty_dryrun(self):
        testmod = importlib.import_module('test_inputs.parse_empty')
        with Capture() as capture:
            text = gen_code.gen_module(testmod, 'tests.test_output_module', '# HEADER',
                                       verbose=True, dryrun=True, doprint=True)
        self.assertEqual(EXPECTED_PARSE_EMPTY, text)
        self.assertEqual(EXPECTED_PARSE_EMPTY_DRYRUN_STDOUT, capture.stdout())
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_module)
    def test_gen_module_empty_exception(self):
        testmod = importlib.import_module('test_inputs.parse_empty')
        with self.assertRaises(ModuleNotFoundError):
            with Capture():
                gen_code.gen_module(testmod, 'does_not_exist.whatever', '# HEADER')

    @tests(gen_code.gen_module)
    def test_gen_module_generated_exception(self):
        """Test that exception in parsed code is caught as expected"""
        testmod = importlib.import_module('test_inputs.tests')
        with Capture() as capture:
            gen_code.gen_module(testmod, 'tests.test_output_module', '# HEADER',
                                verbose=True, dryrun=True, doprint=True)
        self.assertIn('error parsing generated result', capture.stdout().lower())
        self.assertEqual('', capture.stderr())

    @tests(gen_code.gen_module)
    def test_gen_module_example(self):
        """Verify that initial generation of example output module does the right thing"""
        self.assertEqualsExampleOutput('tests.test_no_output_module')

    @tests(gen_code.gen_module)
    def test_gen_module_example_verbose(self):
        self.assertEqualsExampleOutput(
            'tests.test_output_module',
            verbose=True, stdout=EXPECTED_GEN_MODULE_EXAMPLE_VERBOSE
        )

    @tests(gen_code.gen_module)
    def test_gen_module_example_exists_verbose(self):
        self.assertEqualsExampleOutput(
            'test_inputs.output_example',
            verbose=True, stdout=EXPECTED_GEN_MODULE_EXAMPLE_EXISTS_VERBOSE
        )

    @tests(gen_code.gen_module)
    def test_gen_module_example_exists(self):
        self.assertEqualsExampleOutput('test_inputs.output_example')

    @tests(gen_code.gen_module)
    def test_gen_module_example_exists_dryrun(self):
        self.assertEqualsExampleOutput('test_inputs.output_example', dryrun=True, doprint=False)

    @tests(gen_code.gen_module)
    def test_gen_module_example_needs_additions(self):
        self.assertEqualsExampleOutput('test_inputs.output_example_adds')

    @tests(gen_code.gen_module)
    def test_gen_module_example_needs_mod_additions(self):
        self.assertEqualsExampleOutput('test_inputs.output_example_adds_mod_test')

    @tests(gen_code.gen_module)
    def test_gen_module_example_needs_new_import(self):
        self.assertEqualsExampleOutput('test_inputs.output_example_adds_new_import')

# TestFuncGenModule().test_gen_module_example_exists()
# TestFuncGenModule().test_gen_module_example_exists_verbose()
