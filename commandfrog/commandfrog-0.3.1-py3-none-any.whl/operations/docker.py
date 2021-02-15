from commandfrog.drivers.driver import Driver
from .apt import apt_install
from .files import is_regular_file
from .ubuntu import get_ubuntu_codename
from .pacman import pacman_install


def install_docker(host: Driver, client_only: bool = False):
    if host.exec("which docker", assert_ok=False).return_code == 0:
        return

    if host.platform == "ubuntu":
        apt_install(host, ["apt-transport-https", "ca-certificates", "curl", "gnupg-agent", "software-properties-common"])
        host.exec("sh -c 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -'", sudo=True)

        ubuntu_codename = get_ubuntu_codename(host)
        if ubuntu_codename == "groovy":
            # Currenty groovy (Ubuntu 20.10) doesn't have packages in this repo,
            # but we can fall back to focal and everything seems to work.
            ubuntu_codename = "focal"

        host.exec(f'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu {ubuntu_codename} stable" -y', sudo=True)
        host.exec("apt-get update -y", sudo=True)
        if client_only:
            apt_install(host, ["docker-ce-cli"])
        else:
            apt_install(host, ["docker-ce", "docker-ce-cli", "containerd.io"])
            host.exec("service docker start", sudo=True)

        if host.exec("whoami").stdout.decode().strip() != "root":
            host.exec("usermod -aG docker $USER", sudo=True)
    elif host.platform == "arch":
        pacman_install(host, ["docker"])
        if not client_only:
            host.exec("systemctl start docker.service", sudo=True)
            host.exec("systemctl start docker.service", sudo=True)
    else:
        raise ValueError("Don't know how to install Docker on this platform")


def install_docker_compose(host: Driver):
    if is_regular_file(host, "/usr/local/bin/docker-compose"):
        return

    apt_install(host, ["curl"])

    host.exec(
        'curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)"'
        ' -o /usr/local/bin/docker-compose',
        sudo=host.has_sudo
    )
    user = host.exec("whoami").stdout.decode().strip()
    host.exec(f"chown {user} /usr/local/bin/docker-compose", sudo=host.has_sudo)
    host.exec("chmod +x /usr/local/bin/docker-compose")



