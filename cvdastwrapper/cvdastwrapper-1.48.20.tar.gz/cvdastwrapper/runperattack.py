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

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"

def perattackcall(regenreport=False, inspeclist=[], inattacklist=[]):
    rhtml = "<table><tr><th>API Specification</th><th>Per Attack Reports</th></tr>\n"
    i=1
    thespeclist   = inspeclist if inspeclist else runconfig.apispeclist
    theattacklist = inattacklist if inattacklist else runconfig.fuzzattacklist
    for spec in thespeclist:
        spec = spec.lower()  # important: use all lower case cannonical form
        if not os.path.exists(resultrootn+spec):
            os.mkdir(resultrootn+spec)

        rhtml += "\n<tr><td>" + spec + "</td>\n"
        rhtml += "\n<td><b>Report Based on Each Attack Type:</b><ul>"
        for a in theattacklist: 
            arname = a
            if arname.find("/"):
                arname = arname.replace("/", "_")
            print(i)
            i+=1

            if not regenreport:
                #if i % 10 == 0 :
                    #print("\n wait ... \n")
                    #time.sleep(10)
                    
                runonetest.runtest(spec, "",
                                   runconfig.dhostname,
                                   resultrootn+spec+"/"+arname+".html",
                                   a, runconfig.dperattackvalueused)

                if os.path.exists("report.json") :
                    shutil.copy("report.json", resultrootn+spec+"/"+arname+"-report.json")
            else:
                originalr = resultrootn+spec+"/"+arname+"-report.json"
                if os.path.exists(originalr):
                    shutil.copy(originalr, "report.json")
                else:
                    print(" Cannot regenerate report for %s , %s does not exists." % (spec+"_"+arname, originalr))
                    continue

                print("Spec_API %s , regenerating html report to %s " %
                      (spec+"_"+arname, resultrootn+spec+"/"+arname+".html"))

                if not os.path.exists("tests"):
                    os.mkdir("tests")
                if not os.path.exists("tests/data"):
                    os.mkdir("tests/data")
                if not os.path.exists("mytests/attack_info.json"):
                    if not os.path.exists(spec.lower()+"_tests/data/attack_info.json"):
                        print("Missing attack_info %s, please run fuzzing or make sure mytests/attack_info.json exists." % (spec.lower()+"_tests/data/attack_info.json"))
                    else:
                        shutil.copy(spec+"_tests/data/attack_info.json", "tests/data/")
                else:
                    shutil.copy("mytests/attack_info.json", "tests/data/")
                cvdast.CloudvectorDAST.CloudvectorDAST.generate_fuzz_report(resultrootn+spec+"/"+arname+".html")

            rhtml+= "\n<li><a href=\""+resultrootn+spec+"/"+arname+".html"+"\">" + arname + "</a>"
        rhtml += "\n</ul>\n</td></tr>\n"
    rhtml += "</table>\n"
    return rhtml
                

''' end perattackcall '''


def main():
    r = ""
    if (len(sys.argv) > 1):
        if sys.argv[1].startswith("regen"):
            r=perattackcall(True)
        else: 
            print ("\n Usage: [Optional flag regenreport to just regenerate the reports, run all tests on a per API basis. \n")
            return
    else:
        r=perattackcall(False)
    print(r)

    
if __name__ == "__main__":
    # execute only if run as a script
    main()


