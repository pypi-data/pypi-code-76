"""
    DigiCloud Compute Instance Service.
"""
import os

from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from ..utils import tabulate


class CreateSSHKey(ShowOne):
    """Create new public or private key for server ssh access."""

    def get_parser(self, prog_name):
        parser = super(CreateSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='New public or private key name'
        )
        parser.add_argument(
            '--public-key',
            metavar='<file>',
            required=True,
            help='Filename for public key to add. If not used,'
                 ' creates a private key.'
        )
        return parser

    def take_action(self, parsed_args):
        key_path = os.path.expanduser(parsed_args.public_key)
        try:
            with open(key_path) as file_:
                public_key = file_.read()
        except IOError as exc:
            raise Exception(f'Key file {parsed_args.public_key} not found: {exc}')

        payload = {
            'name': parsed_args.name,
            'public_key': public_key or '',
        }

        data = self.app.session.post('/ssh-keys', payload)

        return tabulate(data)


class ListSSHKey(Lister):
    """List ssh_keys."""

    def take_action(self, parsed_args):
        data = self.app.session.get('/ssh-keys')

        return tabulate(data)


class ShowSSHKey(ShowOne):
    """Show ssh_key detail"""

    def get_parser(self, prog_name):
        parser = super(ShowSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'ssh_key',
            metavar='<ssh_key>',
            help=('SSH key Name'),
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/ssh-keys/%s' % parsed_args.ssh_key
        data = self.app.session.get(uri)

        return tabulate(data)


class DeleteSSHKey(Command):
    """Delete SSHKey."""

    def get_parser(self, prog_name):
        parser = super(DeleteSSHKey, self).get_parser(prog_name)
        parser.add_argument(
            'ssh_key',
            metavar='<ssh_key>',
            help=('SSH Key Name')
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/ssh-keys/%s' % parsed_args.ssh_key
        self.app.session.delete(uri)
