# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

from sys import exit as s_exit, stderr
import logging
import urllib.parse as ul
import json
from regapp_tools.parse_args import args
from regapp_tools.config import CONFIG
from regapp_tools.bwidmconnection import BwIdmConnection

logger = logging.getLogger(__name__)

def external_id_from_subiss(sub=None, iss=None, sub_iss=None):
    '''generate a safe urlencoded external_id from sub and iss'''

    # sanitise input:
    if sub_iss is None:
        if sub is None or iss is None:
            raise ValueError('aaaaaaaaa')
        sub_iss = sub+"@"+iss

    if isinstance(sub_iss, list):
        sub_iss = sub_iss[0]

    logger.debug(F"sub iss: {sub_iss}")

    # Values for testing:
    if sub_iss == 'test-offline':
        stderr.write("Offline test: %s\n" % sub_iss)
        return 'hdf_marcus'
    if sub_iss == 'test-id':
        sub_iss = "6c611e2a-2c1c-487f-9948-c058a36c8f0e@https://login.helmholtz-data-federation.de/oauth2"
        stderr.write("using test id: %s\n" % sub_iss)
    if sub_iss == 'test-marcus':
        sub_iss = "6c611e2a-2c1c-487f-9948-c058a36c8f0e@https://login.helmholtz-data-federation.de/oauth2"
        stderr.write("using test id: %s\n" % sub_iss)
    if sub_iss == 'test-borja':
        sub_iss = "309ed509-c56a-4894-b163-5993bd08cbc2@https://login.helmholtz-data-federation.de/oauth2"
        stderr.write("using test id: %s\n" % sub_iss)

    # Construct urlencoded sub@iss
    try:
        vals = sub_iss.split('@')
        sub = '@'.join(vals[0:-1]) # First few components are sub, may contain '@'
        iss = vals[-1] # Last component is issuer may NOT contain '@'
        external_id = ul.quote_plus(sub) + \
                      '@' + \
                      ul.quote_plus(iss)
        return external_id
    except ValueError:
        return None
