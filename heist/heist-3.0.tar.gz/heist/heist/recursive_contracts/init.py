import getpass
from typing import Dict

DEFAULT_TUNNEL = "asyncssh"


async def sig_run(hub, remotes: Dict[str, Dict[str, str]]):
    ...


def _validate_remote(remote: Dict[str, str]):
    if not remote.get("tunnel"):
        remote["tunnel"] = DEFAULT_TUNNEL
    return remote


async def call_run(hub, ctx):
    kwargs = ctx.get_arguments()
    remotes = kwargs["remotes"]

    validate_remotes = {}
    for id_, remote in remotes.items():
        validate_remotes[id_] = _validate_remote(remote)
    return await ctx.func(kwargs["hub"], remotes=validate_remotes)
