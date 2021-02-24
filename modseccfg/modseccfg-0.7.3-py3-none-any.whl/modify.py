# encoding: utf8
# api: modseccfg
# type: function
# category: gui
# title: Modify rules
# description: SecRuleUpdateAction/UpdateTarget dialog
# version: 0.5
# config:
#    { name: modify_updated, type: bool, value: 0, description: Read existing updates from vhost.conf }
# license: Apache-2.0
# doc: https://support.kemptechnologies.com/hc/en-us/articles/209635223-How-to-write-a-WAF-rule-Modsecurity-Rule-Writing
#      https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-%28v2.x%29#SecRuleUpdateActionById
#      https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-%28v2.x%29#SecRuleUpdateTargetById
#
# Combines update of actions and targets(variables) in one dialog.
# Ought to provide a preview of the created directives (after all modseccfg
# is partly about introducing/explaining some of the configuration approaches).
# 
# UI widgets use keys with form syntax (e.g. transforms[], param[msg] or ctl[rulEngine]),
# for easier reassembly and comparison in a SecRule-like structure.
#

import re, json, os, copy
from modseccfg import utils, vhosts, icons, ruleinfo, writer
from modseccfg.utils import conf, log
import PySimpleGUI as sg
import textwrap

def wrap(s):
    return (s or "")[0:120] # tooltips too flaky with multiline text
    return "\n".join( textwrap.wrap(s or "", 70)[0:2] )

