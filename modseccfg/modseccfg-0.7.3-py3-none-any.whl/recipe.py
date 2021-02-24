# api: modseccfg
# encoding: utf-8
# version: 0.5
# type: data
# title: recipe
# description: Apache/mod_security config examples or conversions
# category: config
# config:
#    { name: preconf, type: bool, value: 0, description: "Create and use *.preconf files automatically" }
#    { name: user_recipes, type: bool, value: 0, description: "Load templates from ~/.config/modseccfg/**/*.txt" }
# license: Apache-2.0
#
# Basically just blobs of text and an editor window.
# [Save] will append directives to selected vhost/*.conf file.
#
# Some samples from:
#  · https://wiki.atomicorp.com/wiki/index.php/Mod_security
#


from modseccfg import utils, vhosts, writer
from modseccfg.utils import DictObj, conf
import PySimpleGUI as sg
import re, random, glob
from textwrap import dedent


# predefine some callbacks, to get merged into templates{}
class template_funcs:
    @staticmethod
    def crs_preconfig(data, vars):
        # loop over vhosts/.fn to figure out standard vhosts.conf dirs → add *.preconf
        dirs = []
        for fn, vh in vhosts.vhosts.items():
            if vh.t == "vhost" and vh.cfg.get("documentroot"):
                if re.search("/[\w\-]+\.conf", fn):
                    d = re.sub("/[^/]+$", "/*.preconf", fn)
                elif re.search("/\w+\.[^/]+\.conf", fn):
                    d = re.sub("(/\w+)\.[^/]+$", "\\1.*.preconf", fn)
                else:
                    d = re.sub("/[^/]+$", "/*.preconf", fn)
                dirs.append(d)
        if not dirs:
            dirs = ["/etc/apache2/sites-enabled/*.preconf"]
        # combine
        warn = dedent("""
            # +------------------------------------------------------------------+
            # | WARNING: This should be appended to:                             |
            # | /etc/modsecurity/crs/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf |
            # +------------------------------------------------------------------+
        """).lstrip()
        src = dedent("""
            # --
            # @modseccfg
            # Include vhost *.preconf files to allow conditionalizing CRS rules.
            #
            #  · SecRuleDisableById can go directly into normal vhost.confs
            #  · But recipes and CRS options better reside in 900-EXCLUSION or a *.preconf file
            #  · Each vhost.*.preconf should declare a <Directory> matching its DocumentRoot

        """)
        if not re.search("900-EXCLUSION", data["confn"]):
            src = warn + src
        for d in list(set(dirs)):
            src += f"IncludeOptional {d}\n"
        return src


