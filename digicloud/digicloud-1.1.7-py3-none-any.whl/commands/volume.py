"""
    DigiCloud Volume Service.
"""
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate, is_tty


class ListVolume(Lister):
    """List volumes."""

    def take_action(self, parsed_args):
        data = self.app.session.get('/volumes')

        return tabulate(data)


class ShowVolume(ShowOne):
    """Show volume details."""

    def get_parser(self, prog_name):
        parser = super(ShowVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/volumes/%s' % parsed_args.volume
        data = self.app.session.get(uri)

        return tabulate(data)


class DeleteVolume(Command):
    """Delete volume."""

    def get_parser(self, prog_name):
        parser = super(DeleteVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help='Volume name or ID'
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        if not self.confirm(parsed_args):
            return
        uri = '/volumes/%s' % parsed_args.volume
        self.app.session.delete(uri)

    def confirm(self, parsed_args):
        if parsed_args.i_am_sure:
            return True
        if is_tty():
            volume = self.app.session.get('/volumes/%s' % parsed_args.volume)
            user_response = input(
                "You're about to delete a volume named {} with {}GB size. "
                "Are you sure? [yes/no]".format(
                    volume['name'],
                    volume['size']
                ))
            if user_response == "yes":
                return True
            self.app.stdout.write("Operation cancelled by user\n")
        else:
            self.app.stderr.write("Unable to perform 'delete volume' operation in non-interactive mode,"
                                  " without '--i-am-sure' switch\n")
            return False


class CreateVolume(ShowOne):
    """Create Volume."""

    def get_parser(self, prog_name):
        parser = super(CreateVolume, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Volume name'
        )
        parser.add_argument(
            '--size',
            required=True,
            metavar='<size>',
            help='Volume size'
        )

        parser.add_argument(
            '--type',
            required=True,
            metavar='<type>',
            help='Volume type, could be SSD or ULTRA-DISK',
            choices=['SSD', 'ULTRA-DISK']
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help='Volume description'
        )

        return parser

    def take_action(self, parsed_args):
        volume_type = parsed_args.type.upper()
        payload = {
            'name': parsed_args.name,
            'size': parsed_args.size,
            'volume_type': volume_type
        }
        if parsed_args.description:
            payload['description'] = parsed_args.description

        data = self.app.session.post('/volumes', payload)

        return tabulate(data)


class UpdateVolume(ShowOne):
    """Update volume."""
    def get_parser(self, prog_name):
        parser = super(UpdateVolume, self).get_parser(prog_name)
        parser.add_argument(
            'volume',
            metavar='<volume>',
            help=('Volume name or ID'),
        )
        parser.add_argument(
            '--name',
            required=False,
            metavar='<name>',
            help='new name for the volume, should be unique',
        )
        parser.add_argument(
            '--description',
            required=False,
            metavar='<description>',
            help='Volume description'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/volumes/%s' % parsed_args.volume
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        if not payload:
            raise Exception("At least one of --name or --description is necessary")
        data = self.app.session.patch(uri, payload)

        return tabulate(data)
