from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import cast

from . import keygen


class Peer:
    def __init__(
        self,
        hostname: str,
        private_key: str | None = None,
        public_key: str | None = None,
    ):
        self.hostname: str = hostname
        self.private_key = (
            keygen.generate_private_key() if private_key is None else private_key
        )
        self.public_key = (
            keygen.generate_public_key(self.private_key)
            if public_key is None
            else public_key
        )
        self.ipv4_address: IPv4Address | None = None
        self.ipv4_auto: bool | None = None
        self.ipv6_address: IPv6Address | None = None
        self.ipv6_auto: bool | None = None
        self.port: int | None = None
        self.port_auto: bool | None = None

    def get_addresses(self) -> list[IPv4Address | IPv6Address]:
        result: list[IPv4Address | IPv6Address] = []
        if self.ipv4_address:
            result.append(self.ipv4_address)
        if self.ipv6_address:
            result.append(self.ipv6_address)
        return result

    def get_addresses_str(self):
        return [str(addr) for addr in self.get_addresses()]

    def regenerate_key(self):
        self.private_key = keygen.generate_private_key()
        self.public_key = keygen.generate_public_key(self.private_key)

    def to_config_entry(self) -> dict[str, str | bool | int]:
        yml: dict[str, str | bool | int] = {
            "hostname": self.hostname,
            "private_key": self.private_key,
            "public_key": self.public_key,
        }

        if self.ipv4_address is not None:
            yml["ipv4"] = str(self.ipv4_address)

        if self.ipv4_auto is not None:
            yml["ipv4_auto"] = self.ipv4_auto

        if self.ipv6_address is not None:
            yml["ipv6"] = str(self.ipv6_address)

        if self.ipv6_auto is not None:
            yml["ipv6_auto"] = self.ipv6_auto

        if self.port is not None:
            yml["port"] = self.port

        if self.port_auto is not None:
            yml["port_auto"] = self.port_auto

        return yml

    @staticmethod
    def from_config_entry(entry: dict[str, str | bool | int]) -> Peer:
        peer = Peer(
            str(entry["hostname"]), str(entry["private_key"]), str(entry["public_key"])
        )

        peer.ipv4_address = IPv4Address(entry["ipv4"]) if "ipv4" in entry else None
        peer.ipv4_auto = cast(bool, entry.get("ipv4_auto", None))
        peer.ipv6_address = IPv6Address(entry["ipv6"]) if "ipv6" in entry else None
        peer.ipv6_auto = cast(bool, entry.get("ipv6_auto", None))
        peer.port = cast(int, entry.get("port", None))
        peer.port_auto = cast(bool, entry.get("port_auto", None))

        return peer
