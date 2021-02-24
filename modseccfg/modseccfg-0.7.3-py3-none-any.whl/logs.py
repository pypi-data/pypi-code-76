# api: modseccfg
# encoding: utf-8
# type: file
# category: log
# title: log reader
# description: scanning of error.logs / audit log
# config:
#    { name: log_entries, type: int, value: 5000, description: "How many log entries to show (whole log will be counted regardless)", help: "modseccfg will read the whole log file given, but trim it down for display in the log listbox (performance/memory use)" }
#    { name: log_filter, type: str, value: "(?!404|429)4\d\d|5\d\d", description: "Error codes to look out for in access.logs" }
#    { name: log_skip_rx, type: str, value: "PetalBot|/.well-known/ignore.cgi", description: "Regex to skip whole log lines on" }
#    { name: log_search_id, type: bool, value: 0, description: "Look up rule id, if only file+line given in log (slow)", help: "Chained rules will not be identified in logs, other than by file: and line:. Enabling id: lookup is reasonably fast." }
#    { name: log_max_days,  type: int,  value: 3, description: "Number of days to read from audit/*/*/*/* log directory" }
#    { name: log_strip_json, type:bool, value: 0, description: "Strip JSON blob from audit.logs after conversion", help: "JSON logs are easier to process than the native format, but retaining the full details in the log list will deplete memory and slow down scrolling" }
#    { hidden: 1, name: log_extra, type: str, value: "test/logs/*.log", description: "Additional log files (testing)" }
#    { name: logview_colorize, type: bool, value: 1, description: "Colorize log view", help: "Highlights a few snippets (url, status, msg, data) in the multiline box below the log list" }
# version: 0.5
# license: Apache-2.0
#
# Basic filtering and searching within the logs.
# Filters out by error codes (http 4xx/5xx) or mod_security messages.
# And looks up [id "123456"] strings from entries to generate the
# "Count" column.
#
# Audit log types (serial/concurrent/json) are also supported now,
# but don't necessarily provide more details.
# modseccfg shows AuditDir paths as .../audit/*/*/*/* - and reads
# them via find/cat (perhaps over ssh for remoting). Reading can
# be slow, if binary data (Native log format) is contained there.
#


import os, re, glob
from modseccfg import utils, vhosts, data
from modseccfg.utils import srvroot, conf


# detected rule ids and number of occurences
log_count = {}     # id→count
class state:
    log_curr = ""  # fn
    prev = []      # injected from main to keep unfiltered listbox values


# extraction rules
class rx:
    interesting = re.compile("""
        ModSecurity: |
        \[id\s"\d+"\] |
        "\s((?!429)[45]\d\d)\s\d+        # should come from conf[log_filter]
    """, re.X)
    id = re.compile("""
        (?: \[id\s | \{"id":\s* )  "(\d+)"  [\]\}]   # [id "…"] or json {"id":"…"}
    """, re.X)
    file_line = re.compile("""
        \[file \s
          "(?!apache2_util\.c)(?P<file>.+?)"
        \] \s*
        \[line \s "(?P<line>\d+)"\]
    """, re.X)
    shorten = re.compile("""
        :\d\d.\d+(?=\]) |
        \s\[pid\s\d[^\]]*\] |
        \s\[tag\s"[\w\-\.\/]+"\] |
        \s\[client\s[\d\.:]+\] |
        \sRule\s[0-9a-f]{12} |
        (?<=\[file\s")/usr/share/modsecurity-crs/rules/ |
    """, re.X)
    non_bmp = re.compile(u'[\U00010000-\U0010FFFF]')
    audit = dict(
        section = "^--\w+-([A-Z])--",                # only looking for -A-- and -Z--
        A = "^\[[^\]]+\]\s(\w+)\s+([\d.:]+)\s+(\d+)",   # ignore bollocks datetime format
        request_uri = "^\w+\s(\S+)\sHTTP/",          # just url path
        status = "^HTTP/\d\.\d (\d+)",               # from headers
        user_agent = "^User-Agent:\s*(.+)$",         # U-A
        content_type = "^Content-Type:\s*(\S+)",     # C-T
        msg = "^Apache-Error:\s*(.+)$",              # Warning:...
        id = "id:(\d+)",                             # from SecRule matches
        #secaction = "^SecAction\s*(\S+)",           # first line
        json = "^\{[\{\"]"
    )
    audit_json = re.compile("""
       "(request_line|id|phase|status|Host  #|transaction_id|remote_addr|User-Agent
       )" :
         \s*   (?:"(?=.*?")|(?=\d+,)) (.*?) [",]
    """, re.X|re.I)
    json_request_uri = re.compile(
       """^\w+\s(\S+)"""
    )
rx.audit_all = re.compile("|".join(rx.audit), re.I|re.M)


# search through log file, filter, extract rule ids, return list of log lines
def scan_log(fn="", pipe=None, force=0):

    #print(f"scan_log(fn='{fn}')")
    if fn == state.log_curr and not force:
        return   # no update // notably this will prevent File > Rescan Logs
    state.log_curr = ""
    state.prev = []
    # type
    is_glob = re.search("\*(/?\*)+", fn)
    is_audit = is_glob or re.search("audit", fn)
    if not srvroot.exists(fn) and not is_glob:
        return
    state.log_curr = fn
    log_count = {}
    
    
    # handle
    if pipe:
        pass
    elif is_glob:
        pipe = open_glob(fn)
    elif fn:
        pipe = open(srvroot.fn(fn), "rb")#, mostly_encoding="utf8"
    #print(fn, pipe)
    
    # filter lines
    log_lines = []
    for line in pipe:
        try: # skip binary (from native audit.log)
            line = rx.non_bmp.sub("", line.decode("utf-8"))
        except:
            continue
        # audit/* log
        if is_audit:
            line = audit.collect(line)
            if line:
                log_lines.append(line)
        # access/error.log
        elif rx.interesting.search(line) or force:
            if re.search(conf.log_skip_rx, line):
                continue
            m = rx.id.findall(line)
            if m:
                for i in m:
                    incr_log_count(int(i))
            elif conf.log_search_id:
                m = rx.file_line.search(line)
                if m:
                    id = search_id(m.group("file"), m.group("line"))
                    if id:
                        incr_log_count(int(id))
            log_lines.append(line.strip())
        # slice entries during scan (easy memory depletion for audit.log)
        if len(log_lines) >= conf.log_entries:
            log_lines = log_lines[-conf.log_entries:]
    pipe.close()

    # shorten infos in line
    log_lines = [rx.shorten.sub("", line) for line in log_lines]
    return log_lines
    

