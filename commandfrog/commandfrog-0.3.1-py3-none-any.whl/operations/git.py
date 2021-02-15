import re
from typing import Optional, List

from .files import directory, is_directory
from .apt import apt_install
from .ssh import ssh_keyscan

from commandfrog.drivers.driver import Driver
from commandfrog.operations.platform import get_platform
from commandfrog.drivers.exceptions import CommandFailed
from commandfrog.operations.pacman import pacman_install


def install_git(host: Driver):
    platform = get_platform(host)
    if platform == "ubuntu":
        apt_install(host, ["git"])
    elif platform == "arch":
        pacman_install(host, ["git"])


def repo(host: Driver, src: str, dest: str, ssh_key_path: Optional[str] = None):
    install_git(host)

    directory(host, dest)

    repo_path = src.split("/")[-1]
    assert repo_path.endswith(".git")
    repo_name = repo_path[0:-len(".git")]

    if is_directory(host, f"{dest}/{repo_name}"):
        return

    # Attempt to parse the domain from the git repository (stolen from pyinfra)
    domain = re.match(r'^[a-zA-Z0-9]+@([0-9a-zA-Z\.\-]+)', src)
    if domain:
        ssh_keyscan(host, domain.group(1))

    if ssh_key_path is not None:
        ssh_command_param = f'ssh -i {ssh_key_path}'
        host.exec(f"cd {dest} && git -c core.sshCommand='{ssh_command_param}' clone {src}")
    else:
        host.exec(f"cd {dest} && git clone {src}")

    if ssh_key_path is not None:
        host.exec(f"cd {dest}/{repo_name}; git config core.sshCommand '{ssh_command_param}'")




