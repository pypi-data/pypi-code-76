from unittest import TestCase

from x7.testing.support import Argv, Capture
from x7.lib.annotations import tests
from x7.testing.maketests import maketests


@tests(maketests)
class TestModMaketests(TestCase):
    """Tests for stand-alone functions in x7.testing.maketests.maketests module"""

    def test_do_module(self):
        # do_module(inmod: module, outmod: str, filename: str, header: str, verbose: bool, dryrun: bool, doprint: bool, debug=False)
        pass  # TODO-impl x7.testing.maketests.maketests.do_module test

    @tests(maketests.main)
    def test_main_usage(self):
        with Capture() as capture:
            with Argv(['maketests']):
                maketests.main()
        self.assertIn('Usage: maketests', capture.stdout())
        self.assertEqual('', capture.stderr())

    @tests(maketests.do_module)
    @tests(maketests.single_module)
    @tests(maketests.main)
    def test_main_single(self):
        with Capture() as capture:
            with Argv(['maketests', '-n', '-v', '-p', 'test_inputs.parse_empty']):
                maketests.main()
        lines = [
            'Input: test_inputs.parse_empty',
            'class TestModParseEmpty(TestCase):',
        ]
        for line in lines:
            self.assertIn(line, capture.stdout())
        self.assertNotIn('error', capture.stdout().lower())
        self.assertEqual('', capture.stderr())
