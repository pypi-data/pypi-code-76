import argparse
import json
import subprocess

from tabulate import tabulate
from termcolor import colored

from .module import Module


class Lxd(Module):

    def parse_args(parser: argparse.ArgumentParser):
        return parser

    def __str__(self):
        _proc = subprocess.Popen(['lxc', 'cluster', 'list', '--format', 'json'], stdout=subprocess.PIPE)
        _json = json.loads(_proc.stdout.read().decode())

        _out = []
        for _item in _json:
            _name = ''
            _status = ''
            _db = ''
            for _field in _item.keys():
                if _field == 'server_name':
                    _name = _item.get(_field)
                if _field == 'status':
                    _status = _item.get(_field)
                if _field == 'database':
                    _db = _item.get(_field)

            _colors = {
                'Offline': 'red',
                'Online': 'green'
            }

            _out.append([
                colored(_name, _colors.get(_status, 'red')),
                'D' if _db else ''
            ])

        return(tabulate(_out, tablefmt='plain'))
