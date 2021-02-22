"""
    DigiCloud Network Service.
"""
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate


class ListNetwork(Lister):
    """List networks"""

    def take_action(self, parsed_args):
        data = self.app.session.get('/networks')

        return tabulate(data)


class ShowNetwork(ShowOne):
    """Show network details."""

    def get_parser(self, prog_name):
        parser = super(ShowNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        data = self.app.session.get(uri)

        return tabulate(data)


class DeleteNetwork(Command):
    """Delete network."""

    def get_parser(self, prog_name):
        parser = super(DeleteNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        self.app.session.delete(uri)


class UpdateNetwork(ShowOne):
    """Update network."""
    def get_parser(self, prog_name):
        parser = super(UpdateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network ID',
        )
        parser.add_argument(
            '--name',
            metavar='<Name>',
            help='New name for network.'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<Description>',
            help='New admin state.'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s' % parsed_args.network
        payload = {k: getattr(parsed_args, k) for k in ('name', 'admin_state')
                   if getattr(parsed_args, k) is not None}
        data = self.app.session.patch(uri, payload)
        return tabulate(data)


class CreateNetwork(ShowOne):
    """Create Network"""

    def get_parser(self, prog_name):
        parser = super(CreateNetwork, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Network name'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            default='UP',
            help='Set admin state (default UP).'
        )
        return parser

    def take_action(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'admin_state': parsed_args.admin_state
        }
        data = self.app.session.post('/networks', payload)
        return tabulate(data)


class ListNetworkPorts(Lister):
    """List all ports of Network"""
    def get_parser(self, prog_name):
        parser = super(ListNetworkPorts, self).get_parser(prog_name)

        parser.add_argument(
            'network',
            metavar='<network>',
            help='Network name or ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = f'/networks/{parsed_args.network}/ports'
        data = self.app.session.get(uri)

        return tabulate(data)