class show:

    targets = [
        "ARGS:param", "ARGS:/^\w+/", "ARGS", "ARGS_GET", "ARGS_GET_NAMES", "ARGS_NAMES", "ARGS_POST",
        "ARGS_POST_NAMES", "ENV", "FILES", "FILES_NAMES", "FULL_REQUEST", "FILES_TMPNAMES",
        "FILES_TMP_CONTENT", "GEO", "HIGHEST_SEVERITY", "INBOUND_DATA_ERROR", "MATCHED_VAR", "MATCHED_VARS",
        "MATCHED_VAR_NAME", "MATCHED_VARS_NAMES", "MULTIPART_CRLF_LF_LINES", "MULTIPART_FILENAME",
        "MULTIPART_NAME", "OUTBOUND_DATA_ERROR", "PATH_INFO", "PERF_ALL", "QUERY_STRING", "REMOTE_ADDR",
        "REMOTE_HOST", "REMOTE_PORT", "REMOTE_USER", "REQBODY_ERROR", "REQBODY_ERROR_MSG",
        "REQBODY_PROCESSOR", "REQUEST_BASENAME", "REQUEST_BODY", "REQUEST_BODY_LENGTH", "REQUEST_COOKIES",
        "REQUEST_COOKIES_NAMES", "REQUEST_FILENAME", "REQUEST_HEADERS", "REQUEST_HEADERS_NAMES",
        "REQUEST_LINE", "REQUEST_METHOD", "REQUEST_PROTOCOL", "REQUEST_URI", "REQUEST_URI_RAW",
        "RESPONSE_BODY", "RESPONSE_CONTENT_LENGTH", "RESPONSE_CONTENT_TYPE", "RESPONSE_HEADERS",
        "RESPONSE_HEADERS_NAMES", "RESPONSE_PROTOCOL", "RESPONSE_STATUS", "RULE", "SCRIPT_BASENAME",
        "SCRIPT_FILENAME", "SCRIPT_GID", "SCRIPT_GROUPNAME", "SCRIPT_MODE", "SCRIPT_UID", "SCRIPT_USERNAME",
        "SDBM_DELETE_ERROR", "SERVER_ADDR", "SERVER_NAME", "SERVER_PORT", "SESSION", "SESSIONID",
        "STATUS_LINE", "STREAM_INPUT_BODY", "STREAM_OUTPUT_BODY", "TIME", "TIME_DAY", "TIME_EPOCH",
        "TX", "USERID", "USERAGENT_IP", "WEBAPPID", "WEBSERVER_ERROR_LOG", "XML"
    ]
    flags = [
        ["allow", "pass", "block"],
        ["deny", "drop", "chain"],
        ["log", "auditlog", "capture"],
        ["nolog", "noauditlog"],
        ["multiMatch"],
    ]
    radio = ["allow", "pass", "block", "deny", "drop"]
    transforms = [
        "t:none", "t:base64Decode", "t:sqlHexDecode", "t:base64DecodeExt", "t:base64Encode",
        "t:cmdLine", "t:compressWhitespace", "t:cssDecode", "t:escapeSeqDecode", "t:hexDecode",
        "t:hexEncode", "t:htmlEntityDecode", "t:jsDecode", "t:length", "t:lowercase", "t:md5",
        "t:normalisePath", "t:normalizePath", "t:normalisePathWin", "t:normalizePathWin",
        "t:parityEven7bit", "t:parityOdd7bit", "t:parityZero7bit", "t:removeNulls",
        "t:removeWhitespace", "t:replaceComments", "t:removeCommentsChar", "t:removeComments",
        "t:replaceNulls", "t:urlDecode", "t:uppercase", "t:urlDecodeUni", "t:urlEncode",
        "t:utf8toUnicode", "t:sha1", "t:trimLeft", "t:trimRight", "t:trim"
    ]
    tooltip = {  #@via  e.findall("== (\w+) ==\n'+Description[':]+(.+)", actions_md, re.M)
        'allow': 'Stops rule processing on a successful match and allows the transaction to proceed.',
        'accuracy': 'Specifies the relative accuracy level of the rule related to false positives/negatives.  The value is a string based on a numeric scale (1-9 where 9 is very strong and 1 has many false positives).',
        'append': 'Appends text given as parameter to the end of response body. Content injection must be en- abled (using the SecContentInjection directive). No content type checks are made, which means that before using any of the content injection actions, you must check whether the content type of the response is adequate for injection.',
        'auditlog': 'Marks the transaction for logging in the audit log.',
        'block': 'Performs the disruptive action defined by the previous SecDefaultAction.',
        'capture': 'When used together with the regular expression operator (@rx), the capture action will create copies of the regular expression captures and place them into the transaction variable collection.',
        'chain': 'Chains the current rule with the rule that immediately follows it, creating a rule chain. Chained rules allow for more complex processing logic.',
        'ctl': 'Changes ModSecurity configuration on transient, per-transaction basis. Any changes made using this action will affect only the transaction in which the action is executed. The default configuration, as well as the other transactions running in parallel, will be unaffected.',
        'deny': 'Stops rule processing and intercepts transaction.',
        'deprecatevar': 'Decrements numerical value over time, which makes sense only applied to the variables stored in persistent storage.',
        'drop': 'Initiates an immediate close of the TCP connection by sending a FIN packet.',
        'exec': 'Executes an external script/binary supplied as parameter. As of v2.5.0, if the parameter supplied to exec is a Lua script (detected by the .lua extension) the script will be processed internally. This means you will get direct access to the internal request context from the script. Please read the SecRuleScript documentation for more details on how to write Lua scripts.',
        'expirevar': 'Configures a collection variable to expire after the given time period (in seconds).',
        'id': 'Assigns a unique ID to the rule or chain in which it appears. Starting with ModSecurity 2.7 this action is mandatory and must be numeric.',
        'initcol': 'Initializes a named persistent collection, either by loading data from storage or by creating a new collection in memory.',
        'log': 'Indicates that a successful match of the rule needs to be logged.',
        'logdata': 'Logs a data fragment as part of the alert message.',
        'maturity': 'Specifies the relative maturity level of the rule related to the length of time a rule has been public and the amount of testing it has received.  The value is a string based on a numeric scale (1-9 where 9 is extensively tested and 1 is a brand new experimental rule).',
        'msg': ' Assigns a custom message to the rule or chain in which it appears. The message will be logged along with every alert.',
        'multiMatch': 'If enabled, ModSecurity will perform multiple operator invocations for every target, before and after every anti-evasion transformation is performed.',
        'noauditlog': 'Indicates that a successful match of the rule should not be used as criteria to determine whether the transaction should be logged to the audit log.',
        'nolog': 'Prevents rule matches from appearing in both the error and audit logs.',
        'pass': 'Continues processing with the next rule in spite of a successful match.',
        'pause': 'Pauses transaction processing for the specified number of milliseconds. Starting with ModSecurity 2.7 this feature also supports macro expansion.',
        'phase': 'Places the rule or chain into one of five available processing phases. It can also be used in SecDefaultAction to establish the rule defaults.',
        'prepend': 'Prepends the text given as parameter to response body. Content injection must be enabled (using the SecContentInjection directive). No content type checks are made, which means that before using any of the content injection actions, you must check whether the content type of the response is adequate for injection.',
        'proxy': 'Intercepts the current transaction by forwarding the request to another web server using the proxy backend. The forwarding is carried out transparently to the HTTP client (i.e., there’s no external redirection taking place).',
        'redirect': 'Intercepts transaction by issuing an external (client-visible) redirection to the given location..',
        'rev': 'Specifies rule revision. It is useful in combination with the id action to provide an indication that a rule has been changed.',
        'sanitiseArg': 'Prevents sensitive request parameter data from being logged to audit log. Each byte of the named parameter(s) is replaced with an asterisk.',
        'sanitiseMatched': 'Prevents the matched variable (request argument, request header, or response header) from being logged to audit log. Each byte of the named parameter(s) is replaced with an asterisk.',
        'sanitiseMatchedBytes': 'Prevents the matched string in a variable from being logged to audit log. Each or a range of bytes of the named parameter(s) is replaced with an asterisk.',
        'sanitiseRequestHeader': 'Prevents a named request header from being logged to audit log. Each byte of the named request header is replaced with an asterisk..',
        'sanitiseResponseHeader': 'Prevents a named response header from being logged to audit log. Each byte of the named response header is replaced with an asterisk.',
        'severity': 'Assigns severity to the rule in which it is used.',
        'setuid': 'Special-purpose action that initializes the USER collection using the username provided as parameter.',
        'setrsc': 'Special-purpose action that initializes the RESOURCE collection using a key provided as parameter.',
        'setsid': 'Special-purpose action that initializes the SESSION collection using the session token provided as parameter.',
        'setenv': 'Creates, removes, and updates environment variables that can be accessed by Apache.',
        'setvar': 'Creates, removes, or updates a variable. Variable names are case-insensitive.',
        'skip': 'Skips one or more rules (or chains) on successful match.',
        'status': 'Specifies the response status code to use with actions deny and redirect.',
        't': 'This action is used to specify the transformation pipeline to use to transform the value of each variable used in the rule before matching.',
        'tag': 'Assigns a tag (category) to a rule or a chain.',
        'ver': 'Specifies the rule set version.',
        'xmlns': 'Configures an XML namespace, which will be used in the execution of XPath expressions.',
    }
    colorize = {
        "allow": "#bfc",
        "pass": "#dfc",
        "block": "#dc9",
        "deny": "#fba",
        "drop": "#ea9",
        "pause": "#da4",
        "chain": "#ccc",
    }

    def __init__(self, id, mainwindow, data):
        self.id = id
        self.mainwindow = mainwindow
        self.confn = data["confn"]
        r = vhosts.rules[id]
        if conf.get("modify_updated") and self.confn:
            r = SecRuleCombined(r)
            r.update(vhosts.vhosts[self.confn])
        self.r = r

        # widget options
        bold = dict(font=("Sans", 13, "bold"))
        pad = dict(pad=[(0,0),(12,0)])
        rule_tt = dict(tooltip=r.pattern) # rule @rx tooltip, rather than cluttering dialog with another field

        # vars
        layout = []
        layout += [
            [sg.T("SecRuleUpdate…", **bold), self.w_help("SecRuleUpdateActionById", pad=(0,0))],
            [sg.Multiline("", k="preview", auto_size_text=1, size=(60,4), background_color="#eee")]
        ]
        
        # actions
        layout.append([sg.T("Target/Vars", **bold, **pad), self.w_help("Variables")])
        layout.append([sg.T(" "), sg.InputText(r.vars, disabled=1, size=(30, 1), **rule_tt), sg.T(self.t_target_desc(r), text_color="gray", **rule_tt), sg.B("Info", **rule_tt)])
        layout.append(self.w_combo(0, val=self.suggest_target_exclusion(data)))
        layout.append(self.w_combo(1))
        #layout.append(self.w_combo(2))

        # flags
        layout_flags = [
           [sg.T("Actions/Flags", **bold, **pad), self.w_help("Actions")],
        ]
        for row in show.flags:
            layout_flags.append([self.w_flag(_, radio=(_ in self.radio)) for _ in row])
        # transform
        current = [_ for _ in show.transforms if _ in r.flags]
        #if current and not "t:none" in current:
        #    current.insert(0, "t:none") # add t:none, else existing t:flags would lead to doubled application
        layout_transforms = [
            [sg.T("⭦ Transforms", **bold, **pad), self.w_help("Transformation_functions")],
            [sg.Listbox(show.transforms, current, key="transforms[]", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(22,8), enable_events=True)]
        ]
        # side-by-side: flags + transform
        layout.append([sg.Column(layout_flags), sg.Column(layout_transforms)])

        # params:
        layout.append([sg.T("Actions/Params", **bold, **pad), self.w_help("logdata")])
        layout.append(self.w_param("msg", width=55))
        layout.append(self.w_param("logdata", width=55))
        layout.append(self.w_param("status", width=7, background_color="#fba") + self.w_param("pause", width=8, background_color="#cb6") + self.w_param("redirect", width=30))
        layout.append(self.w_ctl("ruleEngine") + self.w_param("phase", width=7, disabled=1) + self.w_param("skip", width=9, disabled=1))
        layout.append(self.w_param("prepend", width=23) + self.w_param("append", width=24))
        layout.append(self.w_param("exec", width=25) + self.w_param("proxy", width=25))
        # split up, else the dialog becomes unbearable
        layout.append([sg.T("Actions/Control", **bold, **pad), self.w_help("ctl")])
        layout.append(self.w_ctl("auditEngine") + self.w_ctl("auditLogParts", ["", "ABHZ", "ABCFHZ", "ABFHIKZ", "ABCDEFGHIJKZ"], width=15))
        layout.append(self.w_ctl("ruleRemoveById", [""], width=6) + self.w_ctl("ruleRemoveByTag", ["", "attack-disclosure", "OWASP_CRS/POLICY/SIZE_LIMIT", "language-php", "platform-mysql", "OWASP_CRS/WEB_ATTACK/FILE_INJECTION", "language-shell", "attack-protocol"], width=14))
        layout.append(self.w_ctl("ruleRemoveTargetById", [""], width=14) + self.w_ctl("debugLogLevel", ["","0","1","2","3","4","5","6","7","8","9"], width=3))
        layout.append(self.w_param("sanitiseArg", width=20) + self.w_param("sanitiseMatched", width=20))
        # any additional parameters from the rule
        have = ["logdata", "status", "redirect", "phase", "skip", "prepend", "append", "exec", "proxy", "ruleEngine", "auditEngine", "auditLogParts", "ruleRemoveById", "ruleRemoveByTag", "ruleRemoveTargetById", "debugLogLevel", "sanitiseArg", "sanitiseMatched", "setvar", "initcol", "setenv", "deprecatevar"]
        for name in [k for k in r.params.keys() if not k in have]:
            layout.append(self.w_param(name, width=40))
        for name in [k for k in r.ctl.keys() if not k in have]:
            layout.append(self.w_ctl(name, width=35))
        layout.append([sg.T("")])
        # + self.w_param("sanitiseRequestHeader", width=15))

        # window
        layout = [
            [sg.Menu([[f"Rule {id}",["Info", "Save", "Close"]]], key="menu")],
            [sg.Column(layout, expand_x=1, expand_y=0, size=(635,720), scrollable="no", element_justification='left')],
            [sg.Button("Save"), sg.Button("Cancel")]
        ]
        self.w = sg.Window(layout=layout, title=f"⋇ SecRuleUpdate #{id}", resizable=1, font="Sans 12", icon=icons.icon)
        mainwindow.win_register(self.w, self.event)
    

    # widget: flags[] checkbox
    def w_flag(self, name, radio=0):
        kw = {
            "text": f"{name} ", "key": f"flags[{name}]", "disabled": name == "chain",
            "tooltip": wrap(show.tooltip.get(name)), "default": name in self.r.flags,
            "background_color": self.colorize.get(name), "enable_events": True
        }
        return sg.Radio(group_id=radio, **kw) if radio else sg.Checkbox(**kw)

    # widget: params{} input box
    def w_param(self, name, val="", width=55, **kwargs):
        tt = wrap(show.tooltip.get(name))
        width = width - int(len(name) / 1.6)
        if not re.match("^saniti[sz]e|^(xmlns|setenv|expire|deprecate|initcol|exec)|^tag", name): # exclude val= for ACTION_CARDINALITY_MANY args
            val = self.r.__dict__.get(name) or self.r.params.get(name) or self.r.ctl.get(name) or val
        if name == "msg" and self.r.msg_stub:
            val = ""
        return [
            sg.T("  "+name, tooltip=tt),
            sg.InputText(val, key=f"params[{name}]", enable_events=True, size=(width,1), tooltip=tt, **kwargs)
        ]

    # widget: ctl:{} combo box
    def w_ctl(self, name, select=["","On","Off"], width=7, **kwargs):
        tt = wrap(show.tooltip.get(name))
        return [
            sg.T("  ctl:"+name),
            sg.Combo(select, default_value=self.r.ctl.get(name), key=f"ctl[{name}]", size=(width,1), enable_events=True, tooltip=tt, **kwargs)
        ]

    # widget: target/vars combo box
    def w_combo(self, i, val=""):
        return [
            sg.T(" "),
            sg.Combo([""] + ["!"+name for name in show.targets], k=f"vars[{i}]", default_value=val, size=(30,1), enable_events=True, disabled=self.r.vars=="@SecAction"),
            sg.T("!exclude or add", text_color="gray")
        ]

    # widget: help link
    def w_help(self, anchor, **kw):
        help = dict(text_color="#bbd", pad=[(0,0),(12,0)], enable_events=True); help.update(kw)
        return sg.T("(?)", key="https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-%28v2.x%29#"+anchor, **help)

    # description text
    def t_target_desc(self, r):
        if isinstance(r.id, float):
            return "(CHAINED rule!)"
        elif r.vars == "@SecAction":
            return "(Faux rule)"
        return "(current target)"

    # extract an !ARGS:param from current log entry, if any
    def suggest_target_exclusion(self, data):
        if not data.get("log"):
            return ""
        args = re.findall("\\b(ARGS:[\w\-\[\].]+)", str(data["log"]))
        return ",".join(list(set(["!"+a for a in args])))


    # act on changed widgets or save/close event
    def event(self, event, data):
        if event == "Info":
            self.mainwindow.info(data)
        elif event in ("Close", "Cancel"):
            self.w.close()
        elif re.match("^\w+://", event):
            os.system("xdg-open %r" % event)
        elif event == "Save":
            src = self.w["preview"].get()
            if re.match("^\s*Sec", src, re.M):
                writer.append(self.confn, src, "", "")
                self.w.close()
        else:
            self.w["preview"].update(self.construct(self.rule_dict(data)))
    
    # get name[field] from widget data, transform into SecRule-like structure
    def rule_dict(self, data):
        opts = {
            "vars": {},
            "flags": {},
            "params": {},
            "ctl": {},
            "msg": "",
            "logdata": "",
        }
        for k,v in data.items():
            if v and isinstance(k, str) and k.find("[") >= 0:
                name, key, *uu = re.split("[\[\]]", k)
                if name=="transforms":
                    for key in v: # already a list
                        opts["flags"][key] = 1
                #elif key == "logdata":
                #    opts[key] = v # properties, but also params{}
                elif key == "msg":
                    # only assign legitimate/new message, not faux @SecAction or VARS+PATTERN
                    if not self.r.msg_stub or v != self.r.msg:
                        opts[key] = v
                else:
                    opts[name][key] = v
        return opts

    # SecRuleUpdate.. assembly
    #   (Not sure anymore if the rule split in .vars/.params/.flags/.setvar has simplified much here.
    #   Certainly did help for ruleinfo, but now this requires quite a bit of fiddling to construct a
    #   plain list again.)
    exclude_flags = ["tag"] #"ver", "rev", "severity", "tag", "accuracy", "maturity"]
    def construct(self, opts):
        src = ""

        # id:offset
        if isinstance(self.id, float):
            id_offset = str(self.id).replace(".", ":")
        else:
            id_offset = str(self.id)

        # output UpdateTarget if any were set
        vals = opts['vars'].values()
        if vals:
            # uses comma separation for targes !ARGS1,!ARGS2 rather than vertbar | like SecRules
            vals = ','.join(vals)
            src += f"SecRuleUpdateTargetById {id_offset} \"{vals}\"\n"
            # Could do something more clever here, like merging similar attributes,
            # or using the REPLACED_TARGET scheme. For now it's just appending though.

        # add UpdateAction if flags differ from secrule
        flags = list(opts["flags"].keys())
        old_params = {k:v for k,v in self.r.params.items() if k not in show.exclude_flags}
        print("opts==", opts)
        print("r.flags==", self.r.flags)
        print("new.flags==", flags)
        print("r.params==", old_params)
        print("new.params==", opts["params"])
        print("r.ctl==", self.r.ctl)
        print("new.ctl==", opts["ctl"])
        if set(flags) != set(self.r.flags) or opts["params"] != old_params or opts["ctl"] != self.r.ctl:
            # merge params to list
            opts["params"].update({"ctl:"+k:v for k,v in opts["ctl"].items()})
            for k,v in opts["params"].items():
                if k == "phase":
                    continue
                if not re.match("^\w+$",v):
                    v = f"'{v}'"
                if k.find(":") > 0:
                    flags.append(f"{k}={v}")
                else:
                    flags.append(f"{k}:{v}")
            # add msg+logdata individually
            for k in ["msg", "logdata"]:
                if opts.get(k):
                    flags.append(f"{k}:'{opts[k]}'")
            # mk directive
            flags = ', '.join(flags)
            src += f"SecRuleUpdateActionById {id_offset} \"{flags}\"\n"

        return src

# merge global rule definition with local vhost.conf overrides
class SecRuleCombined(vhosts.SecRule):

    def __init__(self, rule):
        # initialize properties .msg/.flags/.params/.tags from global rule
        self.__dict__.update(copy.deepcopy(rule.__dict__))
        
    def update(self, vhost):
        # vhost.update{} contains directive arguments from SecRuleUpdateActionsById/TargetById
        add = vhost.update.get(self.id)
        log.debug("SecRuleCombined.update():", self.id, add)
        if not add:
            return
        # contain text-lists of updates only, so we need to post-process them
        for vars in add["vars"]:
            self.vars += "," + vars
        for actions in add["actions"]:
            # split up actions,attributes:…
            for pfx, action, value, qvalue in vhosts.rx.actions.findall(actions):
                #log.debug(pfx,action,value,qvalue)
                self.assign(pfx, action, value or qvalue)
        self.flags = list(set(self.flags))

