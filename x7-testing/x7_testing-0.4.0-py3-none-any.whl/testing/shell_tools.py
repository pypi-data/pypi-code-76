"""
    Shell tools for x7.testing

    Usage: from x7.shell import *
"""

__all__ = ['maketests']

import _sitebuiltins
_sitebuiltins.Quitter


def maketests(module=None, really=False, force=False):
    """Generate/update tests for python module"""
    import sys
    import x7.testing.maketests.maketests as maketests_mod

    if not module:
        print('Help: maketests(module-name, really=False, force=False)')
        print('Example: maketests("x7.sample.needs_test", True)')
    else:
        saved = sys.argv[:]
        try:
            sys.argv = ['--verbose', '--verbose']
            if not really:
                sys.argv.append('--dry-run')
            if force:
                sys.argv.append('--force')
            sys.argv.append(module)
            print('Maketests: argv=', sys.argv)
            maketests_mod.main()
        finally:
            sys.argv = saved
