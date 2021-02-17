#!/usr/bin/python

import json
import re
import collections
import os
import time, datetime
import sys


import cvdast.CloudvectorDAST
import shutil
from cvdastwrapper import runonetest
from cvdastwrapper import runconfig

resultrootn = runconfig.dresultdir+"/" + runconfig.dperapidir +"/"

def perapicall(regenreport=False, inspeclist=[]):
    rhtml = "<table><tr><th>API Specification</th><th>Per API Reports</th></tr>\n"
    i=1
    thespeclist = inspeclist if inspeclist else runconfig.apispeclist
    
    for spec in thespeclist : 
        if not os.path.exists(resultrootn+spec):
            os.mkdir(resultrootn+spec)

        rhtml += "\n<tr><td>" + spec + "</td>\n"
        rhtml += "\n<td><b>Report Based on Each Individual APIs:</b><ul>"
        specnl = spec.lower() + "_tests"
        if not os.path.exists(specnl):
            print ("Spec directory %s does not exists! " % specnl)
            continue
    
        for apy in os.listdir(specnl) :
            if not apy.endswith("_for_fuzzing.py"):
                continue

            #startstr = "test___"+spec+"__api__"
            startstr = "test___"+spec
            endstr   = "_for_fuzzing.py"
            shortapiname = apy[apy.find(startstr)+len(startstr):apy.find(endstr)]
            print(i)
            i+=1


            if not regenreport:
                if i % 10 == 0 :
                    print("\n wait ... \n")
                    time.sleep(10)
                print("Spec %s , testing %s, result %s, %s" %
                      (spec, specnl+"/"+apy, resultrootn+spec+"/"+shortapiname+".html",resultrootn+spec+"/"+shortapiname+"-report.json"))                 
                runonetest.runtest(spec, apy,
                                   runconfig.dhostname,
                                   resultrootn+spec+"/"+shortapiname+".html",
                                   "All", "1")
        
                if os.path.exists("report.json") :
                    shutil.copy("report.json", resultrootn+spec+"/"+shortapiname+"-report.json")
                    
            else:
                originalr = resultrootn+spec+"/"+shortapiname+"-report.json"
                # adding a backward compatible case where __api__ was stripped
                #  off
                #
                if not os.path.exists(originalr):
                    shortapiname = shortapiname[7:]
                    originalr = resultrootn+spec+"/"+shortapiname+"-report.json"
                if os.path.exists(originalr):
                    shutil.copy(originalr, "report.json")
                else:
                    print(" Cannot regenerate report for %s , %s does not exists." % (spec+"_"+shortapiname, originalr))
                
                print("Spec_API %s , regenerating html reportto %s " %
                      (specnl+"_"+shortapiname, resultrootn+spec+"/"+shortapiname+"-report.json"))

                '''create attack_info.json if it does not exists'''
                if not os.path.exists("tests"):
                    os.mkdir("tests")
                if not os.path.exists("tests/data"):
                    os.mkdir("tests/data")
                if not os.path.exists("mytests/attack_info.json"):
                    if not os.path.exists(specnl+"/data/attack_info.json"):
                        print("Missing attack_info %s, please run fuzzing or make sure mytests/attack_info.json exists." % (specnl+"/data/attack_info.json"))
                        return
                    else:
                        shutil.copy(specnl+"/data/attack_info.json", "tests/data/")
                else:
                    shutil.copy("mytests/attack_info.json", "tests/data/")

                cvdast.CloudvectorDAST.CloudvectorDAST.generate_fuzz_report(resultrootn+spec+"/"+shortapiname+".html")

            rhtml+= "\n<li><a href=\""+resultrootn+spec+"/"+shortapiname+".html"+"\">" + shortapiname + "</a>"
        rhtml += "\n</ul>\n</td></tr>\n"
    rhtml += "</table>\n"
    return rhtml
'''end perapicall'''

def main():
    r=""
    if (len(sys.argv) > 1):
        if sys.argv[1].startswith("regen"):
            r=perapicall(True)
        else: 
            print ("\n Usage: [Optional flag regenreport to just regenerate the reports, run all tests on a per API basis. \n")
            return
    else:
        r=perapicall(False)
    print(r)

    
if __name__ == "__main__":
    # execute only if run as a script
    main()

