from commandfrog.drivers.driver import Driver


def get_ubuntu_codename(host: Driver):
    """
    Return "focal", "groovy" etc.
    """
    return host.exec("lsb_release -cs").stdout.decode().strip()



