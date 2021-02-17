#!/usr/bin/python

import json
import re
import collections
import os
import time
import datetime
import sys


import cvdast.CloudvectorDAST
import shutil
from cvdastwrapper import runonetest
from cvdastwrapper import runconfig
from cvdastwrapper.runconfig import inspecdir
from cvdastwrapper.runconfig import dlogrespdname
from cvdastwrapper.runconfig import dloginputdname
from cvdastwrapper.runconfig import apispeclist, fuzzattacklist
from cvdastwrapper.html_content_gen import generate_test_report
from jinja2 import Environment, FileSystemLoader
from cvdastwrapper import reportutil
from cvdastwrapper import apispecs

resultrootn = runconfig.dresultdir + "/" + runconfig.dperadir + "/"
ainfofname = runconfig.dainfofname
global data
data = {"test_spec_insights": {}, "summary": {}, "metadata_spec": []}


def moveToNoRetest(rval, api):
    if "retest" in rval["skipped"]:
        if api in rval["skipped"]["retest"]:
            objs = rval["skipped"]["retest"][api]
            for obj in objs:
                if obj["reason"] == "--":
                    obj["reason"] = "Test calls with same attack type has generated passed/failed outcome."
            if not "no-retest" in rval["skipped"]:
                rval["skipped"]["no-retest"] = {api: obj}
            elif api in rval["skipped"]["no-retest"]:
                rval["skipped"]["no-retest"][api].append(obj)
            else:
                rval["skipped"]["no-retest"][api] = {api: obj}
            del rval["skipped"]["retest"][api]
    if "no-retest" in rval["skipped"]:
        if api in rval["skipped"]["no-retest"]:
            if isinstance(rval["skipped"]["no-retest"][api], list):
                for each_api in rval["skipped"]["no-retest"][api]:
                    reason = each_api.get('reason')
                if reason.find("Also") < 0 :
                    rval["skipped"]["no-retest"][api][0]['reason'] += ". Also test calls with same attack type has generated passed/failed outcome."
            else:
                reason =rval["skipped"]["no-retest"][api].get('reason')
                if reason.find("Also") < 0 :
                    rval["skipped"]["no-retest"][api]['reason'] += ". Also test calls with same attack type has generated passed/failed outcome."
# end moveToNoRetest


def parseStdoutForInput(instdout):
    request = ''
    curl_str = 'CURL command to retry:'
    delimiter_str = '\n\n---------------------------------\n\n'
    curl_pos = instdout.find(curl_str)
    if curl_pos < 0:
        return request
    curl_req_str = instdout[curl_pos + len(curl_str):]
    del_pos = curl_req_str.find(delimiter_str)
    if del_pos < 0:
        request = curl_req_str
    else:
        request =  curl_req_str[:del_pos]
    return request
# end parseStdoutForInput

#
# Given a dict of a report.json from perattack, extract per-api reports of test data
#  contains two dicts, one is "tested", one is "skipped", each skip has either
#  "no-retest"/"retest" status. No-retest can be no fuzzing needed or same attack, same api
#  test has passed/failed in another test
#


