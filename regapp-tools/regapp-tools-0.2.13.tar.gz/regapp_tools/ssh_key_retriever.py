#!/usr/bin/env python3
'''Commandline tools to retrieve ssh-keys based on unix user name stored in bwIDM regApp (aka LDAP Facade)'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation

import os
import json
import logging
import urllib.parse as ul
import requests

from regapp_tools.config import CONFIG
from regapp_tools.parse_args_ssh import args
from regapp_tools.parse_args_ssh import remove_quotes
from regapp_tools.bwidmtools import external_id_from_subiss, get_external_id_from_username
from regapp_tools.bwidmtools import get_username_from_external_id, get_sshkey_from_external_id
from regapp_tools.bwidmconnection import BwIdmConnection

# Logging
# logformat='[%(levelname)s] %(message)s'
logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.verbose:
    logformat='[%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
if args.debug:
    try:
        logging.basicConfig(filename="/var/log/ssh-key-retriever.log", level=os.environ.get("LOG", "DEBUG"), format = logformat)
    except PermissionError:
        logging.basicConfig(level=os.environ.get("LOG", "DEBUG"), format = logformat)
else:
    try:
        logging.basicConfig(filename="/var/log/ssh-key-retriever.log", level=os.environ.get("LOG", "INFO"), format = logformat)
    except PermissionError:
        logging.basicConfig(level=os.environ.get("LOG", "INFO"), format = logformat)
logger = logging.getLogger(__name__)


# def get_sshkeys(externalId='hdf_61230996-664f-4422-9caa-76cf086f0d6c@unity-hdf'):
def get_sshkeys():
    '''get key from externalId'''

    parameter = args.username
    if len(parameter.split('@')) == 2:
        external_id = external_id_from_subiss(sub_iss=parameter)
    elif len(parameter.split('@')) == 1:
        external_id = get_external_id_from_username(parameter)
    else:
        logger.error(F"The provided parameter '{args.username}' is neither a username nor a sub@iss")
        raise ValueError()

    sshkeys = get_sshkey_from_external_id(external_id)
    return sshkeys


def main():
    '''Main Program'''
    sshkeys = get_sshkeys()
    print (F"{sshkeys}")
    return 0


if __name__ == "__main__":
    keys = main()
