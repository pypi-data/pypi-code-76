"""
The entry point for Heist, this is where config loading and the project
spine is set up
"""
import asyncio
from dict_tools.data import NamespaceDict
import ipaddress
import socket
from typing import Any


def __init__(hub):
    hub.heist.CONS = {}
    hub.heist.ROSTERS = {}
    hub.heist.init.load_subs()
    hub.heist.OS_DEFAULTS = _get_defaults()


def _get_defaults():
    return {
        "linux": {"os_path": "/var/tmp/heist", "user": "root",},
        "windows": {"os_path": "C:\\heist\\tmp", "user": "Administrator",},
        "default": {"os_path": "/var/tmp/heist", "user": "root",},
    }


def default(hub, target_os: str, key: str) -> Any:
    os_defaults = hub.heist.OS_DEFAULTS.get(target_os)
    if not os_defaults:
        value = None
        hub.log.error(f"OS '{target_os}' not defined in hub.heist.OS_DEFAULTS")
    else:
        value = os_defaults.get(key)

    if not value:
        hub.log.error(f"No {target_os}-specific default for {key}, using fallback")
        value = hub.heist.OS_DEFAULTS["default"].get(key)

    return value


def load_subs(hub):
    """
    Load up the needed subs
    """
    hub.pop.sub.load_subdirs(hub.heist, recurse=True)
    for dyne in ("acct", "artifact", "rend", "roster", "service", "tunnel"):
        hub.pop.sub.add(dyne_name=dyne)
    hub.pop.sub.load_subdirs(hub.service, recurse=True)


def start(hub):
    """
    Start the async loop and get the process rolling
    """
    # hub.pop.conf.integrate(["heist", "acct"], cli="heist", roots=True)
    hub.pop.config.load(["heist", "acct"], cli="heist")
    hub.pop.loop.start(
        hub.heist.init.run_remotes(hub.SUBPARSER),
        sigint=hub.heist.init.clean,
        sigterm=hub.heist.init.clean,
    )


async def run_remotes(hub, manager: str):
    """
    Configs, rosters and targets have been loaded, time to execute the
    remote system calls
    """
    raw_remotes = await hub.roster.init.read(hub.OPT.heist.roster)
    remotes = NamespaceDict()
    for k, v in raw_remotes.items():
        remotes[k] = NamespaceDict(v)
    if not remotes:
        return False

    hub.log.debug(f"Heist manager is '{manager}'")
    ret = hub.heist[manager].run(remotes)
    if asyncio.iscoroutine(ret):
        await ret


async def clean(hub, signal: int = None):
    """
    Clean up the connections
    """
    if signal:
        hub.log.warning(f"Got signal {signal}! Cleaning up connections")
    coros = []
    # First clean up the remote systems
    for _, r_vals in hub.heist.ROSTERS.items():
        if not r_vals.get("bootstrap"):
            for t_name, vals in hub.heist.CONS.items():
                manager = vals["manager"]
                coros.append(
                    hub.heist[manager].clean(
                        t_name,
                        vals["t_type"],
                        service_plugin=vals.get("service_plugin"),
                    )
                )
                await asyncio.gather(*coros)
    # Then shut down connections
    coros = []
    for t_name, vals in hub.heist.CONS.items():
        t_type = vals["t_type"]
        coros.append(hub.tunnel[t_type].destroy(t_name))
    await asyncio.gather(*coros)
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        hub.log.warning(
            "Task remains that were not cleaned up, shutting down violently"
        )
        task.cancel()


def ip_is_loopback(hub, addr):
    """
    helper function to determine if an addr
    or hostname is a loopback address
    """
    try:
        info = socket.getaddrinfo(addr, 0)
    except socket.gaierror:
        hub.log.critical("Could not determine if addr is loopback")
        return False
    return ipaddress.ip_address(info[0][-1][0]).is_loopback
