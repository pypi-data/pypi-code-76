from unittest import TestCase
from x7.lib.annotations import tests
from x7.testing.maketests.outmap import OutputMapElem, OutputMap
from test_inputs import parse_basic
from x7.testing.support import Capture
from x7.lib import annotations
from tests.x7.testing.maketests.test_mod_support import cm


def use_stuff_to_eliminate_pylint_warnings_and_provide_test_coverage():
    return [annotations]


@tests(OutputMapElem)
class TestOutputMapElem(TestCase):
    @tests(OutputMapElem.__init__)
    @tests(OutputMapElem.__str__)
    def test_basic(self):
        self.assertRegex(str(OutputMapElem('tag', 'method', 'line-o-text\n')), r'^\s*tag\s*method\s*line-o-text\s*$')
        self.assertRegex(str(OutputMapElem(None, None, 'line-o-text\n')), r'^\s*-\s*-\s*line-o-text\s*$')
        use_stuff_to_eliminate_pylint_warnings_and_provide_test_coverage()

    @tests(OutputMapElem.extend)
    @tests(OutputMapElem.text)
    def test_extend_and_text(self):
        ome = OutputMapElem('tag', 'method', 'line-o-text\n')
        ome.extend(['other-line\n', 'last-line\n'])
        self.assertEqual('line-o-text\nother-line\nlast-line\n', ome.text())


@tests(OutputMap)
class TestOutputMap(TestCase):
    @tests(OutputMap.__init__)
    def test___init__(self):
        self.assertEqual(True, OutputMap(verbose=True).verbose)
        self.assertEqual(False, OutputMap(verbose=False).verbose)

    @tests(OutputMap.find_class_source)
    @tests(OutputMap.build)
    def test_build_verbose(self):
        """Test OutputMap.build with verbose output"""
        om = OutputMap(verbose=True)
        with Capture() as capture:
            om.build(cm(parse_basic))
        out = capture.stdout()
        lines = [
            'Class: ClassGotImported -> tests',
            '  Class: TestModExample -> tests x7.lib.annotations',
            '  Class: TestModExample2 -> tests test_inputs.parse_basic.TestModExample',
        ]
        for l in lines:
            self.assertIn(l, out)
        self.assertEqual('', capture.stderr())

    @tests(OutputMap.find_class_source)
    @tests(OutputMap.build)
    def test_build_missing(self):
        """Test OutputMap.build with non-existent module"""
        om = OutputMap(False)
        om.build('test_inputs.parse_basic_missing')
        self.assertEqual('test_inputs.parse_basic_missing', om.modname)
        self.assertEqual(om.verbose, False)
        self.assertEqual(om.debug, False)
        self.assertEqual(om.added, {})
        self.assertEqual(om.lines, [])
        self.assertEqual({}, om.tested)
        self.assertEqual({}, om.classes)
        self.assertEqual({}, om.testmap)

    @tests(OutputMap.find_class_source)
    @tests(OutputMap.build)
    def test_build(self):
        outmap = OutputMap(False)
        outmap.build(cm(parse_basic))
        self.assertEqual('test_inputs.parse_basic', outmap.modname)
        self.assertEqual(outmap.verbose, False)
        self.assertEqual(outmap.debug, False)
        self.assertEqual(outmap.added, {})
        for n, l in enumerate(outmap.lines):
            if 'THIS_LINE_IS' in l.lines[0]:
                self.assertEqual(n+1, parse_basic.THIS_LINE_IS)
                break
        else:   # pragma: no cover
            self.fail('Did not find THIS_LINE_IS in ' + parse_basic.__file__)
        self.assertEqual(
            {
                'x7.lib.annotations': 'test_inputs.parse_basic.TestModExample',
                'x7.lib.annotations.tests': 'test_tests',
                'test_inputs.example_imported': 'test_example_imported',
                'test_inputs.parse_basic.TestModExample': 'test_inputs.parse_basic.TestModExample2',
             },
            outmap.tested)

        self.assertEqual(
            {'TestModExample', 'TestModExample2'},
            set(outmap.classes.keys()))

        # Add +1 here because .START_LINE is one-based and .start is zero-based
        self.assertEqual(parse_basic.TestModExample.START_LINE, outmap.classes['TestModExample'].start+1)
        # .END_LINE is one-based and .last is zero-based, but represents last+1 already, so no +1 needed
        self.assertEqual(parse_basic.TestModExample.END_LINE, outmap.classes['TestModExample'].last)

        # print(outmap.testmap)
        # print('::'.join('%s(%s)' % (type(e).__qualname__, e) for e in outmap.testmap.keys()))
        self.assertEqual(
            {
                'x7.lib.annotations': 'TestModExample',
                'test_inputs.parse_basic.TestModExample': 'TestModExample2'
            },
            outmap.testmap)


@tests('x7.testing.maketests.outmap')
class Test0outmap(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.outmap module"""
