import os
from pathlib import Path


async def disable(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"systemctl disable {service}"
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def enable(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"systemctl enable {service}"
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def start(hub, tunnel_plugin, target_name, service, block=True):
    cmd = [f"systemctl start {service}"]
    if not block:
        cmd.append("--no-block")
    ret = await hub.tunnel[tunnel_plugin].cmd(target_name, " ".join(cmd))
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def stop(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(target_name, f"systemctl stop {service}")
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


async def restart(hub, tunnel_plugin, target_name, service):
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"systemctl restart {service}"
    )
    if ret.exit_status != 0:
        hub.log.error(ret.stderr)
        return False
    return True


def conf_path(hub, service_name):
    return Path(os.sep, "etc", "systemd", "system", f"{service_name}.service")


async def clean(hub, target_name, tunnel_plugin):
    await hub.tunnel[tunnel_plugin].cmd(target_name, f"systemctl daemon-reload")
