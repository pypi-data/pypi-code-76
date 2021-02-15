from . import AddressValueError

import re

# REGEX GLOBALES VARIABLES
BINARY_RE = re.compile(r'^[0-1]{32}$')
IPv4_ADDR_RE = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

def binary_to_ipv4(binary):
    '''
    Convert a binary to an IPv4 address.

    :param binary: A 32 bits address
    :type binary: str
    :return: The IPv4 address converted
    :rtype: IPv4Address

    :Example:
    >>> binary_to_ipv4('11000000101010000000000000000001')
    IPv4Address('192.168.0.1')
    '''
    if not BINARY_RE.match(binary):
        raise ValueError(binary + ' is not a binary address')

    return IPv4Address('.'.join([ str(int(binary[bit:bit+8], 2)) for bit in range(0, 32, 8) ]))

class IPv4Address:
    def __init__(self, address):
        '''
        IPv4Address object constructor

        :param address: An IPv4 address
        :type address: str
        '''
        if not self._verify_address(address):
            raise AddressValueError(address)
        self._address = address
    
    def _verify_address(self, address):
        '''
        Verify an IPv4 address format

        :param address: An IPv4 address
        :type address: str
        :return: Status of the verification
        :rtype: bool

        :Example:
        >>> IPv4Address._verify_address('192.168.0.1')
        True
        >>> IPv4Address._verify_address('256.1.1.1000')
        False
        '''
        if IPv4_ADDR_RE.match(address):
            return True
        return False
    
    def __str__(self):
        '''
        Return an IPv4Address object in str format

        :return: The IPv4 address
        :rtype: str

        :Example:
        >>> IPv4Address('192.168.0.1').__str__()
        '192.168.0.1'
        '''
        return self._address

    def __octets__(self):
        '''
        Return an IPv4Address object in tuple format

        :return: The IPv4 address
        :rtype: tuple

        :Example:
        >>> IPv4Address('192.168.0.1').__octets__()
        (192, 168, 0, 1)
        '''
        return tuple(map(int, self._address.split('.')))

    def __binary__(self):
        '''
        Return an IPv4Address object in bits format

        :return: The IPv4 address
        :rtype: str

        :Example:
        >>> IPv4Address('192.168.0.1').__binary__()
        '11000000101010000000000000000001'
        '''
        return ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__() ])
