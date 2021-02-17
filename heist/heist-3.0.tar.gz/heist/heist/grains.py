import asyncio
import copy
import json
import secrets
from pathlib import Path
from typing import Dict, Tuple


async def run(hub, remotes: Dict[str, Dict[str, str]]):
    coros = []
    for id_, remote in remotes.items():
        coro = hub.heist.grains.single(id_, remote)
        coros.append(coro)
    results = await asyncio.gather(*coros, loop=hub.pop.Loop, return_exceptions=False)
    print(hub.output.nested.display(dict(results)))


async def single(hub, id_: str, remote: Dict[str, str]):
    """
    Run a single instance of grain collection
    :param id_: The id of the target, this helps turn the results of asyncio.gather into a dictionary from `run`
    :param remote: Information about the target to run on
    """
    try:
        ret = await hub.heist.grains.get(remote)
    except Exception as e:
        hub.log.error(e)
        return id_, {}
    return id_, ret


async def os_arch(hub, target_name: str, tunnel_plugin: str) -> Tuple[str, str]:
    """
    Download artifact if does not already exist.
    """
    DELIM = "|||"
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f'echo "$OSTYPE{DELIM}$MACHTYPE{DELIM}%PROCESSOR_ARCHITECTURE%"'
    )
    assert not ret.returncode, ret.stderr
    kernel, arch, winarch = ret.stdout.lower().split(DELIM, maxsplit=2)

    if "linux" in kernel:
        kernel = "linux"
        if "64" in arch:
            os_arch = "amd64"
        else:
            os_arch = "i386"
    elif "darwin" in kernel:
        kernel = "darwin"
        if "64" in arch:
            os_arch = "darwin64"
        else:
            os_arch = "darwin32"
    elif "bsd" in kernel:
        kernel = "bsd"
        if "64" in arch:
            os_arch = "amd64"
        else:
            os_arch = "i386"
    elif winarch:
        kernel = "windows"
        if "64" in winarch:
            os_arch = "win64"
        else:
            os_arch = "win32"
    else:
        raise ValueError(
            f"Could not determine arch from kernel: {kernel} arch: {arch} winarch: {winarch}"
        )
    hub.log.debug(f'Detected arch "{os_arch}" on target')
    return kernel, os_arch


async def get(
    hub, remote: Dict[str, str], version: int = 2, target_name: str = None
) -> Dict[str, str]:
    # Create tunnel
    tunnel_plugin = remote["tunnel"]
    if not target_name:
        target_name = secrets.token_hex()
        hub.heist.ROSTERS[target_name] = copy.copy(remote)
        created = await hub.tunnel[tunnel_plugin].create(target_name, remote)
        if not created:
            hub.log.error(f"Connection to host {remote.host} failed")
            return hub.pop.data.imap()

    # Get os arch info
    target_kernel, target_os_arch = await hub.heist.grains.os_arch(
        target_name, remote.tunnel
    )

    # Deploy "grainsv2" on the target system
    user = hub.heist.ROSTERS[target_name].get("username")
    if not user:
        user = hub.heist.init.default(target_kernel, "user")

    local_artifact_dir = hub.heist.init.default("default", "os_path")
    remote_artifact_dir = (
        Path(local_artifact_dir + f"_{user}") / f"{secrets.token_hex()[:4]}"
    )

    target_grains_bin = await hub.artifact.grains.deploy(
        target_name,
        tunnel_plugin,
        target_os_arch,
        version,
        remote_artifact_dir,
        local_artifact_dir,
    )

    hub.heist.CONS[target_name] = {"run_dir": remote_artifact_dir}

    # Run the grains command
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"{target_grains_bin} --output=json --timeout=10"
    )

    await hub.artifact.grains.clean(
        target_name, tunnel_plugin, remote_artifact_dir, target_os_arch, version
    )

    # Turn the grains output into json format
    assert not ret.returncode, ret.stderr

    remote_grains = json.loads(ret.stdout)
    return hub.pop.data.imap(remote_grains)
