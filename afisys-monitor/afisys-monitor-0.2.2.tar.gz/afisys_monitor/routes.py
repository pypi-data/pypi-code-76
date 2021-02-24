import argparse
import subprocess

from tabulate import tabulate

from .module import Module


class Routes(Module):

    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument('-c', '--columns', help='Column numbers to include', action='append')
        return parser

    def __str__(self):
        _proc = subprocess.Popen(['netstat', '-r', '-n'], stdout=subprocess.PIPE)

        if self._args.columns is not None:
            _awk_str = '{print $' + ',"\\t\\t",$'.join(self._args.columns) + '}'
            _proc = subprocess.Popen(['awk', _awk_str], stdin=_proc.stdout, stdout=subprocess.PIPE)

        _proc = subprocess.Popen(['tail', '-n+2'], stdin=_proc.stdout, stdout=subprocess.PIPE)
        
        _out = []
        for line in _proc.stdout.read().decode().split('\n'):
            _out.append(line.split())
        return(tabulate(_out, tablefmt='plain'))
