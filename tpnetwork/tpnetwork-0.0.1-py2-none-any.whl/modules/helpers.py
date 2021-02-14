import re
from .exceptions import AddressValueError

IPv4Address_RE = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')

def get_ipv4addr(address):
    if IPv4Address_RE.match(address):
        return address
    
    raise AddressValueError(address)

def is_netmask(netmask):
    if not IPv4Address_RE.match(netmask):
        return False
    
    is_255 = True
    for octet in list(map(int, netmask.split('.'))):
        if not is_255:
            if octet != 0:
                return False
            continue
        if octet == 255:
            continue
        
        is_255 = False
        if octet == 0:
            continue
        
        index_firstzero = bin(octet)[2:].index('0')
        index_lastone = 8 - bin(octet)[2:][::-1].index('1')

        if index_firstzero != index_lastone:
            return False
    
    return True

def get_ipv4network(address):
    if not '/' in address:
        raise AddressValueError(address, message='Bad IPv4 Network format')
    
    netmask = address.split('/')[1]
    address = address.split('/')[0]

    if not IPv4Address_RE.match(address):
        raise AddressValueError(address)
    
    bad_netmask_format = True
    if not len(netmask) <= 2:
        if not is_netmask(netmask):
            raise AddressValueError('Bad IPv4 Netmask')
        bad_netmask_format = False

    if bad_netmask_format:
        cidr = int(netmask)
        if cidr < 0 or cidr > 32:
            raise ValueError('CIDR value must be between 0 and 32')
        
        netmask = (32 - cidr) * '0' + cidr * '1'
    
    return address, netmask