def get_userinfo_from_external_id(external_id):
    '''get all userinfo from external_id. Returns the json response of RegApp or raises an Error'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-user', 'find', 'externalId', external_id)
    logger.debug(F"RESP: {resp}")
    resp_json = safe_resp_conversion(resp)

    return resp_json
def get_username_from_external_id(external_id):
    '''get unix username from an external_id'''
    resp_json = get_userinfo_from_external_id(external_id)

    try:
        username = resp_json['attributeStore']['urn:oid:0.9.2342.19200300.100.1.1']
        bwIdmOrgId = resp_json['attributeStore']['http://bwidm.de/bwidmOrgId']
        full_username = F"{bwIdmOrgId}_{username}"
    except KeyError as e:
        logger.error('Error: I could not find the username in the database.')
        logger.error('  Most likely the user is not registered for this service\n')
        logger.error(F"  {e}")
        logger.error('  This is the json data received\n')
        logger.error(json.dumps(resp_json, sort_keys=True, indent=4, separators=(',', ': ')))

    if args.debug:
        logger.debug('This is the json data received\n')
        logger.debug(json.dumps(resp_json, sort_keys=True, indent=4, separators=(',', ': ')))

    return full_username
def get_sshkey_from_external_id (external_id):
    '''get ssh key from an external_id'''
    resp_json = get_userinfo_from_external_id(external_id)
    # print(json.dumps(resp_json, sort_keys=True, indent=4, separators=(',', ': ')))
    sshkeys=""

    try:
        sshkeys_entry = resp_json['genericStore']['ssh_key']
        sshkeys_store = json.loads(sshkeys_entry)
    except json.JSONDecodeError:
        try:
            sshkeys_entry = sshkeys_entry.replace("'", '"')
            sshkeys_store = json.loads(sshkeys_entry)
        except json.JSONDecodeError:
            logger.error("Cannot find 'ssh_key' in 'genericStore' response of regApp")
            s_exit(2)
    except KeyError:
        s_exit(2)

    try:
        logger.debug(json.dumps(sshkeys_store, sort_keys=True, indent=4, separators=(',', ': ')))
        for key in sshkeys_store:
            sshkeys = sshkeys +  key['value'].rstrip('\n') + "\n"
        if args.verbose:
            logging.debug(F"just obtained keys: {sshkeys}")
    except KeyError:
        logger.error("Cannot find 'ssh_key' in 'genericStore' response of regApp. I tried hard:")
        logger.error(json.dumps(resp_json, sort_keys=True, indent=4, separators=(',', ': ')))
        s_exit(3)
    logger.debug(F"returning: {sshkeys}")
    return sshkeys.rstrip('\n')

def safe_resp_conversion(resp):
    '''Safely convert a response to json'''
    if resp.status_code != 200:
        logger.debug ('Error %d reading from remote: \n%s\n'% (resp.status_code, str(resp.text)))
        s_exit(1) # or raise or return None?
    try:
        resp_json = resp.json()
    except json.JSONDecodeError:
        logging.error ('Could not decode json that I obtained from rest server')
        raise
    return resp_json
def get_external_id_from_username(parameter):
    '''get externalId from unix username'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    ATTR_USERNAME = 'urn:oid:0.9.2342.19200300.100.1.1'

    # find out whether parameter contains a bwidm org id:
    if len(parameter.split('_')) < 2:
        logger.warning(F"The provided parameter is not a prefixed username: '{parameter}'")
        username             = parameter
        bwidmorgid_specified = False
    else:
        parts = parameter.split('_')
        bwidm_org_id = parts[0]
        username  = "_".join(parts[1:])
        bwidmorgid_specified     = True

    if not bwidmorgid_specified:
        try:
            bwidm_org_id = CONFIG['backend.bwidm']['org_id']
        except KeyError:
            logger.warning("No bwidmOrgId specified anywhere. Lets see if there is only one username like this")
            # raise ValueError

    resp = BWIDM.get ('external-user', 'find', 'attribute', ATTR_USERNAME, username)
    # note, this may be a list, because we didn't provide a bwidm_org_id
    resps_json = safe_resp_conversion(resp)

    if not bwidmorgid_specified: # Then we must only continue, if there is a single entry returned!!!
        if len(resps_json) != 1:
            logger.warning("Username did not contain a '_'. This may be normal for example for a root login. Ignoring.")
            # raise ValueError
            s_exit(0)
        return(resps_json[0]['externalId'])

    for resp_json in resps_json:
        if resp_json['attributeStore']['http://bwidm.de/bwidmOrgId'] == bwidm_org_id:
            return(resp_json['externalId'])

    return None # to keep pylint happy
def get_user_registrations_from_external_id(external_id):
    '''get all user registrations from external_id. Returns the json response of RegApp or raises an Error'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-reg', 'find', 'externalId', external_id)
    resp_json = safe_resp_conversion(resp)
    return resp_json
def deregister_external_id_from_service(external_id, service_name):
    '''deregister user from given service'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-reg', 'deregister', 'externalId', external_id, 'ssn', service_name)
    resp_json = safe_resp_conversion(resp)
    return resp_json
def deactivate_user(external_id):
    '''deactivate user from given service'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-user', 'deactivate', 'externalId', external_id)
    return resp
def activate_user(external_id):
    '''activate user from given service'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-user', 'activate', 'externalId', external_id)
    return resp
def register_external_id_from_service(external_id, service_name):
    '''register user from given service'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-reg', 'register', 'externalId', external_id, 'ssn', service_name)
    resp_json = safe_resp_conversion(resp)
    return resp_json
def get_list_of_all_users():
    '''Get list of all users'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-user', 'find', 'all')
    resp_json = safe_resp_conversion(resp)
    return resp_json
def get_list_of_registrations_in_service(service):
    '''Get list of all users from given service'''
    # Call regapp
    BWIDM = BwIdmConnection(CONFIG)
    resp = BWIDM.get ('external-reg', 'find', 'all', 'ssn', service)
    resp_json = safe_resp_conversion(resp)
    return resp_json
