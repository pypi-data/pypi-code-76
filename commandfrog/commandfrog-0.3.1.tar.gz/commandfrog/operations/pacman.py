from typing import List

from commandfrog.drivers.driver import Driver
from commandfrog.drivers.exceptions import CommandFailed

def pacman_install(host: Driver, packages: List[str]):
    try:
        host.exec(f"pacman -S {' '.join(packages)} --noconfirm", sudo=True)
    except CommandFailed as e:
        if "failed to initialize" in e.stderr.decode():
            # https://www.reddit.com/r/archlinux/comments/lek2ba/arch_linux_on_docker_ci_could_not_find_or_read/
            # https://github.com/qutebrowser/qutebrowser/commit/478e4de7bd1f26bebdcdc166d5369b2b5142c3e2
            host.exec('''patched_glibc=glibc-linux4-2.33-4-x86_64.pkg.tar.zst &&     curl -LO "https://repo.archlinuxcn.org/x86_64/$patched_glibc" &&     bsdtar -C / -xvf "$patched_glibc"''')
            host.exec("pacman -Syu --noconfirm", sudo=True)
            host.exec(f"pacman -S {' '.join(packages)} --noconfirm", sudo=True)

