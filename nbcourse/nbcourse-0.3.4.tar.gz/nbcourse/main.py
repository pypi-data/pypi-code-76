"""
Build a small website to host Jupyter notebooks as course chapters
"""

import argparse
from .nbcourse import NbCourse, DEFAULT_CONFIG_FILE
from .initialize import initialize
from pathlib import Path
from .mydoit import MyDoitHelp, ClassTaskLoader


def get_help_epilog() -> str:
    """Instanciate a minimal nbcourse to return help string"""
    course = NbCourse()
    loader = ClassTaskLoader(course)
    return MyDoitHelp(task_loader=loader).get_help()


def main():
    """CLI for nbcourse"""

    prog = globals()['__package__']
    description = globals()['__doc__']
    formatter = argparse.RawDescriptionHelpFormatter
    epilog = get_help_epilog()

    parser = argparse.ArgumentParser(prog=prog,
                                     description=description,
                                     formatter_class=formatter,
                                     epilog=epilog)
    init = parser.add_argument_group('initialize')
    init.add_argument('--init', action='store_true',
                      help=initialize.__doc__)
    generate = parser.add_argument_group('generate')
    generate.add_argument('--config', dest='config_file', type=Path,
                          default=DEFAULT_CONFIG_FILE,
                          help='Load YAML file describing site configuration '
                               '(default: %(default)s)')

    parser.add_argument('--verbosity', '-v', type=str, )
    # Handle undefined arguments
    parsed, extra = parser.parse_known_args()

    if parsed.init:
        initialize()
    else:
        course = NbCourse(parsed.config_file)
        course.build(extra)
