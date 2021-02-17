#!/usr/bin/env python3
from borgssh.version import __version__
from fire import Fire

from borgssh.prj_utils import get_file_path
from borgssh.prj_utils import fail
from borgssh.prj_utils import Bcolors
from borgssh.prj_utils import super_print
import borgssh.borgconf as conf

import os
import sys
import socket
import subprocess as sp

NOTIF = True
try:
    from notifator.telegram import bot_send
except:
    NOTIF = False

# print("i... unit uname loaded, version:",__version__)

#def read_conf(conf = "~/.borgssh.conf" ):
#    print("D... readconf")

def call_notifator(msg):
    if NOTIF:
        host = socket.gethostname()
        msg2 =  msg+"@"+host
        print(msg2)
        bot_send("Backups", msg2 )
    else:
        print("q... notifator not installed...")

def call_command(CMD):
    res = "X... apriori error when calling CMD"
    try:
        res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    except sp.CalledProcessError as e:
        print("X...  ...........................ERROR when calling", CMD)
        print(e.returncode)
        call_notifator("XXX-"+CMD.split()[-1])
        # sys.exit(e.returncode)
    return res

def get_path_reponame_host(folder, debug=False):
    global print
    print=super_print(debug)(print)
    home = os.path.expanduser("~/")
    foname = os.path.expanduser(folder)
    rpname = foname.split(home)[-1]
    host = socket.gethostname()
    if len(foname)<1:
        print("X... problem, not 1st level home directory")
        sys.exit(0)
    if home+rpname != foname:
        print("X... problem, NOT the 1st level dir @HOME")
        if not os.path.isdir(foname):
            print("X... problem, NOT even a folder '{}'".format( foname) )
            sys.exit(0)
        else:
            rpname = rpname.replace("/","")
            rpname = rpname.replace(" ","")
            print("i... but it is a folder... rpname==>", rpname)
    print("D... FONAME REPONAME: ",foname,"rpname",rpname)
    return foname,rpname,host



def init( debug = False, configfile=""):
    """ borg init ssh://borg@***:2222/config/borg -e none  ... one time"""
    global print
    print=super_print(debug)(print)
    conf.load_config(configfile)

    CMD = "borg init ssh://borg@{}:2222/config/borg -e none".format(
        conf.CONFIG['remote']
        )
    print(CMD)
    # direct terminal output
    res = call_command( CMD )
    #res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    print(res)
    return True



def create(folder, debug = False, configfile=""):
    """ borg create ssh://borg@***:2222/config/borg::host_folder
    """
    global print
    print=super_print(debug)(print)
    conf.load_config(configfile)
    foname,rpname,host = get_path_reponame_host(folder,debug)

    CMD = "borg create --stats --progress --compression zstd,9 ssh://borg@{}:2222/config/borg::{}_{}_`date +%Y%m%d_%H%M%S`  {}".format(
        conf.CONFIG['remote'],
        host,
        rpname,
        foname
        )
    print(CMD)
    # direct terminal output
    res = call_command( CMD )
    #res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    print(res)
    return True




def prune(folder, debug = False, configfile=""):
    """ borg prune ssh://borg@***:2222/config/borg::host_folder"""
    global print
    conf.load_config(configfile)
    print=super_print(debug)(print)

    foname,rpname,host = get_path_reponame_host(folder,debug)

    CMD = "borg prune ssh://borg@{}:2222/config/borg   --keep-daily=7 --keep-weekly=8 --keep-monthly=-1  -P {}".format(
        conf.CONFIG['remote'],
        host+"_"+rpname
        )
    print(CMD)
    # direct terminal output
    #res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    res = call_command( CMD )

    print(res)
    return True



def create_and_prune(folder, debug =  False, configfile=""):
    """FIRST of the global commands"""
    create(folder,debug, configfile = configfile)
    prune(folder,debug, configfile = configfile)
    return True


def create_and_prune_defaults(debug =  False, configfile=""):
    """SECOND of the global commands
use: sshborg create_and_prune_defaults --configfile ~/.borgssh.conf
"""
    conf.load_config(configfile)
    report = ""
    if 'default_folders' in conf.CONFIG:
        for folder in conf.CONFIG['default_folders']:
            folder = folder.rstrip("/")
            print("i...  CREATE AND PRUNE:",folder)
            create_and_prune(folder,debug, configfile=configfile)
            report = report + " " + folder
    call_notifator( report ) # only here I call telegram
    return True



def listborg(debug = False, configfile=""):
    """ borg list ssh://borg@***:2222/config/borg"""
    global print
    conf.load_config(configfile)
    print=super_print(debug)(print)

    CMD = "borg list ssh://borg@{}:2222/config/borg".format(
        conf.CONFIG['remote']
        )
    print(CMD)
    # direct terminal output
    # res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    res = call_command( CMD )
    for i in res:
        print(i[:80])
    return True


def extract(folder, debug = False, configfile=""):
    """ borg extract ssh://borg@***:2222/config/borg::host_folder_***"""
    global print
    conf.load_config(configfile)
    print=super_print(debug)(print)
    foname,rpname,host = get_path_reponame_host(folder, debug)

    CMD = "borg extract -n ssh://borg@{}:2222/config/borg::{}_{}".format(
        conf.CONFIG['remote'],
        host,
        foname
        )
    print(CMD)
    # direct terminal output
    res = call_command( CMD )
    #res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    for i in res:
        print(i[:80])
    return True


def check(debug = False, configfile=""):
    """borg check --info ssh://borg@***:2222/config/borg
borg info ssh://borg@***:2222/config/borg"""
    global print
    conf.load_config(configfile)
    print=super_print(debug)(print)

    CMD = "borg check --info ssh://borg@{}:2222/config/borg".format(
        conf.CONFIG['remote']
        )
    print(CMD)
    # direct terminal output
    # res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    res = call_command( CMD )
    for i in res:
        print(i[:80])

    CMD = "borg info ssh://borg@{}:2222/config/borg".format(
        conf.CONFIG['remote']
        )
    print(CMD)
    # direct terminal output
    # res=sp.check_output( CMD, shell=True ).decode("utf8").rstrip().split("\n")
    res = call_command(CMD)
    # res = sp.getoutput(CMD)
    for i in res:
        print(i[:80])
    return True




if __name__ == "__main__":
    print("i... in the __main__ of uname of borgssh")
    Fire({"init":init,
        "create":create,
          "prune":prune,
          "create_and_prune":create_and_prune,
          "create_and_prune_defaults":create_and_prune_defaults,
          "list":listborg,
          "extract":extract,
          "check":check,
          "xtst":call_notifator
          }
    )
