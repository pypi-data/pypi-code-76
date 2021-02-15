#! /usr/bin/env python3

"""
Make unit test stubs

Usage: maketests src.module [test.module]
"""

import os
import sys
import time
import optparse
import importlib
import textwrap
from typing import List  # , Set, List, Union

from x7.testing.maketests.gen_code import gen_module
from x7.testing.maketests.mod_support import locate_output, is_package, Module
from x7.testing.maketests.types import OptParseValues


def do_module(inmod: Module, outmod: str, filename: str, header: str,
              verbose: bool, dryrun: bool, doprint: bool, debug=False):
    text = gen_module(inmod, outmod, header, verbose, dryrun, doprint, debug)

    if not dryrun:      # pragma: no cover
        print('Output to %s (%d bytes)' % (filename, len(text)))
        with open(filename, 'wt') as f:
            f.write(text)


def main():
    usage = '''
      usage: %prog [options] src.module...
    '''
    usage = textwrap.dedent(usage.strip('\n'))
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-d", "--debug",   action="store_true", dest="debug",   default=False, help="print debugging information (implies --verbose)")
    parser.add_option("-f", "--force",   action="store_true", dest="force",   default=False, help="force overwrite of output module")
    parser.add_option("-n", "--dry-run", action="store_true", dest="dryrun",  default=False, help="print what would happen, but don't change")
    parser.add_option("-o", "--output",  action="store_true", dest="output",  default=None,  help="set output root")
    parser.add_option("-p", "--print",   action="store_true", dest="print",   default=False, help="print resultant file to stdout")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="make lots of noise")
    opts, args = parser.parse_args()    # type: OptParseValues, List[str]
    if opts.debug:      # pragma: no cover
        opts.verbose = True
    if not args:
        parser.print_help()
        return

    for arg in args:
        try:
            arg_module = importlib.import_module(arg)
        except Exception as err:
            print(type(err), err)
            raise
        if is_package(arg_module):
            print("Can't process whole module yet @", arg)
            return
        else:
            single_module(arg_module, opts)


def single_module(input_module: Module, opts: OptParseValues):
    header = '# Originally auto-generated on %s\n' % time.strftime('%Y-%m-%d-%H:%M:%S %z %Z')
    header += '# By %r' % ' '.join(sys.argv).replace('\\', '/')

    output_name, output_module_name = locate_output(input_module)
    output_exists = os.path.exists(output_name)
    if opts.verbose:
        print('Input: %s' % input_module.__name__)
        print('Output: %s (%s) [%s]' % (output_module_name, output_name, 'exists' if output_exists else 'new'))
        print('Options: %s' % opts)
        if opts.debug:      # pragma: no cover
            single_line = True
            if single_line:
                print('Path:', ' '.join(p.replace('\\', '/') for p in sys.path))
            else:
                print('Path:')
                print('    ' + '\n    '.join(p.replace('\\', '/') for p in sys.path))

    if opts.print:
        opts.dryrun = True
    if output_exists:
        if not opts.dryrun and not opts.force:      # pragma: no cover
            print('Error: %s exists' % output_name)
            return

    do_module(input_module, output_module_name, output_name, header=header,
              verbose=opts.verbose, dryrun=opts.dryrun, doprint=opts.print, debug=opts.debug)


if __name__ == '__main__':      # pragma: no cover
    main()