def extractAPITests(attack, severity, inreport, inainfo):
    rval = {"tested": {}, "skipped": {}}
    alltests = inreport["report"]["tests"]

    cnt = 0
    for onetest in alltests:
        cnt += 1
        name = onetest["name"]
        tname = name.split("::")[1]

        s = tname[len("test_"):]
        method = s[:s.find("_")]
        api = s[s.find("_")+1:s.find("_for_fuzzing")
                ].replace("__", "/").replace("9i9", "-")
        # print ("\n tname: %s \napi picked %s , method %s , \n. " % (tname, api, method))
        if not "call" in onetest:
            # print(" no call element in %s, attack %s, test #%d  , outcome is %s" % (spec, attack, cnt, onetest["outcome"]))
            continue
        # outcome can be pass/failed/skipped
        outcome = onetest["outcome"].lower()
        meta = onetest["metadata"][0]
        inobj = {"api": api, "method": method, "outcome": outcome, "attack": attack,
                 "severity": severity, "attackinfo": inainfo, "testinput": ""}

        if not outcome == "skipped":      # has a passed/failed outcome
            mdata = meta.split("::")
            inobj["resp"] = mdata[4]       # get the response code
            inobj["respmsg"] = mdata[6]
            # last one is the attack pattern file
            inobj["apatternfile"] = mdata[len(mdata)-1]
            if "stdout" in onetest["call"]:
                inputstr = parseStdoutForInput(onetest["call"]["stdout"])
                if inputstr:
                    # print(" --- \n failed test input: %s" % inputstr)
                    inobj["testinput"] = inputstr
            if outcome == "failed":
                # sometimes the attack pattern file name is missing from the report
                if not inobj["apatternfile"]:
                    inobj["apatternfile"] = reportutil.patchAttackPatternFile(
                        attack)
                    # print(" in a failed test, attack %s, test %d, no attack pattern file recorded in metadata: <<<%s>>>, pick a sample file from the attack pattern dir: %s" % (attack, cnt, meta, inobj["apatternfile"]))
                    # print("--- Debug, cannot find attack pattern file in here: \n %s ----------- Debug --- \n" % onetest)
                # else:
                    # print("\n -- Debug %s -- \n" % meta)

        if (outcome == "skipped"):
            i = meta.find("SKIP_REASON-->")
            reason = ""
            if i > 0:
                reason = meta[i+len("SKIP_REASON-->"):meta.find("::", i)]
            if reason:
                inobj["reason"] = reason
            else:
                inobj["reason"] = "--"

            designation = "retest"
            if (reason and (reason.startswith("No values for the parameters") or reason.startswith("No Parameters to fuzz"))):
                designation = "no-retest"
            if api in rval["tested"]:
                designation = "no-retest"
                if reason == "--":
                    reason = "Test calls with same attack type has generated passed/failed outcome."
                else:
                    reason += ". Also test calls with same attack type has generated passed/failed outcome."

            if designation in rval["skipped"]:
                if api in rval["skipped"][designation]:
                    rval["skipped"][designation][api].append(inobj)
                else:
                    rval["skipped"][designation][api] = [inobj]
            else:
                rval["skipped"][designation] = {api: [inobj]}
        else:
            # if any api is found not to skipped, move that api from retest to no retest
            moveToNoRetest(rval, api)
            # tests sharing the same outcome is saved in a list
            if outcome in rval["tested"]:
                rval["tested"][outcome].append(inobj)
            else:
                rval["tested"][outcome] = [inobj]
    ''' end for tests '''
    return rval

#
# for a particular spec, analyze all failed tests
#  group them into a list of 4 priorties
#   * returned data + severity Critical or H, P1
#   * returned data, other severity           P2
#   * no returned data, C or H severity,      P3
#   * all others                              P4
#
# failedr(eport) is a structure
#   /spec/api/[p1,p2,p3,p4] at which
#       /method(get,post,delete)/
#         ({response-code:[attacks]}, {attackname:[attack-patternfiles]})
#


"""
def APIsByPriorityReport(apilist_pri_report, spec, newtests):
    ele = newtests["tested"]
    failed = ele.get("failed", [])

    for a in failed:
        pri = 4
        api = a["api"]
        sev = a["severity"]
        rsp = a["resp"]
        att = a["attack"]
        m = a["method"]
        attf = a["apatternfile"]

        if spec in apilist_pri_report:
            for eachapi in apilist_pri_report[spec]:
                if api in eachapi:
                    for eachmethod in api:
                        if attk in eachmethod:
                            for severity in eachmethod[attk]:
                                if severity.get("severity") == sev:
                                    if "failed" in severity:
                                        severity["failed"] = severity["failed"] + 1
                                    else:
                                        severity["failed"] = 1
                                else:
                                    severity = {}
                                    severity["severity"] = sev
                                    severity["failed"] = 1
                        else:
                            eachmethod["attk"] = att

    if "failed" in ele:
        if not spec in apilist_pri_report:
            apilist_pri_report[spec] = {}
        spec_element = apilist_pri_report[spec]

        for a in ele["failed"]:
            pri = 4
            api = a["api"]
            sev = a["severity"]
            rsp = a["resp"]
            att = a["attack"]
            m = a["method"]
            attf = a["apatternfile"]

            if rsp and rsp.startswith("200-->"):
                if len(rsp) > len("200-->[]") and (not rsp == "200-->null"):
                    if sev.lower().startswith("c") or sev.lower().startswith("h"):
                        pri = 1
                    else:
                        pri = 2
            if sev.lower().startswith("c") or sev.lower().startswith("h"):
                if pri > 3:
                    pri = 3
            orgele = {}
            if api in spec_element:
                orgele = spec_element[api][pri-1]
            else:
                spec_element[api] = [{}, {}, {}, {}]
                orgele = spec_element[api][pri-1]

            '''
            rsp=rsp.lower()
            if m.lower() in orgele:
                (morgele, afdic) = orgele[m.lower()]
                if rsp in morgele :
                    if not att in morgele[rsp]:
                        morgele[rsp].append(att)
                else:
                    morgele[rsp] = [att]
                if attf :
                    if att in afdic:
                        if not attf in afdic[att]:
                            afdic[att].append(attf)
                    else:
                        afdic[att] = [attf]

            else:
                if attf:
                    orgele[m.lower()] = ({rsp: [att]}, {att: [attf]})
                else:
                    orgele[m.lower()] = ({rsp: [att]}, {})
               '''


''' end failedTestReport '''
"""