# config snippets + menu structure
templates = DictObj({

    #-- <Wrap> excludes
    "<Wrap> exclusions": {

        "<Location>": """
            <Location "/app/">
              SecRuleRemoveById $id   # $msg
              # SecRuleEngine DetectionOnly
            </Location>
        """,

        "<Directory>": """
            <Directory "$documentroot$request_uri">
              SecRuleRemoveById $id   # $msg
            </Directory>
        """,

        "<FilesMatch>": """
            <FilesMatch "\.php$">
              SecRuleRemoveById $id   # $msg
            </FilesMatch>
        """
    },

    #-- basic rules    
    "Exclude Parameter": """
        # Exclude GET/POST parameter from rule
        #
        SecRuleUpdateTargetByID $id "!ARGS:param"
    """,
    
    "Rule to DetectionOnly": """
        # One rule to DetectionOnly
        #
        SecRuleUpdateActionById $id "pass,status:200,log,auditlog"
    """,

    "URL to DetectionOnly": """
        # Set one URL to DetectionOnly
        #
        SecRule REQUEST_URI "$request_uri" "phase:1,id:$rand,tag:modseccfg,tag:url-detectiononly,t:none,t:lowercase,pass,msg:'DetectionOnly for $request_uri',ctl:ruleEngine=DetectionOnly"
    """,

    #-- from REQUEST-900-EXCLUSION examples
    "Example Exlusions": {

        "Ignore param for tag": """
            # Removing a specific ARGS parameter from inspection for only certain attacks
            SecRule REQUEST_FILENAME "@endsWith $PATH" "id:$rand,phase:2,pass,nolog,tag:modseccfg,tag:ignore-param,ctl:ruleRemoveTargetByTag=attack-sqli;ARGS:pwd"
        """,

        "Ignore param for all": """
            # Removing a specific ARGS parameter from inspection for all CRS rules
            SecRule REQUEST_FILENAME "@endsWith /wp-login.php" "id:$rand,phase:2,pass,nolog,tag:modseccfg,tag:ignore-param,ctl:ruleRemoveTargetByTag=OWASP_CRS;ARGS:pwd"
        """,

        "Remove rule range": """
            # Removing a range of rules
            SecRule REQUEST_FILENAME "@beginsWith /admin" "id:$rand,phase:2,pass,nolog,tag:modseccfg,tag:remove-rule,ctl:ruleRemoveById=941000-942999"
        """
    },

    #-- developer tools
    "Whitelist IP": {
    
        "Exempt REMOTE_ADDR": """
            # Exempt client addr from all SecRules
            #
            SecRule REMOTE_ADDR "@streq $remote_addr" "phase:1,id:$rand,t:none,nolog,allow,tag:modseccfg,tag:whitelist,ctl:ruleEngine=Off,ctl:auditEngine=Off"
        """,

        "Whitelist from file": """
            # List of IPs from filename trigger DetectionOnly mode
            #
            SecRule REMOTE_ADDR "@pmFromFile $confn.whitelist" "phase:1,id:$rand,t:none,nolog,allow,tag:modseccfg,tag:whitelist,ctl:ruleEngine=DetectionOnly"
        """
    },
    
    #-- complex/setup rules
    "Macros": {    

        "Macro definitions": """
            # This directive block defines some macros, which you can use to simplify a few
            # SecRules exceptions. Best applied to a central *.conf file, rather than vhosts.
            # An `Use` directive/prefix is necessary to expand these macros.
            #     ↓
            #    Use SecRuleRemoveByPath 900410 /app/exempt/
            #    Use SecIgnoreArgByPathAndId 900410 /calc.php exec
            #
            <IfModule mod_macro.c>

              <Macro NEWID $STR>
                # define %{ENV:NEWID} in the 50000 range; might yield duplicates
                SetEnvIfExpr "md5('$STR') =~ /(\d).*(\d).*(\d).*(\d)/" "NEWID=5$1$2$3$4"
              </Macro>

              <Macro SecRuleRemoveByPath $ID $PATH>
                Use NEWID "$ID$PATH"
                SecRule REQUEST_URI "@streq $PATH" "id:%{ENV:NEWID},phase:1,t:none,pass,tag:modseccfg,tag:whitelist,msg:'Whitelist «$PATH»',ctl:removeById=$ID"
              </Macro>

              <Macro SecIgnoreArgByPathAndId $ID $PATH $ARG>
                Use NEWID "$ID$PATH"
                SecRule REQUEST_URI "@streq $PATH" "id:%{ENV:NEWID},phase:1,t:none,nolog,pass,tag:modseccfg,tag:remove-rule,ctl:ruleRemoveTargetById=$ID;ARGS:$ARG"
              </Macro>

              <Macro SecVar $VAR $VAL>
                Use NEWID "$VAR=$VAL"
                SecAction "id:%{ENV:NEWID},phase:1,nolog,pass,tag:modseccfg,tag:setvar,t:none,setvar:'$VAR=$VAL'"
              </Macro>

            </IfModule>
    """
    },

    #-- main config
    "Setup": {    

        "CRS *.preconf includes": template_funcs.crs_preconfig,
        
        "Cloudflare / IP2LOCATION": """
            # Use mod_ip2location or Cloudflare header
            #
            SetEnvIfExpr "req('CF-IPCountry') =~ '\w\w'" IP2LOCATION_COUNTRY_SHORT=%{HTTP_CF_IPCOUNTRY}
            SecRule ENV:IP2LOCATION_COUNTRY_SHORT "!^(UK|DE|FR)$" "id:$rand,deny,status:500,msg:'Req not from whitelisted country'"
        """,

        "Cloudflare RemoteIP": """
            # Sets REMOTE_ADDR for Apache at large per mod_remoteip.
            # @url https://support.cloudflare.com/hc/en-us/articles/360029696071-Orig-IPs
            #
            <IfModule mod_remoteip.c>
               RemoteIPHeader CF-Connecting-IP
               RemoteIPTrustedProxy 173.245.48.0/20
               RemoteIPTrustedProxy 103.21.244.0/22
               RemoteIPTrustedProxy 103.22.200.0/22
               RemoteIPTrustedProxy 103.31.4.0/22
               RemoteIPTrustedProxy 141.101.64.0/18
               RemoteIPTrustedProxy 108.162.192.0/18
               RemoteIPTrustedProxy 190.93.240.0/20
               RemoteIPTrustedProxy 188.114.96.0/20
               RemoteIPTrustedProxy 197.234.240.0/22
               RemoteIPTrustedProxy 198.41.128.0/17
               RemoteIPTrustedProxy 162.158.0.0/15
               RemoteIPTrustedProxy 104.16.0.0/12
               RemoteIPTrustedProxy 172.64.0.0/13
               RemoteIPTrustedProxy 131.0.72.0/22
               RemoteIPTrustedProxy 2400:cb00::/32
               RemoteIPTrustedProxy 2606:4700::/32
               RemoteIPTrustedProxy 2803:f800::/32
               RemoteIPTrustedProxy 2405:b500::/32
               RemoteIPTrustedProxy 2405:8100::/32
               RemoteIPTrustedProxy 2a06:98c0::/29
               RemoteIPTrustedProxy 2c0f:f248::/32
            </IfModule>

            # Fallback alternative for CRS/mod_security, apply same remote_addr check,
            # but update only CRSs tx.real_ip and remote_addr internally. Not sure
            # if this will yield correct audit log entries.
            #
            <IfModule mod_security.c>
               # Test if remote_addr matches Cloudflare IPs
               #
               SecRule REMOTE_ADDR "@ipMatch 173.245.48.0/20,103.21.244.0/22,103.22.200.0/22,103.31.4.0/22,141.101.64.0/18,108.162.192.0/18,190.93.240.0/20,188.114.96.0/20,197.234.240.0/22,198.41.128.0/17,162.158.0.0/15,104.16.0.0/12,172.64.0.0/13,131.0.72.0/22,2400:cb00::/32,2606:4700::/32,2803:f800::/32,2405:b500::/32,2405:8100::/32,2a06:98c0::/29,2c0f:f248::/32" \
                   "id:7030,t:none,pass,setvar:TX.IS_CLOUDFLARE=1,setvar:TX.IS_CDN=1,tag:modseccfg,tag:remote-addr,tag:setvar,msg:'Cloudflare CDN'"

               # Update TX.REAL.IP + REMOTE_ADDR from CF-Connecting-IP:
               #
               SecRule TX.IS_CLOUDFLARE "@eq 1" "id:7031,t:none,chain,pass,tag:modseccfg,tag:remote-addr,tag:setvar,msg:'Set TX.REAL_IP from Cloudflare CF-Connecting-IP'"
               SecRule REQUEST_HEADERS:cf-connecting-ip "@rx ^[\d\.:a-f]+$" "pass,t:none,capture,setvar:'TX.REAL_IP=%{TX:0}',setvar:'REMOTE_ADDR=%{TX:0}',setenv:'REMOTE_ADDR=%{TX:0}',logdata:'TX.REAL_IP=%{TX:0} set from Cloudflare CDN header'"
            </IfModule>
        """,
         
        "Apache Error/LogFormat": """
            # Extend error log w/ REQUEST_URI and somewhat standard datetime format (not quite 8601)
            #  → Feedback appreciated. What ought to be the post-90s Apache default?
            #
            SetEnvIf Request_URI "(^.*$)" REQ=$1
            ErrorLogFormat "[%{cu}t] [%m:%l] [pid %P:tid %T] [client %a] %E: %M [request_uri \"%{REQ}e\"]"
            
            # "extended" log format
            # @url https://github.com/Apache-Labor/labor/tree/master/labor-04
            #
            LogFormat "%h %{GEOIP_COUNTRY_CODE}e %u [%{%Y-%m-%d %H:%M:%S}t.%{usec_frac}t] \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{Content-Type}i\" %{remote}p %v %A %p %R %{BALANCER_WORKER_ROUTE}e %X \"%{cookie}n\" %{UNIQUE_ID}e %{SSL_PROTOCOL}x %{SSL_CIPHER}x %I %O %{ratio}n%% %D %{ModSecTimeIn}e %{ApplicationTime}e %{ModSecTimeOut}e %{ModSecAnomalyScoreInPLs}e %{ModSecAnomalyScoreOutPLs}e %{ModSecAnomalyScoreIn}e %{ModSecAnomalyScoreOut}e" extended
        """,
        
        "preconf_stub": """
            # type: config
            # sort: pre-crs
            # class: apache
            # title: {ServerName}
            # description: early mod_security configuration
            #
            # For SecRule directives that should override CRS rules, or using modseccfg macros etc.
            # SecRuleDisableById settings belong into regular vhost.conf still.
            # (Still not sure about CRS variable overrides.)
            
            <Directory {DocumentRoot}>
               # Use SecRuleRemoveByPath 900130 /app/
               
            </Directory>
        """

    },
    
    # flat list of all titles
    "has": []
})


