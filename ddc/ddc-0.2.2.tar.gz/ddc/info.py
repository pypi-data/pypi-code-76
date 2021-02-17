import sys

from ddc.utils import exec_cmd

__version__ = "0.2.2"
__package_name__ = "ddc"


def print_about_version():
    print("Devision Developers Cli")  # noqa
    print("Version: " + __version__)  # noqa


def upgrade_pip_version_to_latest():
    _exitcode, out = exec_cmd(
        sys.executable + " -m pip install {} -U".format(__package_name__),
        print_exec_cmd=False,
    )
    print(out)  # noqa
    if not _exitcode:
        print("Update OK")  # noqa


def check_pip_version():
    _exitcode, latest_version = exec_cmd(
        sys.executable + " -m pip install {}==random".format(__package_name__),
        print_exec_cmd=False,
    )
    latest_version = latest_version[: latest_version.find(")")]
    latest_version = latest_version.replace(" ", "").split(",")[-1]

    if latest_version == __version__:
        return True
    else:
        return False


if __name__ == "__main__":
    print(__version__)  # noqa
