from . import get_ipv4addr
from .exceptions import AddressValueError

def binary_to_ipv4(binary):
        octet_bin = ''
        address = ''

        for bit in binary:
            octet_bin += bit
            if len(octet_bin) == 8:
                if address != '':
                    address += '.'
                address += str(int(octet_bin, 2))
                octet_bin = ''
        
        return IPv4Address(address)

class IPv4Address(object):
    def __init__(self, address):
        self._address = address

    def ipv4_to_binary(self):
        octet_bin = ''
        address_bin = []
        for octet in self._address.split('.'):
            octet = int(octet)
            octet_bin += '0'*(8 - len(bin(octet)[2:])) + bin(octet)[2:]
            if len(octet_bin) == 8:
                address_bin.append(octet_bin)
            octet_bin = ''
        
        return tuple(address_bin)

    def __str__(self):
        return self._address
    
    def __repr__(self):
        return f'IPv4Address(\'{self._address}\')'
