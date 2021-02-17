"""
    artifact module to manage the download of grains artifacts
"""
import aiohttp
import hashlib
import os
import tempfile

__virtualname__ = "grains"


def checksum(hub, local_file_path: str) -> str:
    md5 = hashlib.md5()

    if os.path.exists(local_file_path):
        with open(local_file_path, "rb") as fd:
            for line in fd:
                md5.update(line)

    return md5.hexdigest()


async def version(hub, t_os):
    # Detect the version of the binary on the target
    ...


async def get(hub, t_name: str, t_type: str, art_dir: str, t_os: str, ver: str = None):
    """
    Fetch a url return the download location.
    """
    os.makedirs(art_dir, exist_ok=True)

    artifact_url = f"http://artifactory.saltstack.net/artifactory/open-production/grains/{t_os}/{ver}/grains"

    async with aiohttp.ClientSession() as session:
        async with session.get(artifact_url) as response:
            local_grains_bin = os.path.join(
                art_dir, f"{response.url.name}-{ver}-{t_os}"
            )
            hub.log.info(f"Downloading binary to: {local_grains_bin}")
            if hub.artifact.grains.checksum(local_grains_bin) == response.headers.get(
                "X-Checksum-Md5"
            ):
                return local_grains_bin

            with open(local_grains_bin, "wb") as fd:
                async for data in response.content.iter_chunked(1024):
                    fd.write(data)
                os.chmod(local_grains_bin, 0o644)
    return local_grains_bin


async def deploy(
    hub,
    t_name: str,
    t_type: str,
    t_os: str,
    ver: str,
    remote_artifact_dir: str,
    local_artifact_dir: str,
):
    remote = hub.heist.ROSTERS[t_name]

    # Deploy "grainsv2" on the target systems
    local_grains_bin = await hub.artifact.grains.get(
        remote["id"], t_type, local_artifact_dir, t_os, ver=ver
    )
    target_grains_bin = os.path.join(remote_artifact_dir, "grains")
    ret = await hub.tunnel[t_type].cmd(t_name, f"mkdir -p {remote_artifact_dir}")
    assert not ret.returncode, ret.stderr

    # TODO do a checksum, or check the local version of the binary and the remote version (if it exists) to see if a replacement is necessary

    # Deploy "grainsv2" on the target system
    await hub.tunnel[t_type].send(t_name, local_grains_bin, target_grains_bin)

    if "win" not in local_grains_bin:
        hub.log.debug("Not on windows, making the bin executable")
        await hub.tunnel[t_type].cmd(t_name, f"chmod +x {target_grains_bin}")
    return target_grains_bin


async def clean(hub, t_name: str, t_type: str, art_dir: str, t_os: str, ver: str):
    target_dir = hub.heist.init.default("default", "os_path")
    target_grains_bin = os.path.join(target_dir, "grains")
    if "win" in t_os:
        await hub.tunnel[t_type].cmd(t_name, f"del {target_grains_bin}")
    else:
        await hub.tunnel[t_type].cmd(t_name, f"rm {target_grains_bin}")
