from pathlib import Path
from typing import Optional

from typer import Option, Typer

from wgmgr.config import Config
from wgmgr.connection import Connection

app = Typer()


@app.command()
def new(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    peer1: str = Option(..., "-p1", "--peer1", help="first peer of the connection"),
    peer2: str = Option(..., "-p2", "--peer2", help="second peer of the connection"),
    endpoint1: Optional[str] = Option(
        None, "-e1", "--endpoint1", help="peer1 endpoint (domain/address) if applicable"
    ),
    endpoint2: Optional[str] = Option(
        None, "-e2", "--endpoint2", help="peer2 endpoint (domain/address) if applicable"
    ),
    force: bool = Option(
        False, "-f", "--force", help="whether to overwrite existing connection"
    ),
):
    config = Config.load(path)

    if config.get_peer(peer1) is None:
        raise RuntimeError(f'no peer named "{peer1}"')

    if config.get_peer(peer2) is None:
        raise RuntimeError(f'no peer named "{peer2}"')

    if config.get_connection(peer1, peer2) and not force:
        raise RuntimeError(
            f'connection between "{peer1}" and "{peer2}" exists, '
            "use -f/--force to overwrite"
        )

    connection = Connection(peer1, peer2, endpoint1, endpoint2)
    config.connections.append(connection)

    config.save(path)
