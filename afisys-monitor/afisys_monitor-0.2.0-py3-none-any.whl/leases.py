import argparse
import subprocess

from .module import Module


class Leases(Module):

    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument('-s', '--short', help='Skip HW address and show only ip address and hostname', action='store_true')
        return parser

    def __str__(self):
        leases = subprocess.Popen(['cat', '/var/lib/misc/dnsmasq.leases'], stdout=subprocess.PIPE)
        if self._args.short:
            leases = subprocess.Popen(['cut', '-d', ' ', '-f', '3,4'], stdin=leases.stdout, stdout=subprocess.PIPE)
        else:
            leases = subprocess.Popen(['cut', '-d', ' ', '-f', '2-4'], stdin=leases.stdout, stdout=subprocess.PIPE)

        return(leases.stdout.read().decode())
