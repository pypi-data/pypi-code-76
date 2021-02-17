#!/usr/bin/python

import json
import re
import collections
import os
import time, datetime
import sys
import shutil
import cvdast
from cvdastwrapper import runconfig
from cvdastwrapper import apispecs

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
ainfofname  = runconfig.dainfofname
specdname   = runconfig.inspecdir

attackinfo = {}  # attack info matching attackname to info
apidef     = {}  # api info matching spec->api(which is basepath+path-> path info

#
# called by main function to load a few global variables
#  to store attack info, api definitions, and test results
#
# test results are saved for future comparision
#
def init(inainfofname = "", specdir = ""):
    print("\n--- Initializion\n")
          
    if not inainfofname:
        inainfofname = ainfofname
    print("\n---   Loading Attack Info from %s \n" % inainfofname)
    if not os.path.exists(inainfofname):
        print("---    No attack info file %s, loading from fuzzing test. \n" % inainfofname)
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if not os.path.exists("tests/data"):
            os.mkdir("tests/data")
        if not os.path.exists("savedattackinfo/attack_info.json"):
            print("Missing attack_info file, please run fuzzallspec.py to generate fuzzing test and test files. ")
            file_path = os.path.join(os.path.dirname(os.path.abspath(cvdast.__file__)), 'templates/data/attack_info.json')
            with open(file_path) as data_file:
                data = json.load(data_file)
                with open('tests/data/attack_info.json', 'w') as fd:
                    json.dump(data, fd)
        else:
            shutil.copy("savedattackinfo/attack_info.json", "tests/data/")

    ainfo = {}
    with open(inainfofname) as f:
        ainfo = json.load(f)
        f.close()
    if "info" in ainfo:
        for (a, x) in ainfo["info"].items():
            attackinfo[a] = x
    else:
        print("---    Problem with attackinfo, no 'info' key found.\n")

    if not specdir:
        specdir=specdname
    print("\n---   Loading api spec info\n")
    sfs = []
    for (__,__, filename) in os.walk(specdir):
        sfs.extend(filename)

    for sfname in sfs:
        aspec={}
        with open(specdir+"/" + sfname, "r") as f:
            aspec = json.load(f)
            f.close()
          
        if not aspec or (not "paths" in aspec) :
            print ("\n---     Failed to load api spec from %s , spec does not contain required \"paths\" element.\n" % (sfname))
            continue
        else:
            spec = sfname[:-len(".json")].lower()
            bpath=""
            if "basePath" in aspec:
                bpath=aspec["basePath"]
            elif "basepath" in aspec:
                bpath=aspec["basepath"]
            rval = {}
            for ( p, adef) in aspec["paths"].items():
                newp = bpath+p
                if bpath.endswith("/") and p[0] == "/":
                    newp = bpath+p[1:]
                elif (not bpath.endswith("/")) and (not p[0] == "/") :
                    newp = bpath+"/"+p 
                rval[newp] = adef
                # print("\n Debug: new api path is %s\n" % (newp))
            apidef[spec] = rval
    ''' end for sfname '''

    if not runconfig.usecustomlist:
        #print(runconfig.usecustomlist, "usecustomlist")
        runconfig.apispeclist = apispecs.apispeclist
    
    resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
    if not os.path.exists(resultrootn):
        os.makedirs(resultrootn, exist_ok=True)
    for f in os.listdir(resultrootn):
        if not f.lower() == f :
            if not f[:1] == ".": 
                print("\n Rename  %s to %s lower case" % (resultrootn+f, resultrootn+f.lower()))
                os.rename(resultrootn+f, resultrootn+f.lower())
                

#
# end init
#
    
#
# return a list of mapping between attacknames and severity
#
def findAttackInfoObjs(inattacklist=[]): 
    rval = {}

    ainfo = attackinfo
    for aname in ainfo.keys():
        for a in inattacklist :
            if a.startswith(aname) or a.startswith(aname.replace("_", "-")):
                for anysubattack, subinfo in ainfo[aname].items():
                    rval[a] = [subinfo["severity"], subinfo]
                    break

    return rval

#
# patch attack pattern file
#  a patch work around, test metadata sometime does not show the attack file used
#  when it mistakens a test as skipped
#
#  search the fuzzdb attack directory, look for the matching attack file name
#   for use of a link for reporting
#
def patchAttackPatternFile(attack):
    dbd = runconfig.dfuzzdbdirname + "/"
    attd = "attack/" + attack + "/"
    if not os.path.exists(dbd + attd):
        return ""
    for f in os.listdir(dbd+attd):
        if not f.endswith(".md"):
            return attd+f
    return ""
# end patch

#
# utility api spec loading functions
#
#   a is api name found in test name
#   p is what is in the spec, may contain parameters {}
#
#
def matchAPIPath(a, p):
    return a.lower() in p.lower().replace("{", "").replace("}", "") 


def getPathsFromSpec(spec):
    spec = spec.lower()
    if spec in apidef: 
        return apidef[spec]
    else:
        return {}
        
# end utility api spec loading functions


def main():
    init()
    print ("\n --- Attack info \n")
    for (aname, x) in attackinfo.items():
        print (" '%s' " % (aname))
    print ("\n --- API info \n")
    for (spec, a) in apidef.items():
        print ("\n spec: '%s'\n" % spec)
        for ( p, x) in a.items():
           print (" %s " % p)
    print ("\n --------------------\n")


    
if __name__ == "__main__":
    # execute only if run as a script
    main()


