"""
    DigiCloud InstanceTypes Service.
"""
from cliff.lister import Lister
from cliff.show import ShowOne

from .. import formatter
from ..utils import tabulate


class ListInstanceType(Lister):
    """List instance-types."""

    def get_parser(self, prog_name):
        parser = super(ListInstanceType, self).get_parser(prog_name)
        parser.add_argument(
            '--family',
            metavar='<family>',
            help='Filter by family',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/instance-types'
        if parsed_args.family:
            uri = '/instance-types?family=%s' % parsed_args.family
        data = self.app.session.get(uri)

        for instance in data:
            instance['ram'] = formatter.format_ram(instance['ram'])

        return tabulate(data)


class ShowInstanceType(ShowOne):
    """Show instance-type details."""

    def get_parser(self, prog_name):
        parser = super(ShowInstanceType, self).get_parser(prog_name)
        parser.add_argument(
            'instance_type',
            metavar='<instance type>',
            help='InstanceType name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = f'/instance-types/{parsed_args.instance_type}'
        data = self.app.session.get(uri)

        data['ram'] = formatter.format_ram(data['ram'])

        return tabulate(data)
