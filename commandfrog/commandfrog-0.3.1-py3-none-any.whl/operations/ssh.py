from commandfrog.drivers.driver import Driver
from commandfrog.operations.files import is_regular_file, directory


def ssh_keyscan(host: Driver, hostname: str):
    directory(host, "~/.ssh")

    if not is_regular_file(host, "~/.ssh/known_hosts"):
        host.exec("touch ~/.ssh/known_hosts")

    if host.exec(f"ssh-keygen -F {hostname}", assert_ok=False).return_code != 0:
        host.exec(f'ssh-keyscan {hostname} >> ~/.ssh/known_hosts')



