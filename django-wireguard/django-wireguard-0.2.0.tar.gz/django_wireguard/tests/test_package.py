import ipaddress
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase, tag

from django_wireguard.models import WireguardInterface, WireguardPeer
from django_wireguard.signals import interface_created, interface_deleted
from django_wireguard.tests.helpers import SignalHelper
from django_wireguard.utils import purge_private_keys, clean_comma_separated_list
from django_wireguard.wireguard import WireGuard, WireGuardException, PrivateKey, PublicKey


class TestWireguardModule(TestCase):
    interface_name = 'testInterface'

    @tag('net')
    def test_interface_not_exists(self):
        with self.assertRaises(WireGuardException):
            WireGuard(self.interface_name)

    def test_private_key(self):
        private_key = "cIfHrTxl4H+ojFn1LIzMHM+IpxOmbKWjhCtW/vd/YFQ="
        public_key = "aEMb9hff7fiVV2f2avti+b37S31ZaBLxfMLgiLD7z14="

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            PrivateKey()

        obj = PrivateKey(private_key)
        self.assertIsInstance(obj, PrivateKey)
        self.assertEqual(str(obj), private_key)
        self.assertIsInstance(obj.public_key(), PublicKey)
        self.assertEqual(str(obj.public_key()), public_key)

        obj = PrivateKey.generate()
        self.assertIsInstance(obj, PrivateKey)

    def test_public_key(self):
        public_key = "aEMb9hff7fiVV2f2avti+b37S31ZaBLxfMLgiLD7z14="

        with self.assertRaises(TypeError):
            # noinspection PyArgumentList
            PublicKey()

        obj = PublicKey(public_key)
        self.assertIsInstance(obj, PublicKey)
        self.assertEqual(str(obj), public_key)


class TestWireguardInterface(TestCase):
    interface_name = 'testInterface'
    test_port = 4321
    test_addresses = '10.100.20.1/24,10.100.0.1/32'

    @tag('net')
    def test_interface_creation(self):
        interface = WireguardInterface.objects.create(name=self.interface_name,
                                                      listen_port=self.test_port,
                                                      address=self.test_addresses)

        try:
            wg = WireGuard(self.interface_name)
        except WireGuardException:
            self.fail("IPROUTE WireGuard Interface not created.")

        ip_addresses = wg.get_ip_addresses()
        for address in interface.get_address_list():
            ip = str(ipaddress.IPv4Interface(address))
            self.assertIn(ip, ip_addresses)

        # delete interface manually to trigger interfaces cleanup
        interface.delete()


class TestSignals(TestCase):
    interface_name = 'testInterface'
    test_port = 4321
    test_addresses = '10.100.20.1/24,10.100.0.1/32'

    @tag('signals')
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard.get_or_create_interface',
                mock.MagicMock(return_value=(mock.MagicMock(return_value=True), True)))
    def test_interface_created_signal_sent(self):
        """
        Test ``interface_created`` signal is sent upon WireguardInterface instance creation.
        """
        with SignalHelper(interface_created, WireguardInterface) as signal:
            interface = WireguardInterface.objects.create(name=self.interface_name,
                                                          listen_port=self.test_port,
                                                          address=self.test_addresses)
            self.assertTrue(signal.signal_sent)
            self.assertIs(signal.signal_sender, WireguardInterface)
            self.assertEqual(signal.signal_kwargs['instance'], interface)

    @tag('signals')
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def test_interface_deleted_signal_sent(self):
        """
        Test ``interface_deleted`` signal is sent upon WireguardInterface instance deleted.

        Mocks ``WireGuard.create_interface`` and ``WireGuard.delete`` methods to avoid the need for
        Wireguard capabilities enabled.
        """
        with SignalHelper(interface_deleted, WireguardInterface) as signal:
            interface = WireguardInterface.objects.create(name=self.interface_name,
                                                          listen_port=self.test_port,
                                                          address=self.test_addresses)
            interface.delete()
            self.assertTrue(signal.signal_sent)
            self.assertIs(signal.signal_sender, WireguardInterface)
            self.assertEqual(signal.signal_kwargs['instance'], interface)


