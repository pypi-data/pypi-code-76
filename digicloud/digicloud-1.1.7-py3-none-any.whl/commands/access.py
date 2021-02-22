"""
    DigiCloud Access Service.
"""
from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command

from ..utils import tabulate


class ListFloatingIp(Lister):
    """List floating Ips."""

    def take_action(self, parsed_args):
        uri = '/floating-ips'
        data = self.app.session.get(uri)

        return tabulate(data)


class ShowFloatingIp(ShowOne):
    """Show floating Ip details."""

    def get_parser(self, prog_name):
        parser = super(ShowFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip',
            metavar='<floating_ip>',
            help=('Floating IP ID'),
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/floating-ips/%s' % parsed_args.floating_ip
        data = self.app.session.get(uri)

        return tabulate(data)


class CreateFloatingIp(ShowOne):
    """Create Floating Ip."""
    def take_action(self, parsed_args):
        data = self.app.session.post('/floating-ips', {})

        return tabulate(data)


class DeleteFloatingIp(Command):
    """Delete Floating Ip."""

    def get_parser(self, prog_name):
        parser = super(DeleteFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip',
            metavar='<floating_ip>',
            help=('Floating IP ID')
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/floating-ips/%s' % parsed_args.floating_ip
        self.app.session.delete(uri)


class AssociateFloatingIp(ShowOne):
    """Associate Floating Ip."""

    def get_parser(self, prog_name):
        parser = super(AssociateFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip_id',
            metavar='<floating_ip_id>',
            help='Floating IP ID'
        )
        parser.add_argument(
            '--interface-id',
            metavar='<interface_id>',
            required=True,
            help='Interface ID'
        )
        return parser

    def take_action(self, parsed_args):
        payload = {
            'interface_id': parsed_args.interface_id,
        }
        uri = '/floating-ips/%s/associate' % parsed_args.floating_ip_id
        data = self.app.session.post(uri, payload)
        return tabulate(data)


class RevokeFloatingIp(ShowOne):
    """Revoke Floating Ip."""

    def get_parser(self, prog_name):
        parser = super(RevokeFloatingIp, self).get_parser(prog_name)
        parser.add_argument(
            'floating_ip_id',
            metavar='<floating_ip_id>',
            help='Floating IP ID'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/floating-ips/%s/revoke' % parsed_args.floating_ip_id
        data = self.app.session.post(uri, {})
        return tabulate(data)
