"""
This is a comand line utility to allow the user to configure a cisco router or switch
Serves an entrypoint, parses user input, and handles user input

"""

from autoswitch.network import *
from autoswitch.exceptions import *
from autoswitch.utils import *

import argparse


def get_auth_group(parser):
    group = parser.add_argument_group("Authentication")

    group.add_argument(
        "-l", "--username", default="")
    group.add_argument(
        "-p", "--password", default="")
    group.add_argument(
        "-s", "--secret", default="")

    return group


def input_handler(args):
    """
    Handles user input
    """

    if args.get("load") != None:
        args["load_func"](args)

    if args.get("list_port"):
        list_serial_ports()


def get_args(argv) -> dict:

    parser = argparse.ArgumentParser(prog="autoswitch", description="Configure Cisco Device",
                                     epilog="This command-line tool helps configure cisco devices with text files.")

    subparsers = parser.add_subparsers(
        dest="menu", description="The method used to connect to network device")

    ssh_menu = subparsers.add_parser(
        "ssh",  help="Connect to device using ssh")
    ssh_menu.set_defaults(load_func=load_with_ssh)

    telnet_menu = subparsers.add_parser(
        "telnet", help="Connect to device using telnet")
    telnet_menu.set_defaults(load_func=load_with_telnet)

    serial_menu = subparsers.add_parser(
        "serial", help="Connect to device using serial cable")
    serial_menu.set_defaults(load_func=load_with_serial)

    serial_auth_group = get_auth_group(serial_menu)

    serial_util_group = serial_menu.add_argument_group("Tools")
    serial_util_group.add_argument(
        "--list-port", help="lists avalible serial ports", action="store_true")

    default_serial_port = get_default_serial_port()

    if default_serial_port != "":
        serial_menu.add_argument(
            "--load", help="Load configuration file to device", default=None, type=path)
        serial_menu.add_argument(
            "--port", type=comport, help="COMPORT name", default=default_serial_port)

    serial_menu.add_argument(
        "--baudrate", type=int, default=9600, help="Speed bytes are transferred over serial")

    args = parser.parse_args(argv)

    if args.menu == None:
        parser.print_help()
        exit(1)

    return vars(args)


def main(argv=None) -> int:
    """
    Handle Command line Arguments
    """

    args = get_args(argv)

    input_handler(args)

    return 0


if __name__ == "__main__":
    exit(main())
