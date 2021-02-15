from commandfrog.drivers.driver import Driver
from commandfrog.drivers.exceptions import CommandFailed
from typing import List


def init_apt(host: Driver):
    if host.exec("ls /var/lib/apt/lists/* > /dev/null", assert_ok=False).return_code != 0:
        apt_update(host)


def apt_update(host: Driver):
    host.exec("apt-get update -y", sudo=host.has_sudo)


def apt_install(host: Driver, packages: List[str]):
    installed_packages = host.exec(
        "dpkg --get-selections |grep -v deinstall |cut -f 1",
        echo_stdout=False,
        echo_stderr=False,
    ).stdout.splitlines()
    packages_to_install = set(packages) - set(installed_packages)
    if packages_to_install:
        try:
            host.exec(f"apt-get install -y {' '.join(packages_to_install)}", sudo=host.has_sudo)
        except CommandFailed as e:
            if "Unable to locate package" in e.stderr.decode():
                apt_update(host)
                host.exec(f"apt-get install -y {' '.join(packages_to_install)}", sudo=host.has_sudo)

