import base64
import ipaddress
from enum import Enum
from typing import Optional, List, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from pyroute2 import WireGuard as PyRouteWireGuard, IPRoute


class PublicKey:
    """
    X25519 PublicKey Object.

    Handles validation and base64 conversion.

    :param public_key: base64 encoded key or X25519PublicKey object
    :type public_key: Union[str, X25519PublicKey]
    """
    __slots__ = ('__public_key',)

    def __init__(self, public_key: Union[str, X25519PublicKey]):
        if isinstance(public_key, X25519PublicKey):
            self.__public_key = public_key
        elif isinstance(public_key, str):
            self.__public_key = X25519PublicKey.from_public_bytes(base64.b64decode(public_key))
        else:
            raise TypeError("public_key must be a string or X25519PublicKey object")

    def __str__(self):
        value = base64.b64encode(
            self.__public_key.public_bytes(serialization.Encoding.Raw,
                                           serialization.PublicFormat.Raw))
        if isinstance(value, bytes):
            value = value.decode('ascii')
        return value


class PrivateKey:
    """
    X25519 PrivateKey Object.

    Handles validation and base64 conversion.

    :param private_key: base64 encoded key or X25519PublicKey object
    :type private_key: Union[str, X25519PublicKey]
    """
    __slots__ = ('__private_key',)

    def __init__(self, private_key: Union[str, X25519PrivateKey]):
        if isinstance(private_key, X25519PrivateKey):
            self.__private_key = private_key
        elif isinstance(private_key, str):
            self.__private_key = X25519PrivateKey.from_private_bytes(base64.b64decode(private_key))
        else:
            raise TypeError("private_key must be a string or X25519PrivateKey object")

    @classmethod
    def generate(cls):
        """
        Generate a new PrivateKey object.

        :return: Newly generated PrivateKey object
        :rtype: PrivateKey
        """
        return cls(X25519PrivateKey.generate())

    def __str__(self):
        value = base64.b64encode(
            self.__private_key.private_bytes(serialization.Encoding.Raw,
                                             serialization.PrivateFormat.Raw,
                                             serialization.NoEncryption()))
        if isinstance(value, bytes):
            value = value.decode('ascii')
        return value

    def public_key(self) -> PublicKey:
        """
        Return associated PublicKey

        :return: Associated PublicKey
        :rtype: PublicKey
        """
        return PublicKey(self.__private_key.public_key())


class WireGuardException(Exception):
    """
    Exception for WireGuard Interface operational errors (usually wraps NetLink Exceptions).
    """


