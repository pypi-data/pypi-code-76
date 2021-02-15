import functools


@functools.lru_cache
def get_platform(host) -> str:
    # /etc/os-release should contain a line like "ID=ubuntu", "ID=arch", etc.
    # Extract the value of the ID and return it.
    return host.exec(
        'cat /etc/os-release |grep "^ID=" |cut -f 2 -d "="',
        echo_stdout=False
    ).stdout.decode().strip()

