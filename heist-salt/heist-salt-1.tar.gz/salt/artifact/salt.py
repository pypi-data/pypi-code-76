"""
    artifact module to manage the download of salt artifacts
"""
import aiohttp
import os
from distutils.version import LooseVersion
from distutils.version import StrictVersion


async def fetch(hub, session, url, download=False, location=False):
    """
    Fetch a url and return json. If downloading artifact
    return the download location.
    """
    async with session.get(url) as resp:
        if resp.status == 200:
            if download:
                with open(location, "wb") as fn_:
                    fn_.write(await resp.read())
                return location
            return await resp.json()
        hub.log.critical(f"Cannot query url {url}. Returncode {resp.status} returned")
        return False


async def version(hub, t_os):
    """
    Query latest version from repo if user does not define version
    """
    ver = hub.OPT["heist"].get("artifact_version")
    if ver:
        return ver

    url = "https://repo.saltproject.io/salt-bin/repo.json"
    async with aiohttp.ClientSession() as session:
        data = await hub.artifact.salt.fetch(session, url)
        if not data:
            hub.log.critical(
                f"Query to {url} failed, falling back to" f"pre-downloaded artifacts"
            )
            return False
        # we did not set version so query latest version from the repo
        for binary in data[t_os]:
            b_ver = data[t_os][binary]["version"]
            if not ver:
                ver = b_ver
                continue
            if LooseVersion(b_ver) > LooseVersion(ver):
                ver = b_ver
        return ver


async def get(
    hub, t_name: str, t_type: str, art_dir: str, t_os: str, ver: str = ""
) -> str:
    """
    Download artifact if does not already exist. If artifact
    version is not specified, download the latest from pypi
    """
    if ver:
        art_n = f"salt-{ver}"
    else:
        art_n = "salt"
    url = f"https://repo.saltstack.com/salt-bin/{t_os}/{art_n}"

    # TODO this needs to work for windows too
    # Ensure that artifact directory exists
    ret = await hub.tunnel[t_type].cmd(t_name, f"mkdir -p {art_dir}")
    assert not ret.returncode, ret.stderr
    location = os.path.join(art_dir, art_n)

    # check to see if artifact already exists
    if hub.artifact.salt.latest("salt", art_dir, version=ver):
        hub.log.info(f"The Salt artifact {ver} already exists")
        return location

    # download artifact
    async with aiohttp.ClientSession() as session:
        hub.log.info(f"Downloading the artifact {art_n} to {art_dir}")
        await hub.artifact.salt.fetch(session, url, download=True, location=location)

    # ensure artifact was downloaded
    if not os.path.isdir(art_dir):
        hub.log.critical(f"The target directory '{art_dir}' does not exist")
        return ""
    elif not any(ver in x for x in os.listdir(art_dir)):
        hub.log.critical(
            f"Did not find the {ver} artifact in {art_dir}."
            f" Untarring the artifact failed or did not include version"
        )
        return ""
    else:
        return location


def latest(hub, name: str, a_dir: str, version: str = "") -> str:
    """
    Given the artifacts directory return the latest desired artifact

    :param str version: Return the artifact for a specific version.
    """
    names = []
    paths = {}
    if not os.path.isdir(a_dir):
        return ""
    for fn in os.listdir(a_dir):
        if fn.startswith(name):
            ver = fn[len(name) + 1 :]
            names.append(ver)
            paths[ver] = fn
    names = sorted(names, key=StrictVersion)
    if version:
        if version in names:
            return os.path.join(a_dir, paths[version])
        else:
            return ""
    elif not paths:
        return ""
    else:
        return os.path.join(a_dir, paths[names[-1]])


async def deploy(hub, t_name: str, t_type: str, run_dir: str, bin_: str):
    """
    Deploy the salt minion to the remote system
    """
    tgt = os.path.join(run_dir, os.path.basename(bin_))
    root_dir = os.path.join(run_dir, "root")
    config = hub.heist.salt.minion.mk_config(root_dir, t_name)
    conf_dir = os.path.join(run_dir, "conf")
    conf_tgt = os.path.join(conf_dir, "minion")

    # run salt deployment
    ret = await hub.tunnel[t_type].cmd(t_name, f"mkdir -p {conf_dir}")
    assert not ret.returncode, ret.stderr
    ret = await hub.tunnel[t_type].cmd(t_name, f"mkdir -p {root_dir}")
    assert not ret.returncode, ret.stderr
    try:
        await hub.tunnel[t_type].send(t_name, config, conf_tgt)
    except Exception as e:
        hub.log.error(str(e))
        hub.log.error(f"Failed to send {config} to {t_name} at {conf_tgt}")
        os.remove(config)
    await hub.tunnel[t_type].send(t_name, bin_, tgt)
    await hub.tunnel[t_type].cmd(t_name, f"chmod +x {tgt}")
    os.remove(config)
    return tgt


async def clean(hub, t_name: str):
    run_dir = hub.heist.CONS[t_name]["run_dir"]
    t_type = hub.heist.CONS[t_name]["t_type"]
    pfile = os.path.join(run_dir, "pfile")
    await hub.tunnel[t_type].cmd(t_name, f"kill `cat {pfile}`")
    await hub.tunnel[t_type].cmd(t_name, f"rm -rf {run_dir}")
    await hub.heist.salt.minion.FUTURES[t_name]


async def start_command(hub, t_type: str, t_name, tgt, run_dir, pfile) -> str:
    """
    determine which command to use when starting the salt-minion
    """
    at_f = os.path.join(run_dir, "at-minion-scheduler.sh")
    startup = {
        "systemctl": {
            "conf_tgt": os.path.join(
                os.sep, "etc", "systemd", "system", "salt-minion.service"
            ),
            "conf": "systemd",
            "start_cmd": "systemctl start salt-minion",
        },
        "at": {
            "conf_tgt": at_f,
            "conf": "at",
            "start_cmd": f"at -f {at_f} now + 1 minute",
        },
    }
    if hub.heist.ROSTERS[t_name].get("bootstrap"):
        for cmd in startup:
            ret = await hub.tunnel[t_type].cmd(t_name, f"which {cmd}")
            if ret.returncode == 0:
                hub.log.debug(f"Using {cmd} to startup the minion service")
                config = hub.heist.salt.minion.mk_startup_conf(cmd, tgt, run_dir, pfile)
                conf_tgt = startup[cmd]["conf_tgt"]
                await hub.tunnel[t_type].send(t_name, config, conf_tgt)
                return startup[cmd]["start_cmd"]
    return (
        f' {tgt} minion --config-dir {os.path.join(run_dir, "conf")} --pid-file={pfile}'
    )
