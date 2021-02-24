import argparse
from importlib import import_module
from time import sleep

import afisys_monitor
from reprint import output

from .module import modules


class Monitor:
    running_module = None

    def __init__(self):
        self._parse_args()

    def __str__(self):
        return 'Monitor class'

    def _parse_args(self):
        _parser = argparse.ArgumentParser()
        _parser.add_argument('-b', '--batch', help='batch mode - only print values once and exit (default: continuous)', action='store_true')
        _parser.add_argument('-i', '--interval', help='interval between updates in milliseconds (default: 1000)', type=int, default=1000)
        _parser.add_argument('-f', '--filter', help='filter output', action='store')
        _parser.add_argument('-V', '--version', help='display version', action='store_true')
        _subs = _parser.add_subparsers(title='modules', help='module', description='Type <module> -h for more help')

        # Add subparsers for each module
        for _module in modules:
            # Create the subparser
            _sub_parser = _subs.add_parser(_module)
            _sub_parser.set_defaults(module=_module, class_name=modules[_module])
            # Import the module
            _module_name = import_module('afisys_monitor.%s' % (_module))
            _module_class = getattr(_module_name, modules.get(_module))
            # Get the module to add it's parameters to the subparser
            _sub_parser = _module_class.parse_args(_sub_parser)

        # Parse arguments
        self._args = _parser.parse_args()

        # Check if a module was given
        if hasattr(self._args, 'module'):
            _module = import_module('afisys_monitor.%s' % (self._args.module))
            _module_instance = getattr(_module, modules.get(self._args.module))(self._args)

            # Print once if batch mode was selected
            if self._args.batch:
                print(self._apply_filters(str(_module_instance)))

            # Print contiuously
            else:
                # Get first sample to determine number of lines
                _output_lines = self._apply_filters(str(_module_instance)).split('\n')
                with output(output_type='list', initial_len=len(_output_lines), interval=self._args.interval) as _output_lines:
                    while True:
                        i = 0
                        # Update _output_lines one line at a time
                        # (If the whole object is replaced, it will not output)
                        for line in self._apply_filters(str(_module_instance)).split('\n'):
                            _output_lines[i] = line
                            i = i + 1
                        sleep(self._args.interval / 1000)

        # No module was given: show help message
        else:
            # Show version
            if self._args.version:
                print(afisys_monitor.__version__)
            else:
                _parser.print_help()

    def _apply_filters(self, str):
        if self._args.filter is not None:
            _output_lines = ''
            for line in str.split('\n'):
                if self._args.filter not in line:
                    continue
                _output_lines = _output_lines + line + '\n'
        else:
            _output_lines = str

        return _output_lines
