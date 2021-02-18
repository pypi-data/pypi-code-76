import argparse
import subprocess

from tabulate import tabulate

from .module import Module


class Sensors(Module):
    @staticmethod
    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument('-c', '--chip', help='specify sensor chip', action='append')
        return parser

    def __str__(self):
        if self._args.chip is not None:
            proc = subprocess.Popen(
                ['sensors'] + self._args.chip, stdout=subprocess.PIPE
            )
        else:
            proc = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)

        # Filter output
        _out = []
        for line in proc.stdout.read().decode().split('\n'):
            # Only keep lines with ° symbol
            if '°' not in line:
                continue

            # Keep only what we want, and trim multiple spaces
            _out.append((line.split('°')[0] + '°C').split())

        return(tabulate(_out, tablefmt='plain'))