class TestWireguardPeer(TestCase):
    """
    Test WireguardPeer models creation and cleanup utils.

    Mocks ``Wireguard.create_interface`` methods to avoid the need for
    Wireguard capabilities enabled.
    """
    interface_name = 'testInterface'
    test_port = 4321
    test_addresses = '10.100.20.1/24,10.100.0.1/32'

    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def setUp(self):
        self.interface = WireguardInterface.objects.create(name=self.interface_name,
                                                           listen_port=self.test_port,
                                                           address=self.test_addresses)

    @tag('utils')
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def test_key_cleanup(self):
        WireguardPeer.objects.create(interface=self.interface,
                                     address='10.100.20.2',
                                     private_key='cIfHrTxl4H+ojFn1LIzMHM+IpxOmbKWjhCtW/vd/YFQ=')
        self.assertEqual(1, WireguardPeer.objects.filter(private_key__isnull=False).count())
        purge_private_keys()
        self.assertEqual(0, WireguardPeer.objects.filter(private_key__isnull=False).count())


class TestManagementCommands(TestCase):
    interface_name = 'testInterface'
    test_port = 4321
    test_addresses = ['10.100.20.1/24', '10.100.0.1/32']

    @tag('command')
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def test_setup_command_creation(self):
        out = StringIO()
        err = StringIO()
        call_command('setup_interface',
                     self.interface_name,
                     "--listen-port", self.test_port,
                     "--address", *self.test_addresses,
                     stdout=out, stderr=err)
        self.assertIn("create", err.getvalue())
        self.assertIn(self.interface_name, err.getvalue())

        interface = WireguardInterface.objects.filter(name=self.interface_name,
                                                      listen_port=self.test_port)
        self.assertTrue(interface.exists())

        addresses = interface.first().get_address_list()
        for address in self.test_addresses:
            self.assertIn(address, addresses)

    @tag('command')
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def test_setup_command_update(self):
        WireguardInterface.objects.create(
            name=self.interface_name,
            listen_port=self.test_port,
            address=self.test_addresses[0]
        )

        out = StringIO()
        err = StringIO()
        call_command('setup_interface',
                     self.interface_name,
                     "--listen-port", self.test_port,
                     "--address", *self.test_addresses,
                     stdout=out, stderr=err)
        self.assertIn("update", err.getvalue())
        self.assertIn(self.interface_name, err.getvalue())

        interface = WireguardInterface.objects.filter(name=self.interface_name,
                                                      listen_port=self.test_port)
        self.assertTrue(interface.exists())

        addresses = interface.first().get_address_list()
        for address in self.test_addresses:
            self.assertIn(address, addresses)


class TestUtils(TestCase):
    @tag('utils')
    def test_comma_separated_list_clean(self):
        """
        Test ``utils.clean_comma_separated_list`` edge cases.
        """
        expected = ['1', '2', '3']
        res = clean_comma_separated_list("1,2,3")
        self.assertEqual(expected, res, "Clean function not correctly evaluating values at comma")
        res = clean_comma_separated_list("1\n,\n2,3")
        self.assertEqual(expected, res, "Clean function not correctly evaluating LF")
        res = clean_comma_separated_list("1\r\n,\r2,3")
        self.assertEqual(expected, res, "Clean function not correctly evaluating CR")
        res = clean_comma_separated_list("1 ,  2 ,  3 ")
        self.assertEqual(expected, res, "Clean function not correctly evaluating spaces")
        res = clean_comma_separated_list("1,2,3,,")
        self.assertEqual(expected, res, "Clean function not correctly evaluating trailing commas")
        res = clean_comma_separated_list("1,\n  2\r, 3\r\n,\n,")
        self.assertEqual(expected, res, "Clean function not correctly evaluating mixed cases")

        res = clean_comma_separated_list(",\n \r,,, \r\n,\n,")
        self.assertEqual([], res, "Clean function not correctly evaluating empty values")
