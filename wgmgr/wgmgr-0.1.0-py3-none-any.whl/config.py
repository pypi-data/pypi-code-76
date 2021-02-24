from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from pathlib import Path
from typing import Any, Generator

from .connection import Connection
from .peer import Peer
from .util import load_yaml_file, write_yaml_file


class Config:
    def __init__(
        self,
        ipv4_subnet: IPv4Network | None = None,
        ipv6_subnet: IPv6Network | None = None,
        default_port: int = 51902,
    ):
        self.peers: list[Peer] = []
        self.connections: list[Connection] = []
        self.network_ipv4 = ipv4_subnet
        self.network_ipv6 = ipv6_subnet
        self.default_port = default_port

    def update_default_port(self, port: int):
        self.default_port = port

        for peer in self.peers:
            if peer.port_auto:
                peer.port = port

    def update_ipv4_subnet(self, subnet: IPv4Network):
        self.network_ipv4 = subnet
        for peer in self.peers:
            if peer.ipv4_address is None:
                peer.ipv4_address = self.get_next_ipv4()
                continue

            if peer.ipv4_address in self.network_ipv4:
                continue

            peer.ipv4_address = self.get_next_ipv4()

    def update_ipv6_subnet(self, subnet: IPv6Network):
        self.network_ipv6 = subnet
        for peer in self.peers:
            if peer.ipv6_address is None:
                peer.ipv6_address = self.get_next_ipv6()
                continue

            if peer.ipv6_address in self.network_ipv6:
                continue

            peer.ipv6_address = self.get_next_ipv6()

    def get_addresses_ipv4(self) -> Generator[IPv4Address, None, None]:
        for peer in self.peers:
            if peer.ipv4_address:
                yield peer.ipv4_address

    def get_addresses_ipv6(self) -> Generator[IPv6Address, None, None]:
        for peer in self.peers:
            if peer.ipv6_address:
                yield peer.ipv6_address

    def get_next_ipv4(self) -> IPv4Address:
        if not self.network_ipv4:
            raise ValueError("no IPv4 network specified")

        addresses = set(self.get_addresses_ipv4())
        for address in self.network_ipv4.hosts():
            if address in addresses:
                continue
            return address
        raise RuntimeError("all IPv4 addresses already taken")

    def get_next_ipv6(self) -> IPv6Address:
        if not self.network_ipv6:
            raise ValueError("no IPv6 network specified")

        addresses = set(self.get_addresses_ipv6())
        for address in self.network_ipv6.hosts():
            if address not in addresses:
                return address
        raise RuntimeError("all IPv6 addresses already taken")

    def get_peer(self, name: str) -> Peer | None:
        for peer in self.peers:
            if peer.hostname == name:
                return peer
        return None

    def get_connection(self, peer1: str, peer2: str) -> Connection | None:
        if peer1 > peer2:
            peer1, peer2 = peer2, peer1

        for connection in self.connections:
            if (connection.peer1 == peer1) and (connection.peer2 == peer2):
                return connection

        return None

    def get_connections_for_peer(self, peer: str) -> list[Connection]:
        connections: list[Connection] = []
        for connection in self.connections:
            if connection.peer1 == peer:
                connections.append(connection)
                continue
            if connection.peer2 == peer:
                connections.append(connection)
        return connections

    @staticmethod
    def load(path: Path) -> Config:
        yml = load_yaml_file(path)

        config = Config(
            IPv4Network(yml["ipv4_subnet"]) if yml.get("ipv4_subnet", None) else None,
            IPv6Network(yml["ipv6_subnet"]) if yml.get("ipv6_subnet", None) else None,
            default_port=yml["default_port"],
        )

        for hostname in yml["peers"]:
            config.peers.append(Peer.from_config_entry(yml["peers"][hostname]))

        for connection in yml["connections"]:
            config.connections.append(Connection.from_config_entry(connection))

        return config

    def save(self, path: Path):
        yml: dict[str, Any] = {"peers": {}, "default_port": self.default_port}

        if self.network_ipv4 is not None:
            yml["ipv4_subnet"] = str(self.network_ipv4)

        if self.network_ipv6 is not None:
            yml["ipv6_subnet"] = str(self.network_ipv6)

        for peer in self.peers:
            yml["peers"][peer.hostname] = peer.to_config_entry()

        yml["connections"] = []
        for connection in self.connections:
            yml["connections"].append(connection.to_config_entry())

        write_yaml_file(path, yml)
