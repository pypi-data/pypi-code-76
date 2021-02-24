# api: modseccfg
# encoding: utf-8
# title: *.conf scanner
# description: Compiles a list of relevant apache/vhost files and Sec* settings
# type: tokenizer
# category: apache
# version: 0.7
# config:
#    { name: envvars, value: "/etc/default/apache2", type: str, description: "Look up APACHE_ENV vars from shell script", help: "Mostly applies to Debian derivates. Other distros usually embed SetEnv directives for log paths." }
# license: Apache-2.0
#
# Runs once to scan for an vhost* and mod_security config files.
# Uses `apache2ctl -t -D DUMP_INCLUDES` to find all includes,
# and regexes for Sec*Rules or *Log locations and ServerNames.
#
# This should yield any mod_security and vhost-relevant sections.
# The list is kept in `vhosts`. And secrule declarations+options
# in `rules`.
#
# Extraction is fairly simplistic, but for this purpose we don't
# need an exact representation nor nested structures. The UI will
# present vhost/conf files rather than <VirtualHost> sections.
# (We shouldn't penalize the average user for random edge cases.)
# 
# Notably this will not work with mod_security v3, since the
# SecRules/Flags have been moved into matryoshka directives and
# external *.conf files (but no JSON rulesets for some reason).
# Still doable, but not a priority right now. Same for nginx.
#


import os, re, sys, random
import subprocess
import traceback
from pprint import pprint
from modseccfg.utils import srvroot, log


# collected config/vhost sections
vhosts = {
    # fn → vhost:
           # .fn .t .name .logs[] .cfg{} .rulestate{} .ruledecl{} .update{} .linemap{}
}
# and SecRules (we don't actually use all extracted details)
rules = {
    # id → secrule:
           #  .id .chained_to .msg .flags{} .params{} .tags[] .tag_primary .ctl{} .setvar{} .vars .pattern
}


# extraction patterns
class rx:
    # a conf file '(*) /etc/apache2/main.conf'
    dump_includes = re.compile("^\s*\([\d*]+\)\s+(.+)$", re.M)
    # directives we care about (to detect relevant .conf files)
    interesting = re.compile("""
        ^ \s*
         (\#\s*)?                                                                   # possibly commented out
         ( (Error|Custom|Global|Forensic|Transfer)Log (Error)?LogFormat |           # log directivess
          Server(Name|Alias) | (Virtual)?DocumentRoot |                             # vhost directives
          Sec\w* | Use\sSec\w+ | modsecurity\w* | Include\w* ) \\b                  # mod_sec directives
        | ^\#\s*type:\s*config\s*$                                                  # or PMD header
        """,
        re.M|re.I|re.X
    )
    # count <VirtualHost>s
    count_virtualhost = re.compile("""
        ^ \s*(<VirtualHost)\\b
    """, re.X|re.M|re.I)
    # extract directive line including line continuations (<\><NL>)
    configline = re.compile(
        """ ^
        [\ \\t]*                          # whitespace \h*
        # (?:Use \s{1,4})?                # optional: `Use␣` to find custom macros like `Use SecRuleRemoveByPath…`
        (
          \w+ |                           # alphanumeric directive 
          </?(?:File|Loc|Dir|If\\b)\w*    # or <Wrap> section
        )\\b
          [\ \\t]*                        # whitespace \h+
        (
          (?: [^\\n\\\\]+ | [\\\\]. )*    # literals, or backslash + anything
        )
        (?: $ | >.*$ )                    # account for line end or closing >
        """,
        re.M|re.S|re.X
    )
    # to strip <\><NL>
    escnewline = re.compile(
        """[\\\\][\\n]\s*"""              # escaped linkebreaks
    )
    # handle quoted/unquoted directive arguments (not entirely sure if Apache does \" escaped quotes within)
    split_args = re.compile(
        """
        (?:\s+)   |                       # skip whitespace (\K not supported in python re, so removing empty matches in postprocessing)
        \#.*$  |                          # skip trailing comment (which isn't technically allowed, but)
        " ((?:[^\\\\"]+|\\\\ .)+) "  |    # quoted arguments
        (?!\#) ([^"\s]+)                  # plain arguments (no quotes, no spaces)
        """,
        re.X
    )
    # SecRule … … `actions:argument,…`
    actions = re.compile(
        """
        (?: (t|pfx) :)? (\w+)             # action
        (?:
            :                             # : value…
            ([^,']+)     |                # bareword
            :
            ' ([^']+) '                   # ' quoted '
        )?
        """,
        re.X
    )
    # line number scan: roughly look for id:123456 occurences
    id_num = re.compile(
        "id:(\d+)"                        # without context
    )
    # comment lookup, directly preceeding id, uncompiled 
    rule_comment = """
        ( (?:^\#.*\\n)+ )                 # consecutive comment lines
        (?: ^[^\#]+\\n)*                  # filler lines
        .*?  id:{}                        # id:nnnnn, requires rx.format(id)
    """
    # envvars
    shell_vars = re.compile("""
        ^\s* (?:export\s+)?  ([A-Z_]+)  =  ["']?  ([\w/\-.]+)  ["']?
    """, re.M|re.X)
    # secrule actions
    ctl_restricts = re.compile("""
        ruleRemoveById | ruleRemoveByTag
    """, re.X|re.I)
    

