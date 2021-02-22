from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from digicloud.utils import tabulate


class ListRegions(Lister):
    """List available regions"""
    def take_action(self, parsed_args):
        data = self.app.session.get('/regions')
        return tabulate(data)


class SelectRegion(Command):
    """Select specific region to setup"""
    def get_parser(self, prog_name):
        parser = super(SelectRegion, self).get_parser(prog_name)

        parser.add_argument(
            'region_name',
            metavar='<region_name>',
            help="Region name"
        )

        return parser

    def take_action(self, parsed_args):
        self.app.config['AUTH_HEADERS'].update({
            'Digicloud-Region': parsed_args.region_name,
        })


class CurrentRegion(ShowOne):
    """Show current selected region"""
    def take_action(self, parsed_args):
        header = self.app.config.get('AUTH_HEADERS')
        if header is not None:
            selected_region = header.get('Digicloud-Region', 'No region selected')
        else:
            selected_region = 'No region selected'

        return ('Current region', ), (selected_region, )
