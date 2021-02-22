"""
    Digicloud Namespace Management.
"""
import sys

from cliff.formatters.table import TableFormatter
from cliff.lister import Lister
from cliff.show import ShowOne

from ..utils import tabulate, yes_or_no


class NamespaceFetchMixin:
    def _build_namespace_list(self):
        namespaces = self.app.session.get('/namespaces')
        ids, names = {}, {}
        for ns in namespaces:
            if ns['name'] not in names:
                names[ns['name']] = []
            names[ns['name']].append(ns)
            ids[ns['id']] = ns
        return ids, names

    def _get_namespace_or_exit(self, namespace_ref, parsed_args):
        ids, names = self._build_namespace_list()
        if namespace_ref in ids:
            return ids[namespace_ref]
        if namespace_ref in names:
            possible_options = names[namespace_ref]
            if len(possible_options) == 1:
                return possible_options[0]
            self._display_options(possible_options, parsed_args)
        else:
            raise Exception("You don't have a namespace with this name or id")

    def _display_options(self, options, parsed_args):
        header, rows = tabulate(options)
        TableFormatter().emit_list(
            header,
            rows,
            self.app.stdout,
            parsed_args
        )
        message = "You have more than one namespaces with this name, " \
                  "please use namespace id"
        raise Exception(message)


class CreateNamespace(ShowOne):
    """Create Namespace."""

    def get_parser(self, prog_name):
        parser = super(CreateNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=('Name of namespace')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=('Description of namespace')
        )
        return parser

    def take_action(self, parsed_args):
        payload = {
            'name': parsed_args.name,
            'description': parsed_args.description,
        }
        data = self.app.session.post('/namespaces', payload)

        return tabulate(data)


class ListNamespace(Lister):
    """List namespaces"""

    def take_action(self, parsed_args):
        data = self.app.session.get('/namespaces')

        return tabulate(data)


class ShowNamespace(ShowOne, NamespaceFetchMixin):
    """Show server details."""

    def get_parser(self, prog_name):
        parser = super(ShowNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def take_action(self, parsed_args):
        return tabulate(self._get_namespace_or_exit(parsed_args.namespace, parsed_args))


class ListNamespaceMember(Lister, NamespaceFetchMixin):
    """List namespace members."""

    def get_parser(self, prog_name):
        parser = super(ListNamespaceMember, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def take_action(self, parsed_args):
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)
        uri = '/namespaces/%s/members' % namespace['id']
        data = self.app.session.get(uri)

        return tabulate(data)


class InviteMember(ShowOne, NamespaceFetchMixin):
    """Add Member to Namespace."""

    def get_parser(self, prog_name):
        parser = super(InviteMember, self).get_parser(prog_name)
        parser.add_argument(
            '--email',
            metavar='<user_email>',
            required=True,
            help='E-mail Address to send the invitation'
        )

        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        return parser

    def take_action(self, parsed_args):
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)
        uri = '/invitations'
        payload = {
            'email': parsed_args.email,
            'namespace': namespace['id']
        }
        data = self.app.session.post(uri, payload)
        return tabulate(data)


class DeleteNamespaceMember(ShowOne, NamespaceFetchMixin):
    """Delete Member from Namespace."""

    def get_parser(self, prog_name):
        parser = super(DeleteNamespaceMember, self).get_parser(prog_name)
        parser.add_argument(
            '--user-id',
            metavar='<user_id>',
            required=True,
            help='ID of user'
        )
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )

        return parser

    def take_action(self, parsed_args):
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)
        uri = f'/namespaces/{namespace["id"]}/members/{parsed_args.user_id}'
        data = self.app.session.delete(uri)

        return tabulate(data)


class LeaveNamespace(ShowOne, NamespaceFetchMixin):
    """Leave a namespace """
    def get_parser(self, prog_name):
        parser = super(LeaveNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )

        return parser

    def take_action(self, parsed_args):
        current_user = self.app.config['USER']['id']
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)
        uri = '/namespaces/%s/members/%s' % (namespace['id'], current_user)
        self.app.session.delete(uri)
        return tabulate(namespace)


