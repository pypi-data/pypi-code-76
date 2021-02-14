from .ipv4_address import IPv4Address, binary_to_ipv4
from .helpers import get_ipv4network, is_netmask
from .exceptions import AddressValueError

class IPv4Network:
    def __init__(self, address):
        self._address, self._netmask = get_ipv4network(address)
    
    def get_cidr(self):        
        netmask = IPv4Address(self._netmask)

        return ''.join(netmask.ipv4_to_binary()).count('1')

    def get_network_address(self):
        address = IPv4Address(self._address)
        netmask = IPv4Address(self._netmask)
        address_bin = ''.join(address.ipv4_to_binary())
        netmask_bin = ''.join(netmask.ipv4_to_binary())

        index_net_prefix = netmask_bin.index('0')
        network_bin = address_bin[:index_net_prefix] + '0' * (32 - len(address_bin[:index_net_prefix]))

        return binary_to_ipv4(network_bin)
    
    def get_firstlast_addresses(self):
        network = self.get_network_address()
        netmask = IPv4Address(self._netmask)
        network_bin = ''.join(network.ipv4_to_binary())
        netmask_bin = ''.join(netmask.ipv4_to_binary())

        index_net_prefix = netmask_bin.index('0')
        first_bin = network_bin[:index_net_prefix] + '0' * (32 - len(network_bin[:index_net_prefix]) - 1) + '1'
        last_bin = network_bin[:index_net_prefix] + '1' * (32 - len(network_bin[:index_net_prefix]) - 1) + '0'

        return [binary_to_ipv4(address_bin) for address_bin in [first_bin, last_bin]]
    
    def get_broadcast_address(self):
        network = self.get_network_address()
        netmask = IPv4Address(self._netmask)
        network_bin = ''.join(network.ipv4_to_binary())
        netmask_bin = ''.join(netmask.ipv4_to_binary())

        index_net_prefix = netmask_bin.index('0')
        broadcast_bin = network_bin[:index_net_prefix] + '1' * (32 - len(network_bin[:index_net_prefix]))

        return binary_to_ipv4(broadcast_bin)

    def __str__(self):
        return self._address + ' ' + self._netmask
    
    def __repr__(self):
        return f'IPv4Network(\'{self._address}/{self.get_cidr()}\')'