# temporary state variables
class tmp:
    last_rule_id = 0

    decl_preconf = False

    tag_prio = ['event-correlation', 'anomaly-evaluation', 'OWASP_CRS/LEAKAGE/ERRORS_IIS', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_PHP', 'OWASP_CRS/LEAKAGE/ERRORS_PHP', 'OWASP_CRS/LEAKAGE/ERRORS_JAVA', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_JAVA', 'platform-sybase', 'platform-sqlite', 'platform-pgsql', 'platform-mysql', 'platform-mssql', 'platform-maxdb', 'platform-interbase', 'platform-ingres', 'platform-informix', 'platform-hsqldb', 'platform-frontbase', 'platform-firebird', 'platform-emc',
    'platform-db2', 'platform-oracle', 'CWE-209', 'OWASP_CRS/LEAKAGE/ERRORS_SQL', 'platform-msaccess', 'OWASP_CRS/LEAKAGE/SOURCE_CODE_CGI', 'PCI/6.5.6', 'WASCTC/WASC-13', 'OWASP_CRS/LEAKAGE/INFO_DIRECTORY_LISTING', 'attack-disclosure', 'OWASP_CRS/WEB_ATTACK/JAVA_INJECTION', 'language-java', 'CAPEC-61', 'WASCTC/WASC-37', 'OWASP_CRS/WEB_ATTACK/SESSION_FIXATION', 'attack-fixation', 'OWASP_AppSensor/CIE1', 'WASCTC/WASC-19', 'OWASP_CRS/WEB_ATTACK/SQL_INJECTION', 'attack-sqli',
    'PCI/6.5.1', 'OWASP_TOP_10/A2', 'CAPEC-63', 'platform-internet-explorer', 'platform-tomcat', 'CAPEC-242', 'OWASP_AppSensor/IE1', 'OWASP_TOP_10/A3', 'WASCTC/WASC-22', 'WASCTC/WASC-8', 'OWASP_CRS/WEB_ATTACK/XSS', 'attack-xss', 'OWASP_CRS/WEB_ATTACK/NODEJS_INJECTION', 'attack-injection-nodejs', 'language-javascript', 'OWASP_CRS/WEB_ATTACK/PHP_INJECTION', 'attack-injection-php', 'language-php', 'language-powershell', 'PCI/6.5.2', 'WASCTC/WASC-31',
    'OWASP_CRS/WEB_ATTACK/COMMAND_INJECTION', 'attack-rce', 'platform-unix', 'language-shell', 'OWASP_CRS/WEB_ATTACK/RFI', 'attack-rfi', 'PCI/6.5.4', 'OWASP_TOP_10/A4', 'WASCTC/WASC-33', 'OWASP_CRS/WEB_ATTACK/FILE_INJECTION', 'OWASP_CRS/WEB_ATTACK/DIR_TRAVERSAL', 'attack-lfi', 'OWASP_CRS/WEB_ATTACK/HTTP_PARAMETER_POLLUTION', 'CAPEC-460', 'OWASP_CRS/WEB_ATTACK/HEADER_INJECTION', 'OWASP_CRS/WEB_ATTACK/RESPONSE_SPLITTING', 'OWASP_CRS/WEB_ATTACK/REQUEST_SMUGGLING',
    'paranoia-level/4', 'language-aspnet', 'paranoia-level/3', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_UA', 'OWASP_CRS/POLICY/HEADER_RESTRICTED', 'OWASP_CRS/POLICY/EXT_RESTRICTED', 'OWASP_CRS/POLICY/PROTOCOL_NOT_ALLOWED', 'OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE_CHARSET', 'OWASP_CRS/POLICY/CONTENT_TYPE_NOT_ALLOWED', 'OWASP_AppSensor/EE2', 'OWASP_TOP_10/A1', 'WASCTC/WASC-20', 'OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE', 'OWASP_CRS/POLICY/SIZE_LIMIT',
    'OWASP_CRS/PROTOCOL_VIOLATION/IP_HOST', 'OWASP_CRS/PROTOCOL_VIOLATION/EMPTY_HEADER_UA', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_ACCEPT', 'OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_HOST', 'platform-windows', 'platform-iis', 'OWASP_CRS/PROTOCOL_VIOLATION/EVASION', 'OWASP_CRS/PROTOCOL_VIOLATION/INVALID_HREQ', 'CAPEC-272', 'OWASP_CRS/PROTOCOL_VIOLATION/INVALID_REQ', 'attack-protocol', 'OWASP_CRS/AUTOMATION/CRAWLER', 'attack-reputation-crawler',
    'OWASP_CRS/AUTOMATION/SCRIPTING', 'attack-reputation-scripting', 'PCI/6.5.10', 'OWASP_TOP_10/A7', 'WASCTC/WASC-21', 'OWASP_CRS/AUTOMATION/SECURITY_SCANNER', 'attack-reputation-scanner', 'paranoia-level/2', 'attack-dos', 'PCI/12.1', 'OWASP_AppSensor/RE1', 'OWASP_TOP_10/A6', 'WASCTC/WASC-15', 'OWASP_CRS/POLICY/METHOD_NOT_ALLOWED', 'OWASP_CRS', 'IP_REPUTATION/MALICIOUS_CLIENT', 'attack-reputation-ip', 'platform-multi', 'attack-generic', 'platform-apache', 'language-multi',
    'application-multi', 'paranoia-level/1']

    env = {
        "APACHE_LOG_DIR": "/var/log/apache2"  #/var/log/httpd/
    }
    env_locations = [
        "/etc/apache2/envvars", "/etc/default/httpd"
    ]
    
    log_formats = {
        "error": "[%t] [%l] [pid %P] %F: %E: [client %a] %M",
        #"default": "%h %l %u %t "%r" %>s %b",
        "common": '%h %l %u %t "%r" %>s %O',
        "forensic": '+%{forensic-id}n|%r|Host:%H|%{UA}|%{H*}\n-%{forensic-id}n',
        #%t == [%02d/%s/%d:%02d:%02d:%02d %c%.2d%.2d]
    }
    log_map = {
        #"../fn.log": "combined"
    }