# pipe log/audit/*/*/*/* specifier through find+cat
def open_glob(fn):
    fn = re.sub("(/?\*){2,}$", "", fn)
    return srvroot.popen(
        cmd=[
            "find", fn, "-type", "f",     # =find all files in dir tree
            "-readable", "-mtime", "-3",  # should reintroduce conf option
            "-execdir", 'cat', '{}', '+'  # compatibility: -execdir and `+` might be GNU-only
        ], action="r"
    )

# line-wise traversal of serial/concurrent audit.log in native format
class audit:
    collector = {}

    @staticmethod
    def collect(line):
        if line.startswith("{"):
            return audit.json(line)  
        elif rx.audit_all.search(line):
            for id,line_rx in rx.audit.items():
                val = re.findall(line_rx, line, re.I|re.M)
                if not val:
                    continue
                #print(id,val)
                #-- delimiter
                if id=="section":
                    # assemble collected values into log line
                    if val==["A"] or val==["Z"]:
                        if audit.collector:
                            line = audit.as_str()
                            audit.collector = {}
                            if line:
                                return line
                        return
                #-- value:
                elif id=="A":
                    audit.collector = {}
                    audit.collector["uniq_id"] = val[0][0]
                    audit.collector["remote_addr"] = val[0][1]
                elif val:
                    if not audit.collector.get(id):
                        audit.collector[id] = []
                    audit.collector[id] += val
        return None

    # convert dict into log line
    @staticmethod
    def as_str():
        if not audit.collector.get("request_uri"):   # or not audit.collector.get("id"):
            return
        line = []
        keys = ["request_uri", "remote_addr", "user_agent", "msg"] # sort fields first
        [keys.append(k) for k in audit.collector.keys() if not k in keys]
        for k in keys:
            v = audit.collector.get(k)
            if not v:
                continue
            for v in (v if type(v) is list else [v]):
                line.append('[' + k + ' "' + str(v) + '"]')
        line = " ".join(line)
        #print(line)
        return line
        

    # line-wise JSON traversal
    @staticmethod
    def json(line):
        kv = rx.audit_json.findall(line)
        if kv and kv[0][0] == "request_line":
            path = rx.json_request_uri.findall(kv[0][1])[0]
            kv.append( ("request_uri", path,) )
        log = " ".join([f'[{k} "{v}"]' for k,v in kv])
        if not conf.log_strip_json:
            log += ", JSON==" + line
        return log


# increase count for a rule id
def incr_log_count(id):
    if id in log_count:
        log_count[id] += 1
    else:
        log_count[id] = 1

# search [id …] from only [file …] and [line …] - using vhosts.linemap{}
def search_id(file, line):
    utils.log.debug("linemap:", file, line)
    if file and line:
        vh = vhosts.vhosts.get(file)
        if vh:
            return vh.line_to_id(int(line))
    return 0


# assemble list of error/access/audit logs
def find_logs():
    log_list = []
    for fn,vh in vhosts.vhosts.items():
        log_list = log_list + vh.logs
        if vh.cfg.get("secauditlog"):
            if re.match("concurrent", vh.cfg["secauditlogtype"], re.I) and vh.cfg.get("secauditlogstoragedir"):
                log_list.append(vh.cfg["secauditlogstoragedir"]+"/*/*/*/*")
            else:
                log_list.append(vh.cfg["secauditlog"])
             #+ record format (json)? or rely on pattern whilst reading?
             #vh.cfg["secauditlogformat"]
    if conf.get("add_stub_logs"):
        add = [data.dir+"/common_false_positives.log"]
        add += glob.glob(conf.log_extra)
    else:
        add = []
    #log_list.append("./fossil.error.log")  # we might allow a config text field for extra log files?
    return list(set(log_list)) + add


# UI: transform log text into sg.Multiline print() calls
def colorize (w, line):
    w.update(value="")
    styles = {
        "request_uri": dict(background_color="yellow"),
        "request_url": dict(background_color="yellow"),
        "uri": dict(background_color="yellow"),
        "path": dict(background_color="yellow"),
        "status": dict(background_color="orange"),
        "id": dict(background_color="magenta"),
        "msg": dict(text_color="blue"),
        "data": dict(text_color="darkred"),
    }
    rx = "|".join(styles.keys())
    rx = re.compile(f"""
        ([^\[]*.*?)                 # normal text
        (?:                # optional:
           (?<=\[)                  # exclude [ from keyword → yields a bit of backtracking
           (  (?:{rx})  \s"?  )     # keywords + "
           ( .+? )                  # text between [kw" … "]
           (?="?\])                 # "]
        )?""",
        re.X
    )
    for normal, keyword, content in re.findall(rx, line):
        w.print(normal + keyword, end="")
        if keyword:
            keyword = keyword.strip(' "')
            w.print(content, **styles[keyword], end="")
    