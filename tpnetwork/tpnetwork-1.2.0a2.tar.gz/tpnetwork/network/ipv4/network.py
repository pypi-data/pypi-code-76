from . import IPv4Address, binary_to_ipv4, NetworkValueError

import re

IPv4_NETADDR_RE = re.compile(
    r'^(?:((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/'
    r'(?:((?:([1-9]|[1-2][0-9]|3[0-2]))'
    r'|(?:((0\.0\.0\.0)'
    r'|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0\.0\.0)'
    r'|(255\.((0\.0\.0)|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0\.0)'
    r'|(255\.((0\.0)|(((1(28|92))|(2((24)|(4(0|8))|(5(2|4)))))\.0)'
    r'|(255\.(0|(1(28|92))|(2((24)|(4(0|8))|(5(2|4|5))))))))))))))))$'
    )

class IPv4Network:
    def __init__(self, net_address):
        '''
        IPv4Network object constructor

        :param address: An IPv4 network
        :type address: str

        :Example:
        IPv4Network('192.168.0.1/24'), IPv4Network('192.168.0.1/255.255.255.0')
        '''
        if not self._verify_network(net_address):
            raise NetworkValueError(net_address)
        self._net_address = net_address
        self._address = self._net_address.split('/')[0]
        self._netmask = self._net_address.split('/')[1]
        self._cidr = 0

        if '.' in self._netmask:
            self._set_cidr()
        else:
            self._cidr = int(self._netmask)
            self._set_netmask()
    
    def _verify_network(self, net_address):
        '''
        Verify an IPv4 network format

        :param net_address: An IPv4 network
        :type net_address: str
        :return: Status of the verification
        :rtype: bool

        :Example:
        >>> IPv4Address._verify_address('192.168.0.1')
        False
        >>> IPv4Address._verify_address('192.168.0.1/24')
        True
        >>> IPv4Address._verify_address('192.168.0.1/255.255.255.0')
        True
        >>> IPv4Address._verify_address('192.168.0.1/100')
        False
        >>> IPv4Address._verify_address('192.168.0.1/255.255.256.0')
        False
        '''
        if IPv4_NETADDR_RE.match(net_address):
            return True
        return False
    
    def _set_netmask(self):
        '''
        Set netmask value based on CIDR
        '''
        self._netmask = str(binary_to_ipv4('1' * (self._cidr) + '0' * (32 - self._cidr)))
    
    def _set_cidr(self):
        '''
        Set CIDR value based on netmask
        '''
        self._cidr = self.__binary__()[1].count('1')
    
    def get_netinfo(self):
        '''
        Get IPv4Network network information

        :return: The network informations
        :return network: The ipv4 network address
        :return first: The ipv4 first address
        :return last: The ipv4 last address
        :return broadcast: The ipv4 broadcast address
        :rtype: dict
        :rtype network: IPv4Address
        :rtype first: IPv4Address
        :rtype last: IPv4Address
        :rtype broadcast: IPv4Address
        '''
        netaddr_bin = self.__binary__()

        network_bin = netaddr_bin[0][:self._cidr] + '0' * (32 - self._cidr)
        broadcast_bin = netaddr_bin[0][:self._cidr] + '1' * (32 - self._cidr)
        first_addr_bin = network_bin[:-1] + '1'
        last_addr_bin = broadcast_bin[:-1] + '0'
        
        return {
            'network': binary_to_ipv4(network_bin),
            'first': binary_to_ipv4(first_addr_bin),
            'last': binary_to_ipv4(last_addr_bin),
            'broadcast': binary_to_ipv4(broadcast_bin)
            }
    
    def is_address_included(self, address):
        '''
        Verify if an IPv4 address is included in IPv4 network address

        :param address: An IPv4 address
        :type address: IPv4Address
        :return: Verification status
        :rtype: bool

        :Example:
        >>> IPv4Network('192.168.0.1/24').is_address_included(IPv4Address('192.168.0.5'))
        True
        >>> IPv4Network('192.168.0.1/24').is_address_included(IPv4Address('192.168.1.5'))
        False
        '''
        if not isinstance(address, IPv4Address):
            raise TypeError('address argument must an IPv4Address object')
        
        netaddr_self_bin = self.get_netinfo()['network'].__binary__()
        netaddr_address_bin = address.__binary__()[:self._cidr] + '0' * (32 - self._cidr)

        if netaddr_address_bin == netaddr_self_bin:
            return True
        return False
    
    def __str__(self):
        '''
        Return an IPv4Network object in str format

        :return: The IPv4 network
        :rtype: str

        :Example:
        >>> IPv4Address('192.168.0.1/255.255.255.0').__str__()
        '192.168.0.1/24'
        '''
        return self._address + '/' + str(self._cidr)

    def __octets__(self):
        '''
        Return an IPv4Network object in tuple format

        :return: The IPv4 network
        :return 0: The IPv4 address
        :return 1: The IPv4 netmask
        :rtype: tuple
        :rtype 0: tuple
        :rtype 1: tuple

        :Example:
        >>> IPv4Address('192.168.0.1/24').__octets__()
        ((192, 168, 0, 1), (255, 255, 255, 0))
        '''
        return (tuple(map(int, self._address.split('.'))), tuple(map(int, self._netmask.split('.'))))
    
    def __binary__(self):
        '''
        Return an IPv4Network object in bits format

        :return: The IPv4 network
        :return 0: The IPv4 address
        :return 1: The IPv4 netmask
        :rtype: tuple
        :rtype 0: str
        :rtype 1: str

        :Example:
        >>> IPv4Address('192.168.0.1/24').__binary__()
        ('11000000101010000000000000000001', '11111111111111111111111100000000')
        '''
        return (
            ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__()[0] ]),
            ''.join([ '0'*(8-len(bin(octet)[2:])) + bin(octet)[2:] for octet in self.__octets__()[1] ])
            )