# encapsulate properties of config file (either vhosts, SecCfg*, or secrule collections)
class Vhost:
    """
        Represents a config/vhost or mod_security rules file.
        
        Parameters
        ----------
        fn : str
            *.conf filename
        src : str
            config file source
        
        Attributes
        ----------
        fn : str
                filename
        t : str
                *.conf type (one of 'rules', 'vhost', 'cfg')
        name : str
                ServerName
        logs : list
                List of error/access.log filenames
        cfg : dict
                SecOption directives
        rulestate : dict
                SecRuleRemove* states (id→0), usually set for .t='vhost'
        ruledecl : dict
                Map contained SecRules id into vhosts.rules{}, set within .t='rules'
        update : dict
                Map of SecRuleUpdate…By…  { id→{vars:[],action:[]} }
        linemap : dict
                Line number → RuleID (for looking up chained rules in error.log)
        warn : str
                Textual notice on conf file, e.g. "more than VirtualHost defined"
    """

    # split *.conf directives, dispatch onto assignment/extract methods
    def __init__(self, fn, src, cfg_only=False):

        # vhost properties
        self.fn = fn
        self.t = "cfg"
        self.name = ""
        self.logs = []
        self.cfg = {}
        self.rulestate = {}    # 🗶=disabled, ⋇=modified, ⋚=wrapped, 🗸=enabled
        self.ruledecl = {}
        self.update = {}       # SecRuleUpdate… map
        self.warn = ""

        # internal state
        self.linemap = {}      # lineno → first id: occurence
        self.mk_linemap(src)   # fill .linemap{}
        self.wrap = []         # history of <Wrap>

        # actual extraction
        self.extract(src, cfg_only=cfg_only)
        self.classify_cfg(src)    
        log.debug(self.cfg)

    # extract directive lines
    def extract(self, src, cfg_only=False):
        for dir,args  in rx.configline.findall(src):    # or .finditer()? to record positions right away?
            dir = dir.lower()
            #log.debug(dir, args)
            if hasattr(self, dir):
                if cfg_only: #→ if run from SecOptions dialog, we don't actually want rules collected
                    continue
                func = getattr(self, dir)
                func(self.split_args(args))
            # .cfg option
            elif dir.startswith("sec") or dir in ["documentroot", "modsecurity"]:
                if not dir in self.cfg:
                    self.cfg[dir] = args
                    #log.debug(self.cfg)
                else:
                    log.debug(f"Duplicate directive '{dir}' found")
            # .wrap state
            elif dir.startswith("</"):
                if self.wrap:
                    self.wrap.pop(0)
                else:
                    log.warn("ERROR IN CONFIG STRUCTURE(?): tried to pop a </Wrap> directive without being within a section")
            elif dir.startswith("<"):
               self.wrap.insert(0, dir[1:])

    # determine config file type
    def classify_cfg(self, src):
        if self.name:
            self.t = "vhost"
        elif len(self.rulestate) >= 3 or re.search("RE\w+-\d+-EXCLUSION", self.fn):
            self.t = "cfg"
        elif len(self.ruledecl) >= 3:
            self.t = "rules"
        #log.debug(self.fn,self.t)
        # notice
        num = len(rx.count_virtualhost.findall(src))
        if num == 2:
            self.warn = "Two <VirtualHost>s defined. Only first will be updated by modseccfg."
        elif num > 2:
            self.warn = "Unreasonable number of <VirtualHost> entries in conf. It probably shouldn't be edited through modseccfg."
        elif not os.access(self.fn, os.W_OK):
            self.warn = "Config file isn't writable. Don't even try."

    # strip \\ \n line continuations, split all "args"
    def split_args(self, args):
        args = re.sub(rx.escnewline, " ", args)
        args = rx.split_args.findall(args)
        args = [s[1] or s[0] for s in args]
        args = [s for s in args if len(s)]
        #args = [s.decode("unicode_escape") for s in args]   # don't strip backslashes
        return args
    # apply ${ENV} vars
    def var_sub(self, s):
        return re.sub('\$\{(\w+)\}', lambda m: tmp.env.get(m.group(1), ""), s)

    # apache: log directives
    def customlog(self, args):
        fn, ty = self.var_sub(args[0]), args[1]
        self.logs.append(fn)
        if ty.find("%") >= 0:  # turn literal placeholder format into temporary name
            ty, fmt = hex(hash(ty))[4:], ty
            self.logformat(ty, fmt)
        tmp.log_map[fn] = ty
    def errorlog(self, args):
        self.customlog([args[0], "error"])
    def forensiclog(self, args):
        self.customlog([args[0], "forensic"])
    def globallog(self, args):
        self.customlog([args[0], args[1] or "combined"])
    def transferlog(self, args):
        self.customlog([args[0], "transfer"])
    def logformat(self, args):
        if len(args) == 1: args[1] = "transfer"
        tmp.log_formats[args[1]] = args[0].replace('\\"', '"')
    def errorlogformat(self, args):
        self.logformat([args[0], "error"])
    def servername(self, args):
        if not self.name:
            self.name = args[0]

    # modsec: create a rule{}
    def secrule(self, args):
        last_id = int(tmp.last_rule_id)
        r = SecRule(args)
        if r.id:
            tmp.last_rule_id = r.id
        # add a float id (+0.1) to chained rules (no idea how virtual `7f9aa85dec58` rule ids are generated, lackluster docs / no mailing list / no IRC response)
        elif rules.get(last_id) and "chain" in rules[last_id].flags:
            tmp.last_rule_id = round(tmp.last_rule_id + 0.1, 1)
            r.id = tmp.last_rule_id
            r.chained_to = int(last_id) # primary parent
        rules[r.id] = self.ruledecl[r.id] = r
        if self.wrap: # now, rule declarations shouldn't be conditional, and we're not really gonna use this; just record it
            rules[r.id].wrap = True #self.wrap[0]
        #log.debug(r.__dict__)

    # modsec: just a secrule without conditions
    def secaction(self, args):
        self.secrule(["@SecAction", "setvar:", args[0]])
    
    # modsec: SecRuleRemoveById 900001 900002 900003
    def secruleremovebyid(self, args):
        state = "🗶"
        if self.wrap:  # record if within <Dir|File|If|Wrap> section
            state = "⋚"
            #log.info("wrapped SecRuleRm", self.fn, self.wrap, args)
        for a in args:
            if re.match("^\d+-\d+$", a):   # are ranges still allowed?
                a = [int(x) for x in a.split("-")]
                for i in range(*a):
                    if i in rules:    # only apply state for known/existing rules, not the whole range()
                        self.rulestate[i] = state
            elif re.match("^\d+$", a):
                self.rulestate[int(a)] = state
            else:
                self.rulestate[a] = state  # from tag

    # modsec: SecRuleRemoveByTag sqli app-name
    def secruleremovebytag(self, args):
        self.secruleremovebyid(args)

    # modsec: SecRuleUpdateTargetById, SecRuleUpdateActionById
    #
    # Won't get applied onto existing/global rules, but kept as unprocessed .update{} on
    # local vhost.confs.
    # While modify.SecRuleUpdated uses these updates to present current rule parameters.
    # The mainwindow just relies on the rulestate icons.
    def secruleupdatetargetbyid(self, args):
        self._secruleupdate("vars", *args)
    def secruleupdateactionbyid(self, args):
        self._secruleupdate("actions", *args)
    def _secruleupdate(self, cls, id, arg, *repl):
        if re.match("^\d+:\d$", id):
            id = float(id.replace(":", "."))
        elif re.match("^\d+$", id):
            id = int(id)
        else:
            return
        self.rulestate[id] = "⋇"
        # We don't really use the detail. This is just to record that any one rule has been "modified".
        if repl:
            arg = f"!{repl[0]},{arg}"  # merge third parameter from `SecRuleUpdateTarget 123456 NEW_TARGET REMOVE_VAR`
        if not self.update.get(id):
            self.update[id] = {"vars":[], "actions":[]}
        self.update[id][cls].append(arg)
        

    # modssec: irrelevant (not caring about skipAfter rules)
    def secmarker(self, args):
        pass

    # v3-connector: Include
    def modsecurity_rules_file(self, args):
        raise Exception("modsecurity v3 connector rules not supported (module doesn't provide disclosure of custom includes via `apache2ctl -t -D DUMP_INCLUDES` yet)")
        #fn = self.var_sub(args[0]); vhosts[fn] = Vhost(fn, srvroot.read(fn))
    # v3-connector: Inline (the quoting nightmare)
    def modsecurity_rules(self, args):
        raise Exception("modsecurity v3 connector rules not supported")
        #self.extract(args[0])
    
    # apache: define ENV var
    def define(self, args):
        tmp.env[args[0]] = args[1]
    
    # apache: Include
    def includeoptional(self, args):
        if args and re.search("\*\.preconf$", args[0]):
            tmp.decl_preconf = True

    # map rule ids to line numbers
    def mk_linemap(self, src):
        for i,line in enumerate(src.split("\n")):
            id = rx.id_num.search(line)
            if id:
                self.linemap[i] = int(id.group(1))
    # find closest match
    def line_to_id(self, lineno):
        if not lineno in self.linemap:
            lines = [i for i in sorted(self.linemap.keys()) if i <= lineno]
            if lines and lines[-1] in self.linemap:
                self.linemap[lineno] = self.linemap.get(lines[-1])
        return self.linemap.get(lineno, 0)


