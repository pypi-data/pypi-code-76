#!/usr/bin/env python3
import argparse
from os import system

from ..env import get_repo_env, Environment

# for checking whether a url is localhost, because then the docker needs to use
# a special network option (network="host"). If we don't do this, the docker
# will try to connect to _its own_ container localhost, rather than the host
# machine localhost.
from urllib.parse import urlparse
from socket import gethostbyname
from ipaddr import IPAddress

EXEC_COMMAND = r'docker run {network_argument} -e PORT={port} -p {port}:{port} --rm vivekratnavel/omniboard:latest --mu "{mongo_url}"'
LOCALHOST_NETWORK_ARGUMENT = '--network="host"'

def is_url_localhost(url):
    """Checks whether the hostname of this URL address is localhost, i.e.
    loopback.
    """
    hostname = urlparse(url).hostname
    return IPAddress(gethostbyname(hostname)).is_loopback

def main():
    parser = argparse.ArgumentParser(description='Launch Omniboard using Docker for an environment configuration.')
    parser.add_argument('-f', '--file', help='environment configuration yaml file path (default: declair_env.yaml in root of git repository)')
    parser.add_argument('-p', '--port', default=9000, type=int,
                        help='port for Omniboard (default: 9000)')

    args = parser.parse_args()
    filepath = args.file
    if filepath is not None:
        env = Environment.from_file(filepath)
    else:
        env = get_repo_env()

    if env is None:
        print("No environment yaml path provided and default file not present.")
        exit(1)

    url = env.get('observers', {}).get('mongo', {}).get('url')
    if url is None:
        print("Given environment config file has no entry for MongoDB address")
        exit(1)

    if is_url_localhost(url):
        network_string = LOCALHOST_NETWORK_ARGUMENT
    else:
        network_string = ''

    # Format and execute the Docker command
    formatted_command = EXEC_COMMAND.format(network_argument=network_string, port=args.port, mongo_url=url)
    out = system(formatted_command)

    if out == 32000:
        print("Error. Port {} may be taken".format(args.port))
        exit(1)


if __name__ == '__main__':
    main()
