import argparse
import json
import subprocess

import humanfriendly
from tabulate import tabulate
from termcolor import colored

from .module import Module


class Lxc(Module):
    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument(
            '-c',
            '--columns',
            help='columns (default: nPL). See lxc list -h for details',
            default='nPL',
        )
        return parser

    def __str__(self):
        _proc = subprocess.Popen(
            ['lxc', 'list', '--format', 'json'], stdout=subprocess.PIPE
        )
        _json = json.loads(_proc.stdout.read().decode())
        #
        _out = []
        for _item in _json:
            _ipv4 = []
            _ipv6 = []
            _storages = []
            _disk_usage = 0
            _memory = ''
            _snapshots = 0
            _cputime = 0
            _profiles = []
            if '4' in self._args.columns or '6' in self._args.columns:
                try:
                    for _dev in _item.get('state').get('network').items():
                        if _dev[0] == 'lo':
                            continue
                        for _addr in _dev[1]['addresses']:
                            if _addr['family'] == 'inet':
                                _ipv4.append(
                                    '%s (%s)' % (_addr.get('address'), _dev[0])
                                )
                            if _addr['family'] == 'inet6':
                                _ipv6.append(
                                    '%s (%s)' % (_addr.get('address'), _dev[0])
                                )
                except Exception:
                    pass

            if 'b' in self._args.columns:
                try:
                    for _device in _item.get('expanded_devices').items():
                        if _device[1]['type'] == 'disk':
                            _storages.append(_device[1]['pool'])
                except Exception:
                    pass

            if 'P' in self._args.columns:
                try:
                    for _profile in _item.get('profiles'):
                        if _profile != 'default':
                            _profiles.append(_profile)
                except Exception:
                    pass
            if 'D' in self._args.columns:
                try:
                    for _disk in _item.get('state').get('disk').items():
                        _disk_usage = _disk_usage + _disk[1]['usage']
                except Exception:
                    pass

            if 'm' in self._args.columns:
                _memory = _item.get('state').get('memory').get('usage')
                _memory = '' if _memory == 0 else humanfriendly.format_size(_memory)

            if 'S' in self._args.columns:
                try:
                    _snapshots = len(_item.get('snapshots'))
                except Exception:
                    pass
                _snapshots = '' if _snapshots == 0 else _snapshots

            if 'u' in self._args.columns:
                try:
                    _cputime = '%ss' % int(
                        _item.get('state').get('cpu')['usage'] / 1000000000
                    )
                except Exception:
                    pass

            # Color code the name by status
            _colors = {'Stopped': 'yellow', 'Running': 'green'}

            _columns = {
                '4': '\n'.join(_ipv4),
                '6': '\n'.join(_ipv6),
                'a': _item.get('architecture'),
                'b': '\n'.join(_storages),
                'c': _item.get('created_at')[0:16],
                'd': _item.get('description'),
                'D': humanfriendly.format_size(_disk_usage),
                'l': _item.get('last_used_at')[0:16],
                'm': _memory,
                #                M - Memory usage (%)
                'n': colored(
                    _item.get('name'), _colors.get(_item.get('status'), 'red')
                ),
                'N': _item.get('state').get('processes'),
                'p': _item.get('state').get('pid'),
                'P': '\n'.join(_profiles),
                's': _item.get('status'),
                'S': _snapshots,
                't': 'ephemeral' if _item.get('ephemeral') == True else 'persistent',
                'u': _cputime,
                'L': _item.get('location'),
                'f': _item.get('expanded_config').get('volatile.base_image')[0:12],
                'F': _item.get('expanded_config').get('volatile.base_image'),
            }

            _line = []
            for _col in self._args.columns:
                _line.append(_columns.get(_col))

            _out.append(_line)

        return tabulate(_out, tablefmt='plain')
