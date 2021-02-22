"""
    DigiCloud Image Service
"""
from cliff.show import ShowOne
from cliff.lister import Lister

from digicloud import formatter
from ..utils import tabulate


class ListImage(Lister):
    """List images"""

    def take_action(self, parsed_args):
        data = self.app.session.get('/images')

        for image in data:
            image['size'] = formatter.HumanBytes.format(image['size'], True)

        return tabulate(data)


class ShowImage(ShowOne):
    """Show image details."""

    def get_parser(self, prog_name):
        parser = super(ShowImage, self).get_parser(prog_name)
        parser.add_argument(
            'image',
            metavar='<image>',
            help='Image name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/images/%s' % parsed_args.image
        data = self.app.session.get(uri)

        data['size'] = formatter.HumanBytes.format(data['size'], True)

        return tabulate(data)
