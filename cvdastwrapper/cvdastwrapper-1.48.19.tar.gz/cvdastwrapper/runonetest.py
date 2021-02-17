#!/usr/bin/python

import json
import re
import collections
import os
import time, datetime
import sys


import cvdast.CloudvectorDAST
import shutil

from cvdastwrapper.runconfig import dspecnamec
from cvdastwrapper.runconfig import dhostname
from cvdastwrapper.runconfig import dcviast_fuzz_type
from cvdastwrapper.runconfig import dcviast_max_value_to_fuzz
from cvdastwrapper.runconfig import dtestdirname 

from cvdastwrapper.runconfig import dresultdir 
from cvdastwrapper.runconfig import dperadir   
from cvdastwrapper.runconfig import dperapidir 

#specnamec is specname w capital letters
#
# return a link to the result
#
def runtest(specnamec,
            perapifname, 
            targethost,
            resulthtml,
            cviast_fuzz_type="All", 
            cviast_max_value_to_fuzz="1"):
    fulltestname = dtestdirname
    if not specnamec:
        specnamec=dspecnamec

    specnamel    = specnamec.lower()
    testdirname  = specnamel + "_tests"
    if perapifname: 
        fulltestname = testdirname + "/" + perapifname
    else:
        fulltestname = testdirname
    
    if not targethost:
        targethost = dhostname
    if not targethost:
        return ""

    if not cviast_fuzz_type:
        cviast_fuzz_type=dcviast_fuzz_type

    os.environ["CVIAST_FUZZ_TYPE"] = cviast_fuzz_type
    os.environ["CVIAST_MAX_VALUE_TO_FUZZ"] = cviast_max_value_to_fuzz

    sys.argv=["CloudVectorDAST",
              "--execute",
              fulltestname,
              "--host="+targethost]
    if resulthtml:
        sys.argv.append("--report-out="+resulthtml)
        
    '''create attack_info.json if it does not exists'''
    if not os.path.exists("tests"):
        os.mkdir("tests")
    if not os.path.exists("tests/data"):
        os.mkdir("tests/data")
    if not os.path.exists("test/data/attack_info.json"):
        shutil.copy(testdirname+"/data/attack_info.json", "tests/data/")

    print ("Type %s (max=%s) calling cloudvector main with this arg %s" % ( cviast_fuzz_type, cviast_max_value_to_fuzz, sys.argv))
    cvdast.CloudvectorDAST.main()
    
    

def getAllAttacks(adir):
    adict = {}
    for (root, dirs, __) in os.walk(adir):
        for d in dirs:
            rname = ""
            attackname = ""
            if len(root) > len(adir) :
                rname = root[len(adir):]
            if rname and rname in adict :
                del adict[rname]
            if rname:
                attackname = rname + "/" + d
            else: 
                attackname = d
            adict[attackname] = 1

    return list(adict.keys())





speclist=["CpmGateway",
          "TelemetryGateway"]
attacklist = ['xml', 'json']

'''
attlist=getAllAttacks("fuzzdb/attack/")            
speclist=["CpmGateway",
          "MedCabinetGateway",
          "MedServerGateway",
          "OisGateway",
          "OmniCenterGateway",
          "SupplyXGateway",
          "TelemetryGateway"]

attacklist = ['control-chars', 'string-expansion', 'server-side-include', 'xpath', 'unicode', 'html_js_fuzz', 'disclosure-directory', 'xss', 'os-cmd-execution', 'disclosure-source', 'format-strings', 'xml', 'integer-overflow', 'path-traversal', 'json', 'mimetypes', 'redirect', 'os-dir-indexing', 'no-sql-injection', 'authentication', 'http-protocol', 'business-logic', 'disclosure-localpaths/unix', 'file-upload/malicious-images', 'sql-injection/detect', 'sql-injection/exploit', 'sql-injection/payloads-sql-blind']
'''
'''print(attlist)'''
'''runatest("", "", "", "")'''


