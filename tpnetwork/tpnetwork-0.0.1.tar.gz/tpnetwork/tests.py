#!/usr/bin/python3

from modules import IPv4Address, IPv4Network

netip = IPv4Network('192.168.2.111/255.255.255.0')
print(netip.get_network_address())
print(netip.get_firstlast_addresses())
print(netip.get_broadcast_address())
