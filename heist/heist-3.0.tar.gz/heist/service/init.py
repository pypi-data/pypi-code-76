async def disable(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].disable(
        tunnel_plugin, target_name, service
    )


async def enable(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].enable(
        tunnel_plugin, target_name, service
    )


async def start(hub, tunnel_plugin, target_name, service, **kwargs):
    await hub.service[hub.OPT.heist.service_plugin].start(
        tunnel_plugin, target_name, service, **kwargs
    )


async def stop(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].stop(
        tunnel_plugin, target_name, service
    )


async def restart(hub, tunnel_plugin, target_name, service):
    await hub.service[hub.OPT.heist.service_plugin].restart(
        tunnel_plugin, target_name, service
    )


def get_service_plugin(hub, remote=None, grains=None):
    if not grains:
        grains = {}

    if not remote:
        remote = {}

    if "init_system" in remote:
        service_plugin = remote["init_system"]
    elif hub.OPT.heist.get("service_plugin"):
        service_plugin = hub.OPT.heist.get("service_plugin")
    elif "init" in grains:
        service_plugin = grains.init
    else:
        service_plugin = "systemd"
    return service_plugin


def service_conf_path(hub, service_name, service_plugin=None):
    if not service_plugin:
        service_plugin = hub.service.init.get_service_plugin()
    conf_path = hub.service[service_plugin].conf_path(service_name)
    if not conf_path:
        return ""
    return conf_path


async def clean(hub, target_name, tunnel_plugin, service_name, service_plugin):
    # stop service
    await hub.service[hub.heist.CONS[target_name]["service_plugin"]].stop(
        tunnel_plugin, target_name, service_name
    )

    await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"rm -rf {hub.service.init.service_conf_path(service_name)}"
    )

    await hub.service[service_plugin].clean(target_name, tunnel_plugin)
