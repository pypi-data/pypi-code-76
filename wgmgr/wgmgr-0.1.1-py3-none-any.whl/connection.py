from __future__ import annotations

from . import keygen


class Connection:
    def __init__(
        self,
        peer1: str,
        peer2: str,
        endpoint1: str | None = None,
        endpoint2: str | None = None,
        psk: str | None = None,
    ):
        self.peer1 = peer1
        self.peer2 = peer2
        self.endpoint1 = endpoint1
        self.endpoint2 = endpoint2

        if self.peer1 == self.peer2:
            raise ValueError("Both peers are identical!")

        if self.peer1 > self.peer2:
            self.peer1, self.peer2 = self.peer2, self.peer1
            self.endpoint1, self.endpoint2 = self.endpoint2, self.endpoint1

        self.psk = keygen.generate_psk() if psk is None else psk

    def regenerate_psk(self):
        self.psk = keygen.generate_psk()

    def to_config_entry(self) -> dict[str, str]:
        yml: dict[str, str] = {
            "peer1": self.peer1,
            "peer2": self.peer2,
            "psk": self.psk,
        }
        if self.endpoint1:
            yml["endpoint1"] = self.endpoint1
        if self.endpoint2:
            yml["endpoint2"] = self.endpoint2
        return yml

    @staticmethod
    def from_config_entry(entry: dict[str, str]) -> Connection:
        return Connection(
            entry["peer1"],
            entry["peer2"],
            entry.get("endpoint1"),
            entry.get("endpoint2", entry["psk"]),
        )
