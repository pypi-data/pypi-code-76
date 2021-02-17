#!/usr/bin/python

import json
import re
import collections
import os
import time, datetime

#import yaml
#import shutil
#from jinja2 import Template
#from copy import deepcopy
#import requests

#import pytest
#from cvapianalyser import CommunityEdition
#from openapispecdiff import OpenApiSpecDiff


import cvdast.CloudvectorDAST
import shutil
import sys

from cvdastwrapper.runconfig import inspecdir 
from cvdastwrapper import runconfig

def fuzzspecs(specdir = inspecdir):
    
    sfs = []
    for (__,__, filename) in os.walk(specdir):
        sfs.extend(filename)
        break

    tfs = []
    specnames = []
    #print(sfs,".....")
    for spec in sfs:
        
        if not spec.endswith(".json"):
            continue
        specfname = specdir+"/"+spec
        #print(specfname)
        testdir   = spec[:-5].lower() + "_tests" # important, convert specs to all lower case 
        tfs.append(testdir)
        specnames.append(spec[:-5].lower())      # convert specs to all lower case 
        print ("------- Processing %s, generating %s \n"  % (specfname, testdir))
    

        cvdast.CloudvectorDAST.CloudvectorDAST("",
                                               specfname,
                                               "",
                                               runconfig.dfuzzusrname,
                                               "",
                                               runconfig.dcvconfig,
                                               "n",
                                               "",
                                               True)

        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)),"auth.py"), "tests")
        if os.path.exists(testdir):
            shutil.rmtree(testdir)
    
        '''custom attack_info.json over-write tests/data'''
        if os.path.exists("mytests/attack_info.json"):
            print ("----------- Overwriting attack_info -------")
            shutil.copy("mytests/attack_info.json", "tests/data/")

        if not os.path.exists("savedattackinfo"):
            os.mkdir("savedattackinfo")
            shutil.copy("tests/data/attack_info.json", "savedattackinfo/attack_info.json")

        os.rename("tests", testdir)
        print ("------- Done Processing %s, generating %s \n"  % (specfname, testdir))

    ''' 
    # spec name should not be expected as part of the test file, 
    #  it was a coincident in the case of basepath containing spec name
    #
    specnames=[]
    for f in tfs:
        for tf in os.listdir(f):
            if tf.startswith("test___") and tf.endswith("fuzzing.py") :
                startstr = "test___"
                endstr   = "__"
                sindex   = tf.find(startstr)+len(startstr)
                shortspecname = tf[sindex:tf.find(endstr, sindex)]
                specnames.append(shortspecname)
                break
    '''
    
    print ("\n\n----Done Fuzzing all specs -----------------------------------------\n\n")
    from cvdastwrapper import apispecs
    apispecs.apispeclist = specnames
    
    f = open(runconfig.genspeclistpyfname, "w+")
    f.write("#!/usr/bin/python \n")
    f.write("apispeclist=%s" %(specnames))
    f.close()
    #print ("\n You can update runconfig.py with this complete API spec list: \n\n apispeclist=%s \n\n" % specnames)
    
'''end of fuzzspecs'''

def main():
    if (len(sys.argv) > 1):
        if sys.argv[1].startswith("--help") or sys.argv[1].startswith("-help") or sys.argv[1].startswith("help"):
            print ("\n Usage: [Optional name of directory containing json specs, Default: specs]\n")
            return
        
        fuzzspecs(sys.argv[1])
    else:
        fuzzspecs()

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