# break up SecRule definition into parameters, attributes (id,msg,tags,meta,actions etc.)
class SecRule:
    """
        SecRule properties
        
        Parameters
        ----------
        args : list
               Three directive parameters (as in 'SecRule […] […] […]')
        
        Attributes
        ----------
        id : int
                Rule ID
        chained_to : int
                Parent rule ID for flags=[chain] rules
        msg : str
                Message
        flags : list
                Any of block, deny, t:none, ... rule actions
        params : dict
                Any action:value from rule actions, e.g. logdata:..
        tags : list
                Any tag:name from actions
        tag_primary : str
                Most unique of the tags
        ctl : dict
                Any ctl:action=value from rule actions
        setvar : dict
                Any servar:name=val from rule actions
        vars : str
                e.g. ARGS|PARAMS or &TX.VAR
        pattern : str
                e.g. '@rx ^.*$'
        msg_stub : bool
                faux .msg if True
        hidden : bool
                Mark pure control rules / SecActions
        wrap : bool
                Mark if option occured in <If|Match|Etc> section
    """
    
    def __init__(self, args):
        # secrule properties
        self.id = 0
        self.chained_to = 0
        self.msg = ""
        self.flags = []
        self.params = {}
        self.tags = []
        self.tag_primary = ""
        self.ctl = {}
        self.setvar = {}
        self.vars = "REQ*"
        self.pattern = "@rx ..."
        self.hidden = False
        self.wrap = False
        # args must contain 3 bits for a relevant SecRule
        if len(args) == 2:
            args.append("") # empty actions (which a couple of chained rules do)
        elif len(args) != 3:
            log.warn("UNEXPECTED NUMBER OF ARGS:", args)
            return
        self.vars, self.pattern, actions = args
        #log.debug(args)
        # split up actions,attributes:…
        for pfx, action, value, qvalue in rx.actions.findall(actions):
            #log.debug(pfx,action,value,qvalue)
            self.assign(pfx, action, value or qvalue)
        # most specific tag
        for p in tmp.tag_prio:
            if p in self.tags:
                self.tag_primary = p
                break
        # if SecAction (uncoditional rule, mostly setvars:)
        if self.vars == "@SecAction" and not self.msg:
            self.msg = f"@SecAction {self.setvar or self.params}" #.format(str(self.setvar) if self.setvar else str(self.params))
            self.msg_stub = True
        # alternative .msg
        if not self.msg:
            self.msg = self.params.get("logdata") or f"{self.vars}   {self.pattern}" #.format(self.vars, self.pattern)
            self.msg_stub = True
        # .hidden (flow control rules)
        self.hidden = self.pattern == "@eq 0" or self.vars == "TX:EXECUTING_PARANOIA_LEVEL"


    # distribute actions/attributes into properties here
    def assign(self, pfx, action, value):
        if action == "id":
            if re.match("^\d+$", str(value)):
                self.id = int(value)
            elif value == "%{ENV:NEWID}":
                self.id = random.randrange(50000, 59999) + 0.1
            else:
                self.id = random.randrange(60000, 79999) + 0.2
        elif action == "msg":
            self.msg = value
            self.msg_stub = False
        elif action == "tag":
            self.tags.append(value)
        elif action == "ctl":
            if value.find("=") > 0:
                action, value = value.split("=", 1)
            if rx.ctl_restricts.match(action):
                pass # self.restricts[] =
            self.ctl[action] = value or 1
        elif action == "setvar":
            if value.find("=") > 0:
                action, value = value.split("=", 1)
            self.setvar[action] = value
        elif pfx == "t" and not value:
            self.flags.append(pfx+":"+action)
        elif action and not pfx:
            if value:
                self.params[action] = value
            else:
                self.flags.append(action)
        else:
            log.warn("unknown action", [pfx, action, value])
    
    # find vhost it was declared in
    def vhost(self):
        for vh in vhosts.values():
            if self.id in vh.ruledecl:
                return vh
    
    # look up doc comment in source file
    def help(self):
        id = int(self.id)
        for fn,vh in vhosts.items():
            if id in vh.ruledecl:
                src = srvroot.read(fn)
                # clean up empty lines + anything not "id:\d+" or "#comment" (prevent catastrophic backtracking)
                src = "\n".join(re.findall("^\s*\#.+$|^.*id:\d+.*$", src, re.M))
                # search comment block preceeding id:....
                r = rx.rule_comment.format(id)
                comment = re.search(r, src, re.X|re.M)
                if comment:
                    comment = re.sub("^#\s*|\\n(?=\\n)", "", comment.group(1), 0, re.M)
                    #comment = re.sub("\\n\\n+", "\n", comment, 0, re.M)
                    return comment.strip()
                break
        return "No documentation comment present"


