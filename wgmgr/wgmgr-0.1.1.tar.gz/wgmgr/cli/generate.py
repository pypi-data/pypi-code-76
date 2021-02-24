from pathlib import Path

from typer import Argument, Option, Typer

from wgmgr.config import Config
from wgmgr.templates import load_template

app = Typer()


@app.command()
def wg_quick(
    path: Path = Option(
        ...,
        "-c",
        "--config",
        envvar="WGMGR_CONFIG",
        help="path of the config file",
    ),
    peer: str = Argument(..., help="peer to generate config for"),
):
    config = Config.load(path)

    if config.get_peer(peer) is None:
        raise RuntimeError(f'no peer named "{peer}"')

    template = load_template("wg-quick.conf.j2")
    generated = template.render(peer_name=peer, config=config)

    print(generated)
