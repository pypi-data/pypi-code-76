import logging
from argparse import ArgumentParser

from .mac2vendors import get_vendor

logger = logging.getLogger(__name__)

parser = ArgumentParser("mtv")

sub_parsers = parser.add_subparsers(help='[command] help', dest="command")

mac_parser = sub_parsers.add_parser("mac", help="Translates the mac address to a vendor mapping.")

mac_parser.add_argument("mac_address", type=str, default="",
                        help="the mac to translate. A mac looks like this: xx:xx:xx:xx:xx:xx with x hexadecimal.")
mac_parser.add_argument("-s", "--strict", default=False, action="store_true",
                        help="Check if a valid mac_address was inserted")


def mtv():
    args = parser.parse_args()
    if args.command == "mac":
        mapping = get_vendor(mac_address=args.mac_address, strict=args.strict)
        if mapping is not None:
            print(mapping)
        else:
            print("Could not find {mac_address}".format(mac_address=args.mac_address))
    else:
        parser.print_help()


if __name__ == '__main__':
    mtv()
