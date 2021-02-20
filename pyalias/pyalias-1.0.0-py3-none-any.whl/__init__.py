from collections import OrderedDict
import os
from pathlib import Path
import re
import sys
import yaml


class Alias:
    DEFAULT_CONFIG = Path('~/.config/pyalias.yaml').expanduser()

    def __init__(self, config_file=None):
        self.alias_map = self.load_config(config_file)

    def load_config(self, config_file):
        if not config_file:
            config_file = os.environ.get('PYALIAS_CONF', self.DEFAULT_CONFIG)
        with open(config_file) as f:
            config = yaml.safe_load(f)
        alias_map = OrderedDict()
        for item in config:
            d = {
                'name': re.sub(r'\s+', '', item['name']),
                'command': item['command'],
                'description': item.get('description', '')
            }
            alias_map[d['name']] = d
        return alias_map

    def list(self):
        output = ''
        for alias in self.alias_map.values():
            name = alias['name']
            description = alias['description']
            output += f'* [{name}] {description}\n'
        sys.stdout.write(output)

    def main(self):
        try:
            command = sys.argv[1]
        except IndexError:
            command = 'list'
        func = getattr(self, command, None)
        if callable(func):
            return func()
        try:
            alias = self.alias_map[command]
            os.system(alias['command'])
        except KeyError:
            sys.stderr.write(f'unknown command: {command}')
