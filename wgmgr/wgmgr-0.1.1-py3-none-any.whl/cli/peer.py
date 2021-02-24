from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from wgmgr.config import Config
from wgmgr.peer import Peer
from wgmgr.util import validate_address_ipv4, validate_address_ipv6, validate_port

app = Typer()


@app.command()
def new(
    name: str = Argument(..., help="hostname for the new peer"),
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    ipv4: Optional[str] = Option(
        None,
        "-4",
        "--ipv4",
        help="IPv4 address of the new peer",
        callback=validate_address_ipv4,
    ),
    ipv6: Optional[str] = Option(
        None,
        "-6",
        "--ipv6",
        help="IPv6 address of the new peer",
        callback=validate_address_ipv6,
    ),
    port: Optional[int] = Option(
        None,
        "-p",
        "--port",
        help="port to use, will use config default if not specified",
        callback=validate_port,
    ),
    force: bool = Option(
        False, "-f", "--force", help="whether to overwrite existing hosts"
    ),
):
    config = Config.load(path)

    if (config.get_peer(name) is not None) and (not force):
        raise RuntimeError(f'peer "{name}" exists, use -f/--force to overwrite')

    if (
        (config.network_ipv4 is None)
        and (ipv4 is None)
        and (config.network_ipv6 is None)
        and (ipv6 is None)
    ):
        raise RuntimeError(
            "Config does not contain a IPv4 or IPv6"
            "and no address specified through -4/--ipv4 and -6/--ipv6"
        )

    peer = Peer(name)
    if port is not None:
        peer.port = port
        peer.port_auto = False
    else:
        peer.port = config.default_port
        peer.port_auto = True

    if ipv4 is not None:
        peer.ipv4_address = IPv4Address(ipv4)
        peer.ipv4_auto = False
    elif config.network_ipv4 is not None:
        peer.ipv4_address = config.get_next_ipv4()
        peer.ipv4_auto = True

    if ipv6 is not None:
        peer.ipv6_address = IPv6Address(ipv6)
        peer.ipv6_auto = False
    elif config.network_ipv6 is not None:
        peer.ipv6_address = config.get_next_ipv6()
        peer.ipv6_auto = True

    config.peers.append(peer)

    config.save(path)


@app.command()
def list(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path to the config file",
    )
):
    config = Config.load(path)
    for peer in config.peers:
        print(peer.to_config_entry())


if __name__ == "__main__":
    app()
