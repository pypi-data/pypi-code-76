# Originally auto-generated on 2021-02-15-12:14:36 -0500 EST
# By '--verbose --verbose x7.lib.shell_tools'

from unittest import TestCase
from x7.lib.annotations import tests
from x7.testing.support import Capture
from x7.lib import shell_tools
from x7.lib.shell_tools_load import ShellTool


@tests(shell_tools)
class TestModShellTools(TestCase):
    """Tests for stand-alone functions in x7.lib.shell_tools module"""

    @tests(shell_tools.Dir)
    def test_dir(self):
        self.assertIn('__init__', dir(self))
        self.assertNotIn('__init__', shell_tools.Dir(self))
        self.assertIn('test_dir', shell_tools.Dir(self))

    @tests(shell_tools.help)
    def test_help(self):
        with Capture() as orig:
            help(shell_tools.Dir)
        with Capture() as modified:
            shell_tools.help(shell_tools.Dir)
        self.assertEqual(orig.stdout(), modified.stdout())
        self.assertIn('Like dir(v), but only non __ names', orig.stdout())
        st_dir = ShellTool('Dir', shell_tools.Dir)
        with Capture() as as_shell_tool:
            shell_tools.help(st_dir)
        self.assertEqual(orig.stdout(), as_shell_tool.stdout())
        self.assertNotIn('__init__', as_shell_tool.stdout())
        with Capture() as orig_as_shell_tool:
            help(st_dir)
        self.assertIn('__init__', orig_as_shell_tool.stdout())

    @tests(shell_tools.help)
    def test_help_on_help(self):
        with Capture() as orig:
            help(help)
        with Capture() as modified:
            shell_tools.help(ShellTool('help', shell_tools.help))
        self.assertEqual(orig.stdout(), modified.stdout())

    @tests(shell_tools.tools)
    def test_tools(self):
        with Capture() as out:
            shell_tools.tools()
        self.assertIn('Help for tools', out.stdout())
        self.assertGreaterEqual(out.stdout().count('\n'), 5)
