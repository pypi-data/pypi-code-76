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
from cvdastwrapper import reportutil
from cvdastwrapper import sumreport

from cvdastwrapper import runconfig

from cvdastwrapper.runperapi import perapicall
from cvdastwrapper.runperattack import perattackcall
from cvdastwrapper.runconfig import fuzzattacklist
from cvdastwrapper.htmlreportgenerator import iterateallspecs, generate_html_report

from datetime import datetime

#
# process argv, to figure out whether custom
#  output file exists and whether timestamps
#  shoutl be added
#
def processFnames(inargv, postfix, defaultf, defaultt):
    #print(inargv, postfix, defaultf, defaultt, "----")
    if len(inargv) > 2:
        if inargv[2].endswith(postfix):
            return (inargv[2], False, False)
        if len (inargv) > 3:
            if inargv[3].endswith(postfix):
                return (inargv[3], False, False)
    return (defaultf, defaultt, True) 

def main():
    regen = False
    csvfname  = runconfig.dcsvreportfname
    htmlfname = runconfig.dhtmlreportfname
    addhtmltstamp = runconfig.attachtimestamptoreport
    addcsvtstamp = runconfig.attachtimestamptoreport

    usagestr  = "\n Usage: [regen or test: Default test] [an .html report filename: Default "+runconfig.dhtmlreportfname+"-<timestamp>] [a .csv report filename: Default "+runconfig.dcsvreportfname+"<timestamp>] (Timestamp will not be added to user specified filenames; can specify one or both custom report name as long as .html/.csv postfixes are specified.)\n"
    
    #print(sys.argv, "sysrgv")
    if (len(sys.argv) > 1):
        if sys.argv[1].startswith("regen"):
            regen=True
        elif not sys.argv[1].startswith("test"):
            print (usagestr)
            return
        if (len(sys.argv) > 2):
            (htmlfname, addhtmltstamp, notfound1) = processFnames(sys.argv, ".html", htmlfname, addhtmltstamp)
            (csvfname,  addcsvtstamp,  notfound2) = processFnames(sys.argv, ".csv",  csvfname,  addcsvtstamp)
            if notfound1 and notfound2:
                print(usagestr)
                return

    tnow = datetime.now()
    tstamp = tnow.strftime("%Y%m%d%H%M%S")
    if addhtmltstamp:
        htmlfname = htmlfname+"-"+tstamp+".html"
    if addcsvtstamp:
        csvfname  = csvfname+"-"+tstamp+".csv"
    
    reportutil.init()

    print("\n Testing APIs and generating html report in %s and csv report in %s \n" % (htmlfname, csvfname))
    ra = ""
    hs = "<html>\n<head>\n<style>\ntable, th, td {\n  border: 1px dotted black;\n border-collapse: collapse}</style>\n<title>API Test Report Summary</title></head><body><br>\n"
    print ("\n------- Starting API Tests: Testing all APIs in a spec one fuzz attack type at a time. \n")
    #print(regen, runconfig.apispeclist, fuzzattacklist, dir(runconfig))
    ra = perattackcall(regen, runconfig.apispeclist, fuzzattacklist)
    
    (rsum, detail, rfailed, rskipped) = sumreport.sumperattack(csvfname, runconfig.apispeclist, fuzzattacklist)
    
    f = open(htmlfname, "w+")
    f.write(hs)
    if rsum:
        f.write("\n<h2>Test Summary</h2><br>\n" + rsum)
    if rfailed:
        f.write("\n<h3>Failed Test Reports Per API</h3><br>\n" + rfailed)
    if detail:
        f.write("\n<h2>Detailed Per Attack Test Report</h2><br>\n" + detail)
    if rskipped:
        f.write("\n<h3>Skipped Test Reports Per Spec</h3><br>\n" + rskipped)
#    if ra:
#        hs += "\n<h3>Reports Per Attack</h3><br>\n" + ra
#    if rb:
#        hs += "\n<h3>Reports Per API</h3><br>\n" + rb

    f.write("\n\n</body></html>")
    f.close()

    result_report = iterateallspecs(runconfig.apispeclist, runconfig.fuzzattacklist)
    #print("-----+++",result_report)
    generate_html_report(result_report, "report_summary_"+str(time.time())+".html")
    
if __name__ == "__main__":
    # execute only if run as a script
    main()

