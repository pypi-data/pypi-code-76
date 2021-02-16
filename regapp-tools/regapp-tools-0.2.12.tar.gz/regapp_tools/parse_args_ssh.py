'''interface to argparse'''
# pylint
# vim: tw=100
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation

import logging
import argparse

from .helpers import remove_quotes

logger = logging.getLogger(__name__)

def parseOptions():
    '''Parse the commandline options'''

    parser = argparse.ArgumentParser()

    parser.add_argument('--rest_user',   '-u'           , help='username for LDF rest interface')
    parser.add_argument('--rest_passwd', '-p'           , help='passwdname for LDF rest interface')
    parser.add_argument('--logfile',     '-l'    , default='ldf-interface.log')
    parser.add_argument('--loglevel'              ,default='warning')
    parser.add_argument('--base_url'             , default="https://bwidm-test.scc.kit.edu/rest/")
    parser.add_argument('--verify_tls'           , default=True    , action="store_false" , help='disable verify')
    parser.add_argument('--verbose', '-v'        , default=0       , action="count", help="Verbosity")
    parser.add_argument('--debug',   '-d'        , default=False   , action="store_true" )
    # parser.add_argument('--config', '-c'         , default="regapp_tools.conf")
    parser.add_argument('--config', '-c'         , default=None)
    parser.add_argument('--ssh', '-s'            , default=False, action="store_true")
    parser.add_argument(dest='username'          , help='unix username to fetch ssh keys for')

    args = parser.parse_args()

    # consistently remove all quotes from all input parameters:
    for arg in vars(args):
        # typeOfArg = type(getattr(args, arg))
        # print ("\narg: %s -- %s"%(arg, typeOfArg))
        # print ("  before: %s: %s" %(arg, getattr(args, arg)))
        if isinstance (getattr(args, arg),  str):
            setattr(args, arg, remove_quotes(getattr(args, arg)))
            # print ("  after:  %s: %s\n\n\n" %(arg, getattr(args, arg)))
        elif isinstance(getattr(args, arg),  list):
            newlist = []
            for entry in getattr(args, arg):
                entry =  remove_quotes(entry)
                newlist.append(entry)
            setattr(args, arg, newlist)
            # print ("  after:  %s: %s\n\n\n" %(arg, getattr(args, arg)))

    # sanitize some args:
    # args = parser.parse_args()
    # args.base_url   = args.base_url.rstrip('/')
    # args.bwidmOrgId = remove_quotes(args.bwidmOrgId)

    return args

# reparse args on import
args = parseOptions()
