#!/usr/bin/env python3
'''Commandline tool to retrieve and dupmp info stored in regapp based on unix user name stored in bwIDM regApp (aka LDAP Facade)'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, 
# pylint: logging-fstring-interpolation, logging-not-lazy, logging-format-interpolation

import os
import sys
import json
import logging
import urllib.parse as ul

from regapp_tools.parse_args import args
from regapp_tools.bwidmtools import external_id_from_subiss, get_external_id_from_username
from regapp_tools.bwidmtools import get_username_from_external_id, get_sshkey_from_external_id
from regapp_tools.bwidmtools import get_userinfo_from_external_id, get_user_registrations_from_external_id
from regapp_tools.bwidmtools import deregister_external_id_from_service, register_external_id_from_service
from regapp_tools.bwidmtools import get_list_of_all_users, get_list_of_registrations_in_service
from regapp_tools.bwidmtools import deactivate_user, activate_user
from regapp_tools.bwidm_user import User, Registry


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
def do_action():
    '''get info from externalId'''
    ##### in case we need user access:

    if args.findall != False:
        if args.findall == None:
            print ("List of all users")
            user_list = get_list_of_all_users()
            # if args.verbose:
            #     print(json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': ')))
            for u in user_list:
                user = User(u, extensive=args.extensive)
                print (user.info(sshkeys=args.ssh, extensive=args.extensive))
        else:
            print (F"List of users in service {args.findall}")
            registry_list = get_list_of_registrations_in_service(args.findall)
            for r in registry_list:
                registry = Registry(r)
                sys.stdout.write(registry.__repr__(extensive=args.extensive))
            # if args.verbose:
            #     print(json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': ')))

        sys.exit(0)

    ################## args.username required beyond this point 
    if args.deregister_from_service or\
        args.register_for_service or\
        args.activate or\
        args.deactivate or\
        args.grp or\
        args.reg or\
        args.ssh or\
        args.info:
        username = ""
        if args.username is None or args.username == []:
            print("Must specify a username")
            exit(1)
        parameter = args.username[0]
        if len(parameter.split('@')) == 2: # we got sub@iss or external_id
            logger.debug("sub@iss or external_id")
            external_id = external_id_from_subiss(sub_iss=parameter)
            # external_id = "d7a53cbe3e966c53ac64fde7355956560282158ecac8f3d2c770b474862f4756%40egi.eu@https%3A%2F%2Faai.egi.eu%2Foidc%2F"
            # logger.info(F"enforced external id: {external_id}")
            logger.debug(F"actual external id: {external_id}")

            username = get_username_from_external_id(external_id)

        elif len(parameter.split('@')) == 1: # we got a username
            external_id = get_external_id_from_username(parameter)
            logger.debug(F"actual external id: {external_id} (from username: {parameter})")
            username = parameter
        else:
            logger.error(F"The provided parameter '{args.username}' is neither a username nor a sub@iss")
            raise ValueError()

        try:
            (sub,iss) = external_id.split('@')
            sub = ul.unquote_plus(sub)
            iss = ul.unquote_plus(iss)
        except AttributeError:
            sub = ""
            iss = ""
        except ValueError:
            sub = ""
            iss = ""
    # if args.externalid is not None:
    #     external_id = args.externalid
    logger.debug(F"actual external id: {external_id}")

    
    ##### actions on users
    if args.deactivate:
        print ("Deactivating")
        resp=deactivate_user(external_id)
        if args.verbose:
            print(resp)
        if resp.status_code == 204:
            print ("Success")

    if args.activate:
        print ("Activating")
        resp=activate_user(external_id)
        if args.verbose:
            print(resp)
        if resp.status_code == 204:
            print ("Success")

    if args.deregister_from_service:
        print (F"Deregistering from {args.deregister_from_service}")
        resp=deregister_external_id_from_service(external_id, args.deregister_from_service)
        print (F"Result: {resp['result']}")
        if args.verbose:
            print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.register_for_service:
        print (F"Registering for {args.deregister_from_service}")
        resp=register_external_id_from_service(external_id, args.register_for_service)
        print (F"{resp['registryStatus']}")
        if args.verbose:
            print(json.dumps(resp, sort_keys=True, indent=4, separators=(',', ': ')))

    ##### Information about users
    if args.info:
        external_user = get_userinfo_from_external_id(external_id)
        user = User(external_user)
        print (user.info(info=True, groups=False, extensive=args.extensive))
        if args.verbose:
            print(json.dumps(external_user, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.grp:
        external_user = get_userinfo_from_external_id(external_id)
        user = User(external_user)
        print (user.info(info=False, groups=True))
        if args.verbose:
            print(json.dumps(external_user, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.reg:
        reg_info      = get_user_registrations_from_external_id(external_id)
        
        if args.verbose:
            print(json.dumps(reg_info, sort_keys=True, indent=4, separators=(',', ': ')))

        for registry in reg_info:
            registry_object = Registry(registry)
            print (registry_object.info(extensive=args.extensive))
            # print (F"{registry['id']} - "\
            #        F"{registry['registryStatus']:13} - "\
            #        F"{registry['lastStatusChange']:30}- "\
            #        F"{registry['createdAt']:30}- "\
            #        F"{registry['serviceShortName']:10}- "\
            #        F"{registry['registryValues']['localUid']:20}"\
            #        )

    if args.ssh:
        sshkeys = get_sshkey_from_external_id(external_id)
        print (sshkeys)
def main():
    '''Main Program'''
    # if args.username != []:
    do_action()
    return 0


if __name__ == "__main__":
    keys = main()
