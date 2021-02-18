import argparse

modules = {
    'ip': 'Ip',
    'sensors': 'Sensors',
    'leases': 'Leases',
    'resolve': 'Resolve',
    'routes': 'Routes',
    'interfaces': 'Interfaces',
    'lxc': 'Lxc',
    'lxd': 'Lxd'
}


class Module:
    def __init__(self, args):
        self._args = args
        self._name = modules.get(args.module)

    def __str__(self):
        return '%s module\nParameters: %s' % (self._name, self._args)

    @staticmethod
    def parse_args(parser: argparse.ArgumentParser):
        return parser
