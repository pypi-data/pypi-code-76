import asyncio
import copy
import os
import pathlib
import secrets
import tempfile
from typing import Any, Dict

CONFIG = """master: {master}
master_port: {master_port}
publish_port: {publish_port}
root_dir: {root_dir}
"""


async def run(hub, remotes: Dict[str, Dict[str, str]]):
    coros = []
    for id_, remote in remotes.items():
        coro = hub.heist.salt.minion.single(remote)
        coros.append(coro)
    await asyncio.gather(*coros, loop=hub.pop.Loop, return_exceptions=False)


def mk_config(hub, root_dir: str, t_name):
    """
    Create a minion config to use with this execution and return the file path
    for said config
    """
    _, path = tempfile.mkstemp()
    roster = hub.heist.ROSTERS[t_name]
    master = roster.get("master", "127.0.0.1")

    with open(path, "w+") as wfp:
        wfp.write(
            CONFIG.format(
                master=master,
                master_port=roster.get("master_port", 44506),
                publish_port=roster.get("publish_port", 44505),
                root_dir=root_dir,
            )
        )
    return path


async def single(hub, remote: Dict[str, Any]):
    """
    Execute a single async connection
    """
    # create tunnel
    target_name = secrets.token_hex()
    hub.heist.ROSTERS[target_name] = copy.copy(remote)
    t_type = remote.get("tunnel", "asyncssh")
    created = await hub.tunnel[t_type].create(target_name, remote)
    if not created:
        hub.log.error(f'Connection to host {remote["host"]} failed')
        return

    t_grains = await hub.heist.grains.get(remote, target_name=target_name)
    t_os = t_grains.kernel.lower()

    # create artifacts directory
    artifact_dir = pathlib.Path(hub.OPT["heist"]["artifacts_dir"]) / t_os
    pathlib.Path(artifact_dir).mkdir(parents=True, exist_ok=True)

    ver = await hub.artifact.salt.version(t_os)
    if ver:
        await hub.artifact.salt.get(target_name, t_type, artifact_dir, t_os, ver=ver)

    # Get salt minion user
    user = hub.heist.ROSTERS[target_name].get("username")
    if not user:
        user = hub.heist.init.default(t_os, "user")

    run_dir = hub.heist.CONS[target_name].get("run_dir")
    if not run_dir:
        run_dir = (
            pathlib.Path(os.sep, "var")
            / "tmp"
            / f"heist_{user}"
            / f"{secrets.token_hex()[:4]}"
        )
        hub.heist.CONS[target_name]["run_dir"] = run_dir

    # Deploy
    bin_ = hub.artifact.salt.latest("salt", artifact_dir, version=ver)
    tgt = await hub.artifact.salt.deploy(target_name, t_type, run_dir, bin_)
    service_plugin = hub.service.init.get_service_plugin(remote, t_grains)

    hub.heist.CONS[target_name].update(
        {
            "t_type": t_type,
            "manager": "salt.minion",
            "bin": bin_,
            "tgt": tgt,
            "service_plugin": service_plugin,
        }
    )

    # Create tunnel back to master
    if not hub.heist.ROSTERS[target_name].get("bootstrap"):
        await hub.tunnel[t_type].tunnel(target_name, 44505, 4505)
        await hub.tunnel[t_type].tunnel(target_name, 44506, 4506)

    # Start minion
    hub.log.debug(f"Target '{remote.id}' is using service plugin: {service_plugin}")
    await hub.service.salt.minion.apply_service_config(
        t_type, target_name, run_dir, tgt, service_plugin
    )
    await hub.service[service_plugin].start(
        t_type, target_name, "salt-minion", block=False
    )

    if hub.OPT.heist.get("accept_keys", False):
        await hub.salt.key.init.accept_key_master(target_name, t_type, tgt, run_dir)

    hub.log.debug(
        f"Starting infinite loop on {remote.id}.  Checkin time: {hub.OPT.heist.checkin_time}"
    )

    while True:
        await asyncio.sleep(hub.OPT.heist.checkin_time)
        if hub.OPT.heist.dynamic_upgrade:
            latest = hub.artifact.salt.latest("salt", artifact_dir)
            if latest != bin_:
                bin_ = latest
                await hub.artifact.salt.update(
                    target_name, t_type, latest, tgt, run_dir
                )


async def clean(hub, target_name, tunnel_plugin, service_plugin):
    """
    Clean up the connections
    """
    # clean up service files
    await hub.service.init.clean(
        target_name, tunnel_plugin, "salt-minion", service_plugin
    )
    # clean up run directory and artifact
    await hub.artifact.init.clean(target_name, tunnel_plugin)

    minion_id = hub.heist.CONS[target_name].get("minion_id")
    if minion_id:
        if not hub.salt.key.init.delete_minion(minion_id):
            hub.log.error(f"Could not delete the key for minion: {minion_id}")