class WireGuard:
    """
    WireGuard Interface abstraction class.

    This class wraps :mod:`pyroute2` methods to manage a WireGuard interface via NetLink.

    :param interface_name: WireGuard Interface Name
    """
    __slots__ = ('__ifname', '__ifindex')
    __wg = None
    __ipr = None

    class ErrorCode(Enum):
        """
        Enumeration of useful NetLink errors.

        Use this enum to check for matching NetLinkException codes.
        """
        NO_SUCH_DEVICE = 19

    def __init__(self, interface_name):
        self.__connect_backend()
        self.__ifname = interface_name
        interface = self.__get_interface_index(interface_name)
        if not interface:
            raise WireGuardException("Interface does not exist.")
        self.__ifindex = interface

    @classmethod
    def __connect_backend(cls):
        """
        Initialize static pyroute backend objects.

        These attributes are made static such that they won't clog up the file descriptors
        whenever too many are instantiated and not garbage collected.
        """
        if cls.__wg is None:
            cls.__wg = PyRouteWireGuard()
        if cls.__ipr is None:
            cls.__ipr = IPRoute()

    @classmethod
    def create_interface(cls, interface_name: str) -> 'WireGuard':
        """
        Create and enable (set state up) a new WireGuard interface.

        :param interface_name: WireGuard interface name
        :type interface_name: str
        :return: WireGuard object handling the newly created interface
        :rtype: WireGuard
        """
        cls.__connect_backend()
        cls.__ipr.link('add', ifname=interface_name, kind='wireguard')
        cls.__ipr.link('set', index=cls.__get_interface_index(interface_name), state='up')
        return cls(interface_name)

    @classmethod
    def get_or_create_interface(cls, interface_name: str) -> ('WireGuard', bool):
        """
        Get or create a new WireGuard interface.

        Create and enable (set state up) a new WireGuard interface.
        If this already exists, get it.

        :param interface_name: WireGuard interface name
        :type interface_name: str
        :return: WireGuard object handling the interface, whether the interface has been created
        :rtype: (WireGuard, bool)
        """
        cls.__connect_backend()
        interface = cls.__get_interface_index(interface_name)
        if not interface:
            return cls.create_interface(interface_name), True
        return cls(interface_name), False

    @classmethod
    def get_interface(cls, interface_name: str) -> Optional['WireGuard']:
        """
        Same as calling constructor, but returns None instead of raising WireGuardException

        :param interface_name: WireGuard interface name
        :return: WireGuard object handling the interface or None
        :rtype: WireGuard, optional
        """
        cls.__connect_backend()
        try:
            return cls(interface_name)
        except WireGuardException:
            return None

    @classmethod
    def __get_interface_index(cls, interface_name: str) -> Optional[int]:
        """
        Get iproute device index by interface name

        :param interface_name: WireGuard interface name
        :return: IPRoute device index
        :rtype: int, optional
        """
        cls.__connect_backend()
        interface: list = cls.__ipr.link_lookup(ifname=interface_name)
        if not interface:
            return None
        return interface[0]

    @property
    def interface_name(self):
        """
        The interface name.

        :return: interface name
        :rtype: str
        """
        return self.__ifname

    def get_ip_addresses(self) -> List[str]:
        """
        Return the interface's addresses.

        :return: list of IPv4 interfaces (IP with CIDR) as str
        :rtype: list
        """
        interface_data = self.__ipr.get_addr(label=self.interface_name)
        return list(map(
            lambda i: dict(i['attrs'])['IFA_ADDRESS'] + '/' + str(i['prefixlen']),
            interface_data
        ))

    def set_ip_addresses(self, *ip_addresses: str):
        """
        Set the interface's addresses.

        :param ip_addresses: new addresses
        """
        old_ip_addresses = self.get_ip_addresses()
        new_ip_addresses = []
        for address in ip_addresses:
            try:
                address = ipaddress.IPv4Interface(address)
            except Exception as e:
                raise ValueError(e)

            new_ip_addresses.append(str(address))

        for address in old_ip_addresses:
            ip, mask = address.split('/')
            if address not in new_ip_addresses:
                self.__ipr.addr('del', self.__ifindex,
                                address=ip, mask=int(mask))

        for address in new_ip_addresses:
            ip, mask = address.split('/')
            if address not in old_ip_addresses:
                self.__ipr.addr('add', self.__ifindex,
                                address=ip, mask=int(mask))

    def set_interface(self, **kwargs):
        """
        Set interface parameters.

        :param kwargs: :mod:`pyroute2.WireGuard.set` kwargs https://docs.pyroute2.org/wireguard.html
        """
        self.__wg.set(self.__ifname, **kwargs)

    def set_peer(self, public_key, *allowed_ips, **kwargs):
        """
        Set a peer on the interface

        :param public_key: peer's public key
        :param allowed_ips: peer's AllowedIPs
        :param kwargs: peer struct kwargs https://docs.pyroute2.org/wireguard.html
        """
        self.set_interface(peer={
            'public_key': str(public_key),
            'allowed_ips': [str(ipaddress.IPv4Interface(ip)) for ip in allowed_ips],
            **kwargs
        })

    def set_peers(self, *peers):
        """
        Set multiple peers

        :param peers: peer structs https://docs.pyroute2.org/wireguard.html
        """
        for peer in peers:
            self.set_interface(peer=peer)

    def remove_peers(self, *public_keys):
        """
        Remove peers by public key

        :param public_keys: peers' public keys
        """
        for pubkey in public_keys:
            peer = {'public_key': str(pubkey), 'remove': True}
            self.set_interface(peer=peer)

    def delete(self):
        """
        Delete the WireGuard interface.

        Set state down and remove device.
        """
        self.__ipr.link('set', index=self.__ifindex, state='down')
        self.__ipr.link('delete', index=self.__ifindex)
