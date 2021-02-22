"""
    Authentication to digicloud API.
"""
import getpass

from cliff.show import ShowOne
from cliff.command import Command


class Login(ShowOne):
    """Digicloud Login"""

    def get_parser(self, prog_name):
        parser = super(Login, self).get_parser(prog_name)
        parser.add_argument(
            '--email',
            required=True,
            metavar='<EMAIL>',
            dest='email',
            help=("Your Digicloud email")
        )

        parser.add_argument(
            '--password',
            metavar='<PASSWORD>',
            required=False,
            default=None,
            dest='password',
            help=("Your Digicloud account password")
        )

        parser.add_argument(
            '--namespace',
            metavar='<NAMESPACE>',
            dest='namespace',
            help=("ID of the Digicloud namespace")
        )

        return parser

    def take_action(self, parsed_args):
        columns = ('Email', 'Namespace name', 'Namespace ID', 'Region')
        payload = {
            'email': parsed_args.email,
            'password': parsed_args.password or getpass.getpass(),
        }
        data = self.app.session.post('/tokens', payload)

        selected_ns = None
        if parsed_args.namespace:
            selected_ns = self._find_namespace(parsed_args.namespace, data['namespaces'])

        selected_ns = selected_ns or data['namespaces'][0]
        rows = [
            parsed_args.email,
            selected_ns['name'],
            selected_ns['id']
        ]
        self.app.config['api_token'] = data['token']
        self.app.config['AUTH_HEADERS'].update({
            'Authorization': 'Bearer {}'.format(data["token"]),
            'Digicloud-Namespace': selected_ns['id'],
        })
        self.app.config['USER'] = data['user']
        rows.append(self._get_active_region())
        return columns, rows

    def _find_namespace(self, name_or_id, namespaces):
        result = [ns for ns in namespaces
                  if name_or_id == ns['name'] or name_or_id == ns['id']]
        if len(result) == 0:
            raise Exception(f'No namespace matched {name_or_id}')
        elif len(result) > 1:
            raise Exception(f'Multiple namespaces matched {name_or_id}')
        return result[0]

    def _get_active_region(self):
        self.app.setup_session()
        auth_headers = self.app.config['AUTH_HEADERS']
        if 'Digicloud-Region' not in auth_headers:
            regions = self.app.session.get('/regions')
            if len(regions) == 0:
                raise Exception("There are no region available for your namespace, "
                                "Please contact support for further information.")
            auth_headers['Digicloud-Region'] = regions[0]['name']
        return auth_headers['Digicloud-Region']


class Logout(Command):
    """DigiCloud Logout"""

    def take_action(self, parsed_args):
        if 'api_token' in self.app.config:
            self.app.session.delete('/tokens/{}'.format(self.app.config['api_token']))
            del self.app.config['api_token']

        del self.app.config['AUTH_HEADERS']
        del self.app.session.headers['Authorization']

        return 0
