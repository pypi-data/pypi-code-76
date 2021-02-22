"""
    DigiCloud Security Service.
"""
from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate


class ListSecurityGroup(Lister):
    """List Security Groups."""

    def take_action(self, parsed_args):
        data = self.app.session.get('/security-groups')

        return tabulate(data)


class ShowSecurityGroup(ShowOne):
    """Show security group details."""

    def get_parser(self, prog_name):
        parser = super(ShowSecurityGroup, self).get_parser(prog_name)
        parser.add_argument(
            'security_group',
            metavar='<security_group>',
            help='Security group name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/%s' % parsed_args.security_group
        data = self.app.session.get(uri)

        return tabulate(data)


class CreateSecurityGroup(ShowOne):
    """Create Security Group."""

    def get_parser(self, prog_name):
        parser = super(CreateSecurityGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Security group name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            default="",
            required=False,
            help='Security group name'
        )

        return parser

    def take_action(self, parsed_args):
        payload = {'name': parsed_args.name, 'description': parsed_args.description}
        data = self.app.session.post('/security-groups', payload)

        return tabulate(data)


class DeleteSecurityGroup(Command):
    """Delete Security Group."""

    def get_parser(self, prog_name):
        parser = super(DeleteSecurityGroup, self).get_parser(prog_name)
        parser.add_argument(
            'security_group',
            metavar='<security_group>',
            help='Security group name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/%s' % parsed_args.security_group
        self.app.session.delete(uri)


class UpdateSecurityGroup(Command):
    """Update Security Group."""

    def get_parser(self, prog_name):
        parser = super(UpdateSecurityGroup, self).get_parser(prog_name)
        parser.add_argument(
            'security_group',
            metavar='<security_group>',
            help='Security group name or ID'
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            required=False,
            help='Security group name'
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            required=False,
            help='Security group name'
        )
        return parser

    def take_action(self, parsed_args):
        uri = f'/security-groups/{parsed_args.security_group}'
        payload = {}
        if parsed_args.name:
            payload['name'] = parsed_args.name
        if parsed_args.description:
            payload['description'] = parsed_args.description
        self.app.session.patch(uri, payload)


class ListSecurityGroupRule(Lister):
    """List Security Group Rules."""

    def get_parser(self, prog_name):
        parser = super(ListSecurityGroupRule, self).get_parser(prog_name)
        parser.add_argument(
            'security_group',
            metavar='<security_group>',
            help='Security group rule ID',
        )
        return parser

    def take_action(self, parsed_args):
        data = self.app.session.get(
            '/security-groups/{}/rules'.format(parsed_args.security_group)
        )
        return tabulate(data)


class ShowSecurityGroupRule(ShowOne):
    """Show security group rule details."""

    def get_parser(self, prog_name):
        parser = super(ShowSecurityGroupRule, self).get_parser(prog_name)
        parser.add_argument(
            'security_group_rule',
            metavar='<security_group_rule>',
            help='Security group rule ID',
        )
        parser.add_argument(
            '--security-group',
            required=True,
            metavar='<security_group>',
            help='security group name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/{}/rules/{}'.format(
            parsed_args.security_group,
            parsed_args.security_group_rule
        )
        data = self.app.session.get(uri)
        return tabulate(data)


class CreateSecurityGroupRule(ShowOne):
    """Create Security Group Rule."""

    def get_parser(self, prog_name):
        parser = super(CreateSecurityGroupRule, self).get_parser(prog_name)
        parser.add_argument(
            'security_group',
            metavar='<security_group>',
            help='Security group name or ID'
        )
        parser.add_argument(
            '--direction',
            required=True,
            metavar='<direction>',
            help='Direction'
        )
        parser.add_argument(
            '--ethertype',
            default='IPv4',
            metavar='<ethertype>',
            help='IP version',
            choices=['IPv4', 'IPv6']
        )
        parser.add_argument(
            '--port-range-min',
            metavar='<port_range_min>',
            help='Minimum of port range'
        )
        parser.add_argument(
            '--port-range-max',
            metavar='<port_range_max>',
            help='Maximum of port range'
        )
        parser.add_argument(
            '--protocol',
            required=True,
            metavar='<protocol>',
            help="Protocol"
        )
        parser.add_argument(
            '--remote-ip-prefix',
            required=False,
            metavar='<remote_ip_prefix>',
            help='remote IP prefix matched by this security group rule'
        )
        return parser

    def take_action(self, parsed_args):
        args = [
            'direction', 'ethertype', 'port_range_min',
            'port_range_max', 'protocol', 'remote_ip_prefix',
        ]
        payload = {arg: getattr(parsed_args, arg) for arg in args
                   if getattr(parsed_args, arg) is not None}
        uri = '/security-groups/%s/rules' % parsed_args.security_group
        data = self.app.session.post(uri, payload)

        return tabulate(data)


class DeleteSecurityGroupRule(Command):
    """Delete Security Group Rule."""

    def get_parser(self, prog_name):
        parser = super(DeleteSecurityGroupRule, self).get_parser(prog_name)
        parser.add_argument(
            'security_group_rule',
            metavar='<security_group_rule>',
            help='Security group rule ID'
        )
        parser.add_argument(
            '--security-group',
            required=True,
            metavar='<security_group>',
            help='Security group name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/security-groups/{}/rules/{}'.format(parsed_args.security_group,
                                                    parsed_args.security_group_rule)
        self.app.session.delete(uri)