def iterateallspecs(inspeclist=[], inattacklist=[]):
    ainfo = {}
    thespeclist = inspeclist if inspeclist else runconfig.apispeclist
    theattacklist = inattacklist if inattacklist else runconfig.fuzzattacklist

    sumr = {}           # summary test report filled in by sumPerSpec
    apilist_pri_report = {
        "total_tests": 0,
        "total_passed": 0,
        "total_failed": 0,
        "all_failed_apis": set(),
        "total_count": 0,
        "critical_count": 0,
        "high_count": 0,
        "medium_count": 0,
        "low_count": 0,
        "attack_category": {},
        "all_apis": set(),
        "failed_cc": 0,
        "failed_hc": 0,
        "failed_mc": 0,
        "failed_lc": 0,
    }        # failed test report by failedTestReport

    inputfilenum = 0
    for spec in thespeclist:
        #print(resultrootn+spec, " resultrootn+spec")
        spec = spec.lower()   # important, cannonical form of spec all lower case
        if not os.path.exists(resultrootn+spec):
            print("-- Failed to generate summary report: %s does not exist. " %
                  resultrootn+spec)
            return ""

        an = 0
        firstattack = True
        srow = 0
        dahtml = ""
        spec_report = {
            "apis_by_priority": {
                "p1": set(),
                "p2": set(),
                "p3": set(),
                "p4": set(),
            },
            "priority_count": {
                "p1_count": 0,
                "p2_count": 0,
                "p3_count": 0,
                "p4_count": 0
            },
            "total_tests_count": 0,
            "total_failed_count": 0,
            "total_passed_count": 0,
            "skipped_tests_count": 0,
            "all_spec_apis": set(),
            "all_failed_apis": set(),
        }
        #print(theattacklist, "THEATTACXKLIST")
        for a in theattacklist:
            arname = a
            if arname.find("/"):
                arname = arname.replace("/", "_")

            if not ainfo:
                ainfo = reportutil.findAttackInfoObjs(theattacklist)
            if not a in ainfo:
                print(" Attack info not found for %s in attackinfo: %s" %
                      (a, ainfo))
                continue
            severity = ainfo[a][0]
            classification = ainfo[a][1]["classification"]

            originalr = resultrootn+spec+"/"+arname+"-report.json"

            if not os.path.exists(originalr):
                print(" Cannot regenerate report for %s , %s does not exists." % (
                    spec+"_"+arname, originalr))
                continue
            with open(originalr) as f:
                areporti = json.load(f)
                f.close()

            originalhtml = resultrootn+spec+"/"+arname+".html"
            if not os.path.exists(originalhtml):
                print(" Cannot regenerate html report for %s , %s does not exists." % (
                    spec+"_"+arname, originalhtml))
                continue
            tests = extractAPITests(a, severity, areporti, ainfo)
            # print("List of Tested and Skipped per attack category: {}".format(tests))

            # if 'failed' in tests['tested']:
            #    print(tests["tested"]["failed"][0])
            #    print("\n\n\n\n")
            # if 'passed' in tests['tested']:
            #    print(tests["tested"]["passed"][0])

            # Get information for Failed Tests table
            apilist_pri_report[spec] = spec_report
            generate_test_report(apilist_pri_report, spec, tests)

        #print("Report for Spec: {} is {}".format(spec, apilist_pri_report))
    return apilist_pri_report


def get_most_frequent_attack(report_json):
    attack_category_json = report_json['attack_category']
    if not attack_category_json:
        return {}
    sorted(attack_category_json.items(), key=lambda item: 'count')
    #print(attack_category_json)    
    res = list(attack_category_json.keys())[0]
    val = attack_category_json[res]
    freq_string = res + " - " + str(val['count']) + \
        " Tests Failed Across " + \
        str(len(val['p1_apis']) + len(val['p2_apis']) +
            len(val['p3_apis']) + len(val['p4_apis'])) + " APIs."
    return freq_string


def get_attack_catogery_count(report_json):
    res = {}
    attack_category = report_json.get('attack_category', {})
    for key, value in attack_category.items():
        res[key] = {}
        res[key]['all_apis_count'] = len(value.get('all_apis', set()))
        if len(value.get('p1_apis', set())):
            res[key]['pri_count'] = len(value['p1_apis'])
            res[key]['priority'] = 'Critical'
        elif len(value.get('p2_apis', set())):
            res[key]['pri_count'] = len(value['p2_apis'])
            res[key]['priority'] = 'High'
        elif len(value.get('p3_apis', set())):
            res[key]['pri_count'] = len(value['p3_apis'])
            res[key]['priority'] = 'Medium'
        else:
            res[key]['pri_count'] = len(value['p4_apis'])
            res[key]['priority'] = 'Low'
    return res


