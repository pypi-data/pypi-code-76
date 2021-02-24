import subprocess
from ipaddress import IPv4Network, IPv6Network
from pathlib import Path
from typing import Optional

from typer import Argument, Option, Typer

from wgmgr import util
from wgmgr.config import Config

app = Typer()
app_set = Typer()
app.add_typer(app_set, name="set")


@app.command()
def new(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    ipv4_subnet: Optional[str] = Option(
        None, "-4", "--ipv4", help="IPv4 subnet", callback=util.validate_subnet_ipv4
    ),
    ipv6_subnet: Optional[str] = Option(
        None, "-6", "--ipv6", help="IPv6 subnet", callback=util.validate_subnet_ipv6
    ),
    port: int = Option(
        51902,
        "-p",
        "--port",
        help="default port for new peers",
        callback=util.validate_port,
    ),
    force: bool = Option(
        False, "-f", "--force", help="whether to overwrite existing config file"
    ),
):
    """Create a new, empty config."""

    if path.exists() and not force:
        raise RuntimeError(
            f'config file "{path}" exists, ' "use -f/--force to overwrite"
        )

    config = Config(
        IPv4Network(ipv4_subnet) if ipv4_subnet else None,
        IPv6Network(ipv6_subnet) if ipv6_subnet else None,
        port,
    )
    config.save(path)


@app.command()
def edit(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    )
):
    editor = util.get_editor()
    subprocess.run([str(editor), str(path)])


@app_set.command()
def default_port(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    port: int = Argument(
        ..., help="default port for peers", callback=util.validate_port
    ),
):
    """Set default port updating all peers that do not have a fixed port."""
    config = Config.load(path)
    config.update_default_port(port)
    config.save(path)


@app_set.command()
def ipv4_subnet(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    subnet: str = Argument(
        ..., help="IPv4 subnet in CIDR notation", callback=util.validate_subnet_ipv4
    ),
):
    """Set IPv4 subnet and update addresses accordingly."""
    config = Config.load(path)
    config.update_ipv4_subnet(IPv4Network(subnet))
    config.save(path)


@app_set.command()
def ipv6_subnet(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    subnet: str = Argument(
        ..., help="IPv6 subnet in CIDR notation", callback=util.validate_subnet_ipv6
    ),
):
    """Set IPv6 subnet and update addresses accordingly."""
    config = Config.load(path)
    config.update_ipv6_subnet(IPv6Network(subnet))
    config.save(path)


if __name__ == "__main__":
    app()
