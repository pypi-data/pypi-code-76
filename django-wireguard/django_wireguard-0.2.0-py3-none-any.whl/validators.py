import ipaddress
from typing import Union

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django_wireguard.wireguard import PrivateKey, PublicKey


def validate_private_ipv4(value: str):
    """
    Validate private IPv4 address.

    :param value: Value to validate
    :type value: str
    :raises: ValidationError if value provided is not a valid IPv4 address
    """
    try:
        ip_address = ipaddress.IPv4Address(value)
        if not ip_address.is_private or ip_address.is_unspecified:
            raise ValueError
    except (ValueError, ipaddress.AddressValueError):
        raise ValidationError(
            _('%(value)s is not a valid private IP Address.'),
            params={'value': value},
        )


def validate_allowed_ips(value: str):
    """
    Validate comma-separated list of allowed_ips (IPv4 interfaces).

    :param value: Value to validate
    :type value: str
    :raises: ValidationError if value provided is not a valid list of IPv4 interfaces
    """
    for ip in value.split(','):
        try:
            ip_address = ipaddress.IPv4Interface(ip)
            if not ip_address.is_private or ip_address.is_unspecified:
                raise ValueError
        except (ValueError, ipaddress.AddressValueError):
            raise ValidationError(
                _('%(value)s is not a valid private IP Address.'),
                params={'value': value},
            )


def validate_wireguard_private_key(value: str):
    """
    Validate base64 encoded private key.

    :param value: Value to validate
    :raises: ValidationError if value provided is not a valid private key
    """
    try:
        PrivateKey(value)
    except ValueError:
        raise ValidationError(
            _('The value specified is not a valid WireGuard Private Key.'),
        )


def validate_wireguard_public_key(value):
    """
    Validate base64 encoded public key.

    :param value: Value to validate
    :raises: ValidationError if value provided is not a valid public key
    """
    try:
        PublicKey(value)
    except ValueError:
        raise ValidationError(
            _('The value specified is not a valid WireGuard Public Key.'),
        )