def get_spec_details(report_json):
    res = {}
    api_count = 0    
    apispeclist = apispecs.apispeclist
    #print(apispeclist, "APISPECLIST")
    for spec in apispeclist:
        res[spec] = report_json[spec]
        pri = report_json[spec]['apis_by_priority']
        api_count = len(pri['p1']) + len(pri['p2']) + \
            len(pri['p3']) + len(pri['p4'])
        res[spec]['api_count'] = api_count
        res[spec]['count_by_api_priority'] = {
            'p1': len(pri['p1']),
            'p2': len(pri['p2']),
            'p3': len(pri['p3']),
            'p4': len(pri['p4'])
        }
        res[spec]['all_apis_count'] = len(report_json[spec]['all_spec_apis'])
        res[spec]['failed_apis_count'] = len(
            report_json[spec]['all_failed_apis'])
        api_details = {}
        for api_key, value in report_json.get(spec, {}).items():
            if '/' in api_key:
                values_list = []
                for key, info in value.items():
                    if info.get('pri', '') == 'p1':
                        info['pri'] = 1
                    elif info.get('pri', '') == 'p2':
                        info['pri'] = 2
                    elif info.get('pri', '') == 'p3':
                        info['pri'] = 3
                    else:
                        info['pri'] = 4
                    values_list.append(info)
                api_details[api_key] = values_list
        res[spec]['api_details'] = api_details
    return res


def generate_html_report(result_report_json, filename):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    # print(templates_dir, root) - root is project root directory that is report_gen
    template = env.get_template('index.html')
    #print(result_report_json, "RRRRRRRRRR")
    frequent_attack = get_most_frequent_attack(result_report_json)
    category_counts = get_attack_catogery_count(result_report_json)
    spec_details = get_spec_details(result_report_json)
    #print(spec_details, "_____+++++++")
    #print(runconfig.fuzzattacklist, "oooooo")
    with open(filename, 'w') as fh:
        fh.write(template.render(
            num_spec_files=len(apispecs.apispeclist),
            num_total_apis=len(result_report_json.get('all_apis')),
            num_dst_hosts=1,  # TODO: len(runconfig.dhostname)
            num_attack_categ=len(runconfig.fuzzattacklist),
            

            total_attack_vectors=result_report_json.get('total_count'),
            total_critical_av_count=result_report_json.get('critical_count'),
            total_high_av_count=result_report_json.get('high_count'),
            total_medium_av_count=result_report_json.get('medium_count'),
            total_low_av_count=result_report_json.get('low_count'),
            av_count_list=[result_report_json.get('critical_count'), result_report_json.get('high_count'),
                           result_report_json.get('medium_count'), result_report_json.get('low_count')],

            total_vul_apis=len(result_report_json.get('all_failed_apis')),

            total_tests=result_report_json.get('total_tests'),
            passed_count=result_report_json.get('total_passed'),
            failed_count=result_report_json.get('total_failed'),

            failed_critical_count=result_report_json.get('failed_cc'),
            failed_high_count=result_report_json.get('failed_hc'),
            failed_medium_count=result_report_json.get('failed_mc'),
            failed_low_count=result_report_json.get('failed_lc'),

            attack_category=category_counts,

            spec_details=spec_details,
            frequent_attack=frequent_attack
        ))

    return


def main():
    print("\n\n")
    print("\t" * 7 + "# /***************************************************************\\")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **  / ___| | ___  _   _  __| \ \   / /__  ___| |_ ___  _ __  **")
    print("\t" * 7 + "# ** | |   | |/ _ \| | | |/ _` |\ \ / / _ \/ __| __/ _ \| '__| **")
    print(
        "\t" * 7 + "# ** | |___| | (_) | |_| | (_| | \ V /  __/ (__| || (_) | |    **")
    print("\t" * 7 + "# **  \____|_|\___/ \__,_|\__,_|  \_/ \___|\___|\__\___/|_|    **")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **      (c) Copyright 2018 & onward, CloudVector             **")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **  For license terms, refer to distribution info            **")
    print("\t" * 7 + "# \***************************************************************/\n\n")

    print("*****" * 20)
    print("CloudVector IAST - Report Generation plugin")
    print("*****" * 20)

    reportutil.init()
    result_report = iterateallspecs(apispeclist, runconfig.fuzzattacklist)    
    generate_html_report(result_report, "sample.html")


if __name__ == "__main__":
    # execute only if run as a script
    main()
