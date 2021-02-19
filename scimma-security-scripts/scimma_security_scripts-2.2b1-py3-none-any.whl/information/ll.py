#!/usr/bin/env python
"""
utilities
standard strinfgs
"""

import json
import glob
import os

L0A_dir = "./report_files/L0A"
L0B_dir = "/Users/ekimtco2/PycharmProjects/security-scripts/security_scripts/information/report_files/L0B"
L1_dir  = "./report_files/L1"


def jsons_from_dir(dir):
    """
    return binary json contents of file
    and base file name.
    """
    file_glob=os.path.join(dir,"*.json")
    for filename in glob.iglob(file_glob):
        jlist = json_from_file(filename)
        yield jlist, os.path.basename(filename)

def json_from_file(filename):
    "return binary json contents from a file)"
    jf = open(filename,"r")
    jlist = json.load(jf)
    jf.close()
    return jlist

def json_to_file(fdir, fn, jlist):
    """
    Write a file given a list binary JSON objects.
    """
    jlist = [json.dumps(item) for item in jlist]
    jtext = ",".join(jlist)
    jtext = "[" + jtext + "]"
    L0B_file_name = os.path.join(fdir,fn)
    f=open(L0B_file_name, "w")
    f.write(jtext)
    f.close()





    
    

