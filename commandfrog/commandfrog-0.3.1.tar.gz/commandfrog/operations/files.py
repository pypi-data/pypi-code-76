from commandfrog.drivers.driver import Driver


def exists(host: Driver, path: str):
    if host.exec(f"test -e {path}", assert_ok=False).return_code == 0:
        return True
    elif host.exec(f"test -L {path}", assert_ok=False).return_code == 0:
        return True
    else:
        return False


def is_directory(host: Driver, path: str):
    return host.exec(f"test -d {path}", assert_ok=False).return_code == 0


def is_regular_file(host: Driver, path: str):
    return host.exec(f"test -f {path}", assert_ok=False).return_code == 0


def directory(host: Driver, path: str):
    if not is_directory(host, path):
        host.exec(f"mkdir -p {path}")


def link(host: Driver, target: str, link_name: str):
    if host.exec(f"[ $(readlink -f $(realpath {link_name})) = $(realpath {target}) ]", assert_ok=False).return_code == 0:
        return

    if exists(host, link_name):
        host.exec(f"rm {link_name}")

    host.exec(f"ln -s {target} {link_name}")

