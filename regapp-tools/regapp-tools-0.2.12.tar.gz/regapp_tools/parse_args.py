# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import logging
import argparse

from .helpers import remove_quotes

logger = logging.getLogger(__name__)

def parseOptions():
    '''Parse the commandline options'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--rest_user',   '-u',             help='username for LDF rest interface')
    parser.add_argument('--rest_passwd', '-p',             help='passwdname for LDF rest interface')
    parser.add_argument('--iss'                  , action="append")
    parser.add_argument('--bwidmOrgId'           , default="hdf")
    parser.add_argument('--base_url'             , default="https://bwidm-test.scc.kit.edu/rest/")
    parser.add_argument('--verify_tls'           , default=True    , action="store_false" , help='disable verify')
    parser.add_argument('--verbose', '-v'        , default=0   , action="count", help="Verbosity")
    parser.add_argument('--debug',   '-d'        , default=False   , action="store_true" )
    parser.add_argument('--config', '-c'         , default=None)
    parser.add_argument(dest='sub_iss'           , default=None, nargs='*', help='Content of $REMOTE_USER. For testing use "test-offline" and "test-id"')
    parser.add_argument('--ssh', '-s'            , default=False, action="store_true")
    parser.add_argument('--reg', '-r'            , default=False, action="store_true")
    parser.add_argument('--grp', '-g'            , default=False, action="store_true")
    parser.add_argument('--info', '-i'           , default=False, action="store_true")
    parser.add_argument('--extensive', '-e'      , default=False, action="count")
    parser.add_argument('--all', '-a'            , default=False, action="store_true")
    parser.add_argument('--findall', '-f', '-l'  , default=False, nargs='?')
    parser.add_argument('--deactivate'           , default=False, action="store_true")
    parser.add_argument('--activate'             , default=False, action="store_true")
    parser.add_argument('--deregister_from_service', '--deregister', default=None)
    parser.add_argument('--register_for_service',     '--register', default=None)

    # sanitize some args:
    args = parser.parse_args()
    args.base_url   = args.base_url.rstrip('/')
    args.bwidmOrgId = remove_quotes(args.bwidmOrgId)

    args.username = args.sub_iss

    if args.all:
        args.grp=True
        args.info=True
        args.reg=True

    # Set info, in case no other action is set
    if args.deregister_from_service or\
        args.register_for_service or\
        args.activate or\
        args.deactivate or\
        args.grp or\
        args.reg or\
        args.ssh:
            pass
    else:
        args.info = True

    return args

# reparse args on import
args = parseOptions()