class DeleteNamespace(ShowOne, NamespaceFetchMixin):
    """Delete Namespace."""

    def get_parser(self, prog_name):
        parser = super(DeleteNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )
        parser.add_argument(
            '--i-am-sure',
            help='Use this switch to bypass confirmation',
            default=None,
            action='store_true'
        )

        return parser

    def take_action(self, parsed_args):
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)

        if not parsed_args.i_am_sure and not self.confirm(namespace, parsed_args):
            self.app.stdout.write("Namespace deletion canceled by user\n")
            sys.exit(0)

        uri = '/namespaces/%s?force=true' % namespace['id']
        self.app.session.delete(uri)
        self.app.stdout.write("Namespace has been deleted\n")
        return tabulate(namespace)

    def confirm(self, namespace, parsed_args):
        uri = '/namespaces/%s/resources' % namespace['id']
        data = self.app.session.get(uri)
        headers = ("region", "type", "name", "description", "spec", "created_at")
        rows = []
        for region in data:
            for instance in region['resources']['instances']:
                rows.append(
                    (
                        region['region_name'],
                        "instance",
                        instance['name'],
                        instance.get('description', ""),
                        "type=%s,status=%s" % (instance['type'], instance['status']),
                        instance['created_at'],
                    )
                )
            for volume in region['resources']['volumes']:
                rows.append(
                    (
                        region['region_name'],
                        "volume",
                        volume['name'],
                        volume.get('description', ""),
                        "size=%sGB,status=%s" % (volume['size'], volume['status']),
                        volume['created_at'],
                    )
                )
            for network in region['resources']['networks']:
                rows.append(
                    (
                        region['region_name'],
                        "network",
                        network['name'],
                        network.get('description', ""),
                        "subnets=%s,status=%s" % (
                            len(network['subnets']), network['status']),
                        network['created_at'],
                    )
                )

            for subnet in region['resources']['subnets']:
                rows.append(
                    (
                        region['region_name'],
                        "subnet",
                        subnet['name'],
                        subnet.get('description', ""),
                        "gateway=%s,cidr=%s" % (
                            subnet['gateway_ip'], subnet['cidr']),
                        subnet['created_at'],
                    )
                )

            for router in region['resources']['routers']:
                rows.append(
                    (
                        region['region_name'],
                        "router",
                        router['name'],
                        router.get('description', ""),
                        "status=%s" % router['status'],
                        router['created_at'],
                    )
                )
            for fip in region['resources']['floating_ips']:
                rows.append(
                    (
                        region['region_name'],
                        "floating-ip",
                        " --- ",
                        fip.get('description', ""),
                        "address=%s,status=%s" % (
                        fip['floating_ip_address'], fip['status']),
                        fip['created_at'],
                    )
                )

            for sg in region['resources']['security_groups']:
                rows.append(
                    (
                        region['region_name'],
                        "security-group",
                        sg['name'],
                        sg.get('description', ""),
                        "rules=%s" % len(sg['security_group_rules']),
                        sg['created_at'],
                    )
                )

        TableFormatter().emit_list(
            headers,
            rows,
            self.app.stdout,
            parsed_args
        )
        return yes_or_no(
            "You're about to delete namespace '%s' with all resources including"
            " Instances, Volumes, Networks. \nPlease review this list "
            "carefully before deleting your namespace, All your data and network"
            " configuration will be lost.\n"
            "Are you sure?" % namespace['name'])


class SelectNamespace(ShowOne, NamespaceFetchMixin):
    """Select Namespace."""

    def get_parser(self, prog_name):
        parser = super(SelectNamespace, self).get_parser(prog_name)
        parser.add_argument(
            'namespace',
            metavar='<namespace>',
            help='Namespace name or id',
        )

        return parser

    def take_action(self, parsed_args):
        namespace = self._get_namespace_or_exit(parsed_args.namespace, parsed_args)
        self.app.config['AUTH_HEADERS']['Digicloud-Namespace'] = namespace['id']
        self.app.config.save()
        return tabulate(namespace)


class CurrentNamespace(ShowOne):
    """Display current namespace."""

    def get_parser(self, prog_name):
        parser = super(CurrentNamespace, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):
        if self.app.config.get('AUTH_HEADERS') is None:
            raise Exception("Login is required")
        else:
            namespace_id = self.app.config['AUTH_HEADERS']['Digicloud-Namespace']
            namespace = self.app.session.get('/namespaces/%s' % namespace_id)
            return tabulate(namespace)


class AcceptInvitation(ShowOne, NamespaceFetchMixin):
    """Accept an invitation to join a namespace"""

    def get_parser(self, prog_name):
        parser = super(AcceptInvitation, self).get_parser(prog_name)
        parser.add_argument(
            'invitation',
            metavar='<invitation>',
            help='Invitation ID to accept or reject'
        )

        return parser

    def take_action(self, parsed_args):
        uri = '/invitations/%s' % parsed_args.invitation
        payload = {
            'status': "accepted"
        }
        data = self.app.session.patch(uri, payload)
        return tabulate(data)


class ListInvitation(Lister, NamespaceFetchMixin):
    """List your namespace invitations"""

    def take_action(self, parsed_args):
        uri = '/invitations'
        data = self.app.session.get(uri)
        return tabulate(data)
