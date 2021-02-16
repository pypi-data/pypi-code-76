#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#

import argparse
import logging
import sys

from colorama import Fore, Style

from aos_prov import __version__
from aos_prov.command_provision import run_provision
from aos_prov.communication.cloud.cloud_api import DEFAULT_REGISTER_PORT
from aos_prov.communication.utils import DEFAULT_USER_CERT_PATH, DEFAULT_USER_KEY_PATH
from aos_prov.communication.utils.errors import CloudAccessError, BoardError, DeviceRegisterError
from aos_prov.communication.utils.user_credentials import UserCredentials

ARGUMENT_USER_CERTIFICATE = '--cert'
ARGUMENT_USER_KEY = '--key'

logger = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="The board provisioning tool using gRPC protocol",
        epilog="Run 'aos-prov --help' for more information on a command.")

    parser.add_argument(
        '-u',
        '--unit',
        required=True,
        help="Unit address in format ADDRESS:PORT"
    )

    parser.add_argument(
        ARGUMENT_USER_CERTIFICATE,
        default=DEFAULT_USER_CERT_PATH,
        help="User certificate file. Default: {}".format(DEFAULT_USER_CERT_PATH))

    parser.add_argument(
        ARGUMENT_USER_KEY,
        default=DEFAULT_USER_KEY_PATH,
        help="User key file. Default: {}".format(DEFAULT_USER_KEY_PATH))

    parser.add_argument(
        '--register-host',
        help="Overwrite cloud address. By default it is taken from user certificate"
    )

    parser.add_argument(
        '--register-port',
        default=DEFAULT_REGISTER_PORT,
        help=f"Cloud port. Default: {DEFAULT_REGISTER_PORT}"
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()
    return args


def main():
    """ The main entry point. """
    status = 0
    args = _parse_args()

    try:
        uc = UserCredentials(args.cert, args.key)
        run_provision(args.unit, uc, args.register_port)
    except CloudAccessError as e:
        logger.error('\nUnable to provision the board with error:\n%s', str(e))
        status = 1
    except DeviceRegisterError as e:
        print(f"{Fore.RED}FAILED with error: {str(e)} {Style.RESET_ALL}")
        logger.error('Failed: %s', str(e))
        status = 1
    except BoardError as e:
        logger.error('\nFailed during communication with device \n%s', str(e))
        status = 1
    except (AssertionError, KeyboardInterrupt):
        sys.stdout.write('Exiting ...\n')
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    main()
