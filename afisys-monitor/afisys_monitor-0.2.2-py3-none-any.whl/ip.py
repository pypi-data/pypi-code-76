import argparse
import json
import urllib.request

from tabulate import tabulate

from .module import Module


class Ip(Module):
    _curr_ip = None
    _ip_info = None

    def parse_args(parser: argparse.ArgumentParser):
        parser.add_argument('-o', '--output', help='Specify output fields [default: ip city country]', action='append', default=['ip', 'city', 'country'])
        parser.add_argument('-a', '--all', help='Display all fields', action='store_true')
        return parser

    def __str__(self):
        # Check current IP with a quota-free service
        try:
            _new_ip = urllib.request.urlopen('https://wtfismyip.com/text', None, 1).read().decode()
        except Exception as e:
            return(str(e))

        # Update info if ip has changed
        if _new_ip != self._curr_ip:
            self._curr_ip = _new_ip
            _jsonData = json.loads(urllib.request.urlopen('https://ipinfo.io?token=3796117b2f73cb').read().decode())
            _out = []
            for field in _jsonData.keys():
                if field in self._args.output or self._args.all:
                    _out.append([field, str(_jsonData.get(field))])
            self._ip_info = tabulate(_out, tablefmt='plain')

        return(self._ip_info)
