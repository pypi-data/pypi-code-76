import re

from django.core.management.base import BaseCommand
from django.core.validators import RegexValidator

from django_wireguard.models import WireguardInterface


class Command(BaseCommand):
    help = 'Setup WireGuard interface'

    def add_arguments(self, parser):
        parser.add_argument('interface_name',
                            type=str,
                            help="Interface Name")
        parser.add_argument('--listen-port',
                            nargs='?',
                            type=int,
                            default=1194,
                            help="Listen Port for the interface")
        parser.add_argument('--private-key',
                            nargs='?',
                            type=str,
                            help="Base64 encoded Private Key")
        parser.add_argument('--address',
                            nargs='*',
                            type=str,
                            help="Interface address(es)")

    def handle(self, *args, **options):
        if not re.match(r'^[a-zA-Z0-9]+$', options['interface_name']):
            self.stderr.write(self.style.ERROR("Interface Name must be a string of alphanumeric characters."))
            return

        interface = WireguardInterface.objects.filter(name=options['interface_name'])

        address = ','.join(options['address'] or [])

        if interface.exists():
            if options['private_key']:
                interface.update(listen_port=options['listen_port'],
                                 private_key=options['private_key'],
                                 address=address)
            else:
                interface.update(listen_port=options['listen_port'],
                                 address=address)
            self.stderr.write(self.style.SUCCESS(f"Interface updated: {interface.first().name}.\n"))
        else:
            interface = WireguardInterface.objects.create(name=options['interface_name'],
                                                          listen_port=options['listen_port'],
                                                          private_key=options['private_key'],
                                                          address=address)

            self.stderr.write(self.style.SUCCESS(f"Interface created: {interface.name}.\n"))
