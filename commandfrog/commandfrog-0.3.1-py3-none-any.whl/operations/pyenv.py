from typing import List

from commandfrog.drivers.driver import Driver

from .apt import apt_install
from .files import is_regular_file, exists, link
from .shell import get_shell_rc_file
from .pacman import pacman_install


def install_pyenv(host: Driver):
    if is_regular_file(host, "~/.pyenv/bin/pyenv"):
        return

    # If you don't have tzdata setup, consult the web service at
    # ipapi.co/timezone to get the correct time zone and put it in
    # /etc/localtime. Otherwise installing the following packages would
    # interactively prompt for your time zone.
    # https://stackoverflow.com/a/63153978/223486
    if not exists(host, "/etc/localtime"):
        host.exec("ln -snf /usr/share/zoneinfo/$(curl https://ipapi.co/timezone) /etc/localtime")

    if host.platform == "ubuntu":
        apt_install(host, [
            # Required to install pyenv itself
            "curl",
            "git",

            # Required to use pyenv to install Python versions
            "build-essential",
            "libssl-dev",
            "zlib1g-dev",
            "libbz2-dev",
            "libreadline-dev",
            "libsqlite3-dev",
            "llvm",
            "libncurses5-dev",
            "libncursesw5-dev",
            "xz-utils",
            "tk-dev",
            "libffi-dev",
            "liblzma-dev",

            # Possibly was required for earlier versions of Ubuntu? Doesn't seem to
            # exist anymore and we seem to be fine without it.
            #"python-openssl",
        ])
    elif host.platform == "arch":
        pacman_install(host, ["git", "base-devel"])
    else:
        raise ValueError("Don't know what to install on this platform")

    host.exec("curl https://pyenv.run |bash")


def pyenv_install_rc(host: Driver):
    lines = [
        'export PATH="$HOME/.pyenv/bin:$PATH"',
        'eval "$(pyenv init -)"',
        'eval "$(pyenv virtualenv-init -)"',
    ]
    rc_file = get_shell_rc_file(host)
    if rc_file is not None:
        if host.exec(f"grep pyenv {rc_file}", assert_ok=False).return_code != 0:
            host.exec_as_script("\n".join([
                f"cat >> {rc_file} <<'EOF'",
                *lines,
                "EOF",
            ]))


def pyenv_install(host: Driver, python_version: str):
    install_pyenv(host)

    if python_version in host.exec("~/.pyenv/bin/pyenv versions --bare").stdout.decode():
        return

    host.exec(f"~/.pyenv/bin/pyenv install {python_version}")


def pyenv_virtualenv(host: Driver, python_version: str, virtualenv_name: str):
    install_pyenv(host)

    if (
        f"{python_version}/envs/{virtualenv_name}"
        in host.exec("~/.pyenv/bin/pyenv virtualenvs --bare", echo_stdout=False).stdout.decode().splitlines()
    ):
        return

    pyenv_install(host, python_version)
    host.exec(f"~/.pyenv/bin/pyenv virtualenv {python_version} {virtualenv_name}")


def pip_install(
    host: Driver,
    python_version: str,
    virtualenv_name: str,
    what_to_install: str,
    editable: bool = False
) -> None:
    host.exec_as_script("\n".join([
        'export PATH="$HOME/.pyenv/bin:$PATH"',
        'eval "$(pyenv init -)"',
        'eval "$(pyenv virtualenv-init -)"',
        f"pyenv activate {virtualenv_name}",
        f"pip install {'-e' if editable else ''} {what_to_install}"
    ]))


def install_python_app(
    host: Driver,
    python_version: str,
    virtualenv_name: str,
    install_cmd: str,
    binaries: List[str]
):
    pyenv_virtualenv(host, python_version, virtualenv_name)

    host.exec_as_script(f"""
        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        pyenv activate {python_version}/envs/{virtualenv_name}
        {install_cmd}
    """)

    for b in binaries:
        link(host, link_name=f"~/bin/{b}", target=f"{virtualenv_dir(python_version, virtualenv_name)}/bin/{b}")


def virtualenv_dir(python_version: str, virtualenv_name: str) -> str:
    return f"~/.pyenv/versions/{python_version}/envs/{virtualenv_name}"
