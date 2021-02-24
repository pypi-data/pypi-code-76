# api: modseccfg
# title: craft *.log.fmt
# description: record current log formats
# type: internal
# category: update
# version: 0.2
#
# Create a *.fmt descriptor for each Apache *.log
# This should be used on remote systems. Whereas
# local setups ought to use `update-logfmt`.
#


import re, json
from modseccfg import vhosts, writer
import logfmt1
from modseccfg.vhosts import tmp
from modseccfg.utils import conf, log, srvroot


print("# Create prepared *.log.fmt descriptors\n")


# traverse log files, create .fmt descriptor with current format string
for fn,ty in tmp.log_map.items():

    fn_fmt = f"{fn}.fmt"
    fmt_record = tmp.log_formats.get(ty)
    if not fmt_record:
        continue
    
    j = {}
    if srvroot.exists(fn_fmt):
        try:
            j = json.loads(srvroot.read(fn_fmt))
        except Exception as e:
            j = {}
            print(f"WARN: {fn_fmt} contained invalid json: {str(e)}")
    if not "class" in j:
        j["class"] = f"apache {ty}"
    if not "record" in j or j["record"] != fmt_record:
        j["record"] = fmt_record
        
    # add descriptors for known placeholders
    if not "fields" in j or True:
        j["regex"] = logfmt1.regex(j)

    print(f"→ {fn_fmt}")
    try:
        f = open(fn_fmt, "w")
        f.write(json.dumps(j, indent=4))
        f.close()
    except Exception as e:
        print("ERR: " + str(e))

