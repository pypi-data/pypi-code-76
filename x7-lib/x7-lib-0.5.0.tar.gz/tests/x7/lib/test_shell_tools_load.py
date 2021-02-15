# Originally auto-generated on 2021-02-15-12:14:41 -0500 EST
# By '--verbose --verbose x7.lib.shell_tools_load'

from unittest import TestCase

from x7.testing.support import Capture

from x7.lib.annotations import tests
from x7.lib import shell_tools_load
from x7.lib.shell_tools_load import ShellTool


def func():
    """Func Doc"""
    print('func called')


@tests(shell_tools_load.ShellTool)
class TestShellTool(TestCase):
    @tests(shell_tools_load.ShellTool.__init__)
    @tests(shell_tools_load.ShellTool.__repr__)
    @tests(shell_tools_load.ShellTool.doc)
    @tests(shell_tools_load.ShellTool.__call__)
    def test_init(self):
        st = ShellTool('func', func)
        self.assertEqual('func - Func Doc: use func() to invoke', repr(st))
        with Capture() as out:
            st()
        self.assertEqual('func called', out.stdout())
        self.assertEqual('Func Doc', st.doc())


@tests(shell_tools_load)
class TestModShellToolsLoad(TestCase):
    """Tests for stand-alone functions in x7.lib.shell_tools_load module"""

    @tests(shell_tools_load.load_tools)
    def test_load_tools(self):
        found = dict()
        with Capture() as ignore:
            shell_tools_load.load_tools(found)
        self.assertIn('Dir', found)
        self.assertIn('maketests', found)
