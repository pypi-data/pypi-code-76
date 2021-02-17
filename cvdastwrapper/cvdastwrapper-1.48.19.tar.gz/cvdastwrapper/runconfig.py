#
# A set of configuration values that can be
#  modified to fit customers environment
#

#
# Customer specific config
#  These are variables that most likely needed to be modified
#  to fit customers environment
#
    
import os

inspecdir = os.path.join(os.getcwd(),"specs")                           # default spec folder name, no /
dfuzzusrname="cvbot@cloudvector.com"          # username to use for fuzzing
dcvconfig=os.path.join(os.getcwd(),"cv_config.yaml")                 # config .yaml file for fuzzing
dspecnamec="ob"                               # default spec to use when running test, sample orangebank app shown here
#dhostname="http://40.117.155.144:32143/"      # api service hostname
#dhostname = input("host: ") or "http://40.117.155.144:32143/"
#dhostname = ""
#
# Default values: a set of default values in case
#  nothing is customized. 
#
dcviast_fuzz_type="string-expansion"       # default fuzz type to use
dcviast_max_value_to_fuzz="1"              # default max value to fuzz if running runonetest directly
dtestdirname = os.path.join(os.getcwd(),"tests")                     # folder under which tests are saved
dfuzzdbdirname  = "fuzzdb"                 # folder under which fuzzdb is stroed

dsavedreportd = "savedreports"             # a folder under which reports are saved

dlogrespdname  = "testrsps"                # a series of auto-generated files linked to from summary.html
dloginputdname = "testinputs"              # also auto generated input samples linked to from summary.html

dainfofname  = dtestdirname + "/data/attack_info.json"   # where to find attack info

dresultdir = os.path.join(os.getcwd(),"results")                     # folder to save CVDAST/CVIAST test results, used for report gen
dperadir   = "perattack"                   # save perattack results
dperapidir = "perapi"                      # save perapi test results, currently not used by test wrapper

savefailedtestreport   = True              # save a copy of the failed tests that can be compared using reportcomp later
usecustomreportfname   = True              # custom report name to use, by default a file failedtest.json is generated
customsavedreportfanme = "failedtest.json" # specify the custom report name
ddiffrlogrspdirname = "testdiffrsps"       # when running reportcomp, just like testrsps, we use this dir to save resp file

dcsvreportfname = "fordev-sum"             # a csv file generated that can be used to show developers the findings, timestamp will be attached by default
dhtmlreportfname = "summary"               # name of the html file, timestamp will be attached
attachtimestamptoreport = True             # control whether to attach time stamp


#
# Test specific tuning control
#  tweeking these variables will 
#
genspeclistpyfname = os.path.join(os.path.dirname(os.path.realpath(__file__)),"apispecs.py")         # this is a simply .py file, fuzzallspecs.py will generate the spec list. 


#usecustomlist = input("Want to Specify Custom Spec List? (y/n): ")
usecustomlist = False
'''                      # one can set this to True and then config the list below to control what spec to test or re
if str(usecustomlist).lower() == 'y':
    usecustomlist = True
    apispeclist=input("Specify Spec List (Example: spec1,spec2: ").split(",")           #["ob", "newob"]
else:
    usecustomlist = False
    apispeclist = []

'''
apispeclist = []
dperattackvalueused="1"                    # when running test, the number of patterns picked from each attack, set to 1 to avoid huge number of tests
#
# default list containing all attacks. runall.py will run
#  each one by one and log results.
#
# can adjust this list to control test run and/or report to generate. 
#
#fuzzattacklist = input("Fuzz Attack List (Example: attack_type1, attack_type2): ").split(",")      # 
fuzzattacklist = ["control-chars"]

'''

fuzzattacklist = ['control-chars', 'string-expansion', 'server-side-include',
                  'xpath', 'unicode', 'html_js_fuzz', 'disclosure-directory',
                  'xss', 'os-cmd-execution', 'disclosure-source',
                  'format-strings', 'xml', 'integer-overflow',
                  'path-traversal', 'json', 'mimetypes', 'redirect',
                  'os-dir-indexing', 'no-sql-injection', 'authentication',
                  'http-protocol', 'business-logic',
                  'disclosure-localpaths/unix',
                  'file-upload/malicious-images',
                  'sql-injection/detect',
                  'sql-injection/exploit',
                  'sql-injection/payloads-sql-blind']
'''

import sys, os
import yaml
thismodule = sys.modules[__name__]
config = input("\n\tEnter the path to config file:")
if not config:
    print("Config is mandatory!")
    raise SystemExit
if not os.path.exists(config):
    print("Please check the path to Config!!")
    raise SystemExit
with open(config) as fobj:
    ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
for k,v in ce_details.get("execution_info").items():
    if type(v) is str and "," in v:
        setattr(thismodule, k, v.split(","))
    else:
        setattr(thismodule, k, v)