# assemble menu list from templates.menu{}
def ls(templ):
    l = []
    for title,e in templ.items():
        if title.startswith("_") or title == "has":
            continue
        if True:
            l.append(title)
        if isinstance(e, dict):
            l.append(ls(e))
        else:
            templates.has.append(title)
    return l

def user_rec():
    templates[".config/modseccfg/*"] = add = {}
    for fn in glob.glob(f"{conf.conf_dir}/**/*.txt"):
        src = open(fn, "r", encoding="utf-8").read()
        add[fn[len(conf.conf_dir)+1:]] = src

# inject recipe list to main menu
def init(menu, **kwargs):
    if conf.get("user_recipes"):
        user_rec()
    i_ls = menu.index(["Recipe"]) # already a list
    menu[i_ls].append(ls(templates.__dict__))
   
def has(name):
    return name in templates.has


# window
class show:

    def __init__(self, name="", raw_event="Menu", data={}, mainwindow=None, **kwargs):

        # extract infos from main UI (id and log elements)
        self.name = name
        self.fn = data["confn"]
        vars = self.vars(data)

        # find text or func
        text = self.find_in_dict(raw_event, templates)
        if type(text) is str:
            if text.startswith("@"):
                # or better: pluginconf.get_data()
                text = re.sub("[^/]+$", text.lstrip("@"), __file__)
                text = open(text, "r", encoding="utf-8").read()
            text = dedent(text).lstrip()
            text = self.repl(text, vars)
        else:
            text = text(data, vars).lstrip()
        #print(data)
        #print(text)
        
        # create window and dispatch to main event loop
        self.w = sg.Window(title=f"Recipe '{name}'", resizable=1, layout=[
            [sg.Multiline(default_text=text, key="src", size=(90,24), font="Mono 12")],
            [sg.Button(f"Save to {self.fn}", key="save"), sg.Button("Cancel", key="cancel")]
        ])
        mainwindow.win_register(self.w, self.event)

    # write …
    def event(self, event, data):
        #print(data)
        if event == "save":
            text = data["src"]
            # possibly redirect to *.preconf
            fn = writer.fn_preconf(self.fn, addsrc=text)
            writer.append(fn=fn, directive=text, value="", comment="")
            # postconfig hooks
            if hasattr(self, self.name):
                getattr(self, self.name)()
        self.w.close()

    # hooks after saving
    def crs_preconfig_includes(self):
        vhosts.tmp.decl_preconf = True
        #conf["preconf"] = 1; utils.cfg_write()?
        
    def find_in_dict(self, key, d):
        for k,v in d.items():
            if k == key:
                return v
            elif isinstance(v, dict):
                v = self.find_in_dict(key, v)
                if v:
                    return v

    # prepare vars dict from mainwindow event data + selected log line
    def vars(self, data):
        vh = vhosts.vhosts.get(data.get("confn", "-"), {})
        vars = {
            "id": "0",
            "rand": random.randrange(2000,5000),
            "request_uri": "/PATH",
            "confn": data.get("confn"),
            "documentroot": vh.cfg.get("documentroot", "") if vh else "/srv/www"
        }
        if data.get("log"):
            for k,v in re.findall('\[(\w+) "([^"]+)"\]', str(data["log"])):
                if k in ("uri", "request_line",): k = "request_uri"
                if k in ("request_uri",): v = re.escape(v)
                vars[k] = v
        if data.get("rule"):
            vars["id"] = data["rule"][0]
        return vars

    # substitute $varnames in text string
    def repl(self, text, vars):
        text = re.sub(r"\$(\w+)", lambda m,*k: str(vars.get(m.group(1), m.group(0))), text)
        return text

