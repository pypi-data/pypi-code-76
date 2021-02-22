"""
    DigiCloud Router Service.
"""
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate


class ListRouter(Lister):
    """List Routers."""

    def take_action(self, parsed_args):
        data = self.app.session.get('/routers')

        return tabulate(data)


class ShowRouter(ShowOne):
    """Show Router details."""

    def get_parser(self, prog_name):
        parser = super(ShowRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        data = self.app.session.get(uri)

        return tabulate(data)


class DeleteRouter(Command):
    """Delete router."""

    def get_parser(self, prog_name):
        parser = super(DeleteRouter, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        self.app.session.delete(uri)


class CreateRouter(ShowOne):
    """Create Router."""

    def get_parser(self, prog_name):
        parser = super(CreateRouter, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Router name'
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
        data = self.app.session.post('/routers', payload)
        return tabulate(data)


class ListRouterInterface(Lister):
    """List all router interfaces"""

    def get_parser(self, prog_name):
        parser = super(ListRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = f'/routers/{parsed_args.router}/interfaces'
        data = self.app.session.get(uri)
        return tabulate(data)


class ShowRouterInterface(ShowOne):
    """Show router interface."""
    def get_parser(self, prog_name):
        parser = super(ShowRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface_id>',
            help='Interface ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/interfaces/%s' % (parsed_args.router, parsed_args.interface_id)
        data = self.app.session.get(uri)

        return tabulate(data)


class AddRouterInterface(ShowOne):
    """Add router interface."""

    def get_parser(self, prog_name):
        parser = super(AddRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--subnet',
            required=True,
            metavar='<subnet>',
            help='Subnet name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/interfaces' % parsed_args.router
        payload = {'subnet': parsed_args.subnet}
        data = self.app.session.post(uri, payload)

        return tabulate(data)


class RemoveRouterInterface(Command):
    """Remove router interface."""
    def get_parser(self, prog_name):
        parser = super(RemoveRouterInterface, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--interface-id',
            required=True,
            metavar='<interface_id>',
            help='Interface ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/interfaces/%s' % (parsed_args.router, parsed_args.interface_id)
        self.app.session.delete(uri)


class AddRouterExternal(ShowOne):
    """Add external network to router."""

    def get_parser(self, prog_name):
        parser = super(AddRouterExternal, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        payload = {'has_gateway': True}
        data = self.app.session.patch(uri, payload)
        return tabulate(data)


class RemoveRouterExternal(ShowOne):
    """Remove external network from router."""

    def get_parser(self, prog_name):
        parser = super(RemoveRouterExternal, self).get_parser(prog_name)
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s' % parsed_args.router
        payload = {'has_gateway': False}
        data = self.app.session.patch(uri, payload)
        return tabulate(data)


class UpdateRouter(ShowOne):
    _description = "Update Router"

    def get_parser(self, prog_name):
        parser = super(UpdateRouter, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()
        parser.add_argument(
            'router',
            metavar='<router>',
            help='Router name or ID'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='New name for the router'
        )
        parser.add_argument(
            '--admin-state',
            metavar='<AdminState>',
            help='Set admin state.'
        )
        group.add_argument(
            '--disable-gateway',
            help='Disconnect router from external network',
            action='store_true'

        )
        group.add_argument(
            '--enable-gateway',
            help='Connect router to external network',
            action='store_true'
        )
        return parser

    def take_action(self, parsed_args):
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.disable_gateway:
            payload['has_gateway'] = False
        if parsed_args.enable_gateway:
            payload['has_gateway'] = True
        if parsed_args.admin_state:
            payload['admin_state'] = parsed_args.admin_state
        if len(payload) == 0:
            raise Exception("You need to at least provide one of --name, --enable-gateway or --disable-gateway")
        uri = '/routers/%s' % parsed_args.router
        data = self.app.session.patch(uri, payload)
        return tabulate(data)


class ListRouterStatic(Lister):
    """List router static routes."""
    def get_parser(self, prog_name):
        parser = super(ListRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        data = self.app.session.get(uri)
        return tabulate(data)


class AddRouterStatic(Lister):
    """Add router static routes."""
    def get_parser(self, prog_name):
        parser = super(AddRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        parser.add_argument(
            '--destination',
            metavar='<Network>',
            required=True,
            help='Destination network.'
        )
        parser.add_argument(
            '--nexthop',
            metavar='<IP address>',
            required=True,
            help='Next hop IP address.'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        payload = {
            "destination": parsed_args.destination,
            "nexthop": parsed_args.nexthop,

        }
        data = self.app.session.post(uri, payload)
        return tabulate(data)


class DeleteRouterStatic(Lister):
    """Delete static routes."""
    def get_parser(self, prog_name):
        parser = super(DeleteRouterStatic, self).get_parser(prog_name)
        parser.add_argument(
            'router_id',
            metavar='<router_id>',
            help='Router ID'
        )
        parser.add_argument(
            '--destination',
            metavar='<Network>',
            required=True,
            help='Destination network.'
        )
        parser.add_argument(
            '--nexthop',
            metavar='<IP address>',
            required=True,
            help='Next hop IP address.'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/routers/%s/static-routes' % parsed_args.router_id
        payload = {
            "destination": parsed_args.destination,
            "nexthop": parsed_args.nexthop,

        }
        data = self.app.session.delete(uri, payload)
        return tabulate(data)
