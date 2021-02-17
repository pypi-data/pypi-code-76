def __init__(hub):
    hub.artifact.ACCT = ["artifact"]


def get(hub):
    # TODO Determine which artifact to use, find the right plugin, and execute it's get function
    ...


def version(hub):
    # TODO Determine which artifact to use, find the right plugin, and find out the target's version of the artifact
    ...


def deploy(hub):
    # TODO Determine which artifact to use, find the right plugin, and execute it's deploy function
    ...


async def clean(hub, target_name, tunnel_plugin):
    """
    Clean up the deployed artifact and files
    """

    # remove run directory
    await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"rm -rf {hub.heist.CONS[target_name]['run_dir']}"
    )