# filter: look up rule_ids in a given range
def rules_between(min=900000, max=900999):
    return [i for i in sorted(rules.keys()) if i >= min and i <= max]



# scan for APACHE_ENV= vars
def read_env_vars():
    for fn in tmp.env_locations:
        if srvroot.exists(fn):
            src = srvroot.read(fn)
            tmp.env.update(
                dict(rx.shell_vars.findall(src))
            )

# progressbar from rich "▰▰▰▰▰▰▰▰▱▱▱▱▱"
def progress(i=1, n=100, w=72):
    p = i/(n if n else 100)
    s = "▰" * int(round(p * w)) + "▱" * int(round(((1-p) * w)))
    if i >= n:
        print("\033[0K", end="")
    else:
        print("\0337" + s + "\0338", end="")
    sys.stdout.flush()

# iterate over all Apache config files, visit relevant ones (vhosts/mod_security configs)
def scan_all():
    read_env_vars()
    ls = apache_dump_includes()
    for i, fn in enumerate(ls):
        progress(i+1, len(ls))
        src = srvroot.read(fn)
        if rx.interesting.search(src):
            vhosts[fn] = Vhost(fn, src)

# get *.conf list from apache2ctl
def apache_dump_includes():
    stdout = srvroot.popen(["apache2ctl", "-t", "-D", "DUMP_INCLUDES"])
    return rx.dump_includes.findall(stdout.read().decode("utf-8"))

# just used once    
def count_tags():
    import collections
    tags = []
    for fn,v in rules.items():
        if v.tags:
            tags = tags + v.tags
    print(list(reversed(list(collections.Counter(tags).keys()))))
    
# prepare list of names for mainwindow vhosts/conf combobox
def list_vhosts(types=["cfg","vhost"]): #+,"rules" to see all
    return [k for k,v in vhosts.items() if v.t in types]



# initialization (scan_all) is done atop mainwindow

#scan_all()
#count_tags()
#pprint(vhosts)
#print({k:pprint(v.__dict__) for k,v in vhosts.items()})
