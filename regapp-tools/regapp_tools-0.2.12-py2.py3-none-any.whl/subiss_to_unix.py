#!/usr/bin/env python3
'''Commandline tools to retrieve unix user name based on OIDC sub@iss from bwIDM regApp (aka LDAP Facade)'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation

import os
from sys import stdout
import logging

from regapp_tools.parse_args import args
from regapp_tools.bwidmtools import external_id_from_subiss, get_username_from_external_id

# Logging
# logformat='[%(levelname)s] %(message)s'
logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.verbose:
    logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.debug:
    logging.basicConfig(level=os.environ.get("LOG", "DEBUG"), format = logformat)
else:
    logging.basicConfig(level=os.environ.get("LOG", "INFO"), format = logformat)
logger = logging.getLogger(__name__)


def main():
    '''main entry point'''

    if len(args.sub_iss) >0 :
        external_id = external_id_from_subiss(sub_iss=args.sub_iss)
        username = get_username_from_external_id(external_id)
        stdout.write(username)

if __name__ == '__main__':
    main()
