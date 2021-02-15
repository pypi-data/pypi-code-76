# Originally auto-generated on 2021-02-15-12:14:48 -0500 EST
# By '--verbose --verbose x7.shell'

from unittest import TestCase
from x7.lib.annotations import tests
from x7.testing.support import Capture
with Capture() as ignored:
    from x7 import shell


@tests(shell)
class TestModShell(TestCase):
    """Tests for stand-alone functions in x7.shell module"""

    def test_shell(self):
        self.assertIn('Dir', dir(shell))
        self.assertIn('tools', dir(shell))
        self.assertIn('pp', dir(shell))
