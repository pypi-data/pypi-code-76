# api: modseccfg
# encoding: utf-8
# type: function
# category: config
# title: CRS options
# description: config window for CoreRuleSet setvar flags
# version: 0.3
# depends: pluginconf (>= 0.7.3)
# config:
#    { name: crsopt_defaults, type: bool, value: 0, description: "Use defaults in place of existing *.conf options" }
#    { name: crsopt_undefine, type: bool, value: 1, description: "Undefine previous config rules per setvar" }
# license: Apache-2.0
# author: OWASP CRS team (options and descriptions)
#
# Basically like SecOptions, but for CRS options (from crs-setup.conf).
# But this module will not replace them, but inject a combined SecAction,
# which overrides all variables in one swoop.
#
# Hence it requires declaring an id. Default is 5999 in the user range.
# If the distributed crs-setup.conf is targeted, you want to set the id
# to 900999 instead, so it applies AFTER all SecActions in there.
# (We could add another mode to update individual SecAction entries, but
# that's probably too detailobsessed.)
#



import re, json, os, copy
from collections import OrderedDict
import pluginconf, pluginconf.gui
from modseccfg import utils, writer, vhosts, icons
from modseccfg.utils import srvroot


# autoconverted via `dev/crsvars2pmd.py`
setvar = OrderedDict()
setvar['id'] = {
    "id": "5999",
    "name": "id",
    "description": "Override variables early (5999) or inject after crs-setup (900999)",
    "type": "select",
    "value": "5999",
    "help": "Override variables early (5999) or inject after crs-setup (900999)\nYou want to use 9009999 if you update the global crs-setup.conf.\nBut if you need different settings for different vhosts, then\nkeep crs-setup.conf disabled, and create individual setup files.\n(This could probably be automated in the dialog. And ideally, we'd\nuse skipAfter= or something in conjunction for the override scheme.)",
    "select": {
        "5999": "5999",
        "900999": "900999"
    }
}
setvar['fn'] = {
    "id": "5998",
    "name": "fn",
    "description": "Which *.conf file to write back to.",
    "type": "select", ## dev/update might reset this ##
    "value": "/etc/modsecurty/crs/crs-setup.conf",
    "select": {},
    "help": "Which *.conf file to write back to.\nIf you want to read out rules from crs-setup.conf, but then\nwrite to a custom location; use this option. Start the dialog\n(File\u2192CRS option) whilst crs-setup.conf is selected, then\nchange the target filename here."
}
setvar['tx.paranoia_level'] = {
    "id": "900000",
    "name": "tx.paranoia_level",
    "description": "The Paranoia Level (PL) setting allows you to choose the desired level",
    "type": "select",
    "value": "1",
    "help": "The Paranoia Level (PL) setting allows you to choose the desired level\nof rule checks that will add to your anomaly scores.\nWith each paranoia level increase, the CRS enables additional rules\ngiving you a higher level of security. However, higher paranoia levels\nalso increase the possibility of blocking some legitimate traffic due to\nfalse alarms (also named false positives or FPs). If you use higher\nparanoia levels, it is likely that you will need to add some exclusion\nrules for certain requests and applications receiving complex input.\n- A paranoia level of 1 is default. In this level, most core rules\nare enabled. PL1 is advised for beginners, installations\ncovering many different sites and applications, and for setups\nwith standard security requirements.\nAt PL1 you should face FPs rarely. If you encounter FPs, please\nopen an issue on the CRS GitHub site and don't forget to attach your\ncomplete Audit Log record for the request with the issue.\n- Paranoia level 2 includes many extra rules, for instance enabling\nmany regexp-based SQL and XSS injection protections, and adding\nextra keywords checked for code injections. PL2 is advised\nfor moderate to experienced users desiring more complete coverage\nand for installations with elevated security requirements.\nPL2 comes with some FPs which you need to handle.\n- Paranoia level 3 enables more rules and keyword lists, and tweaks\nlimits on special characters used. PL3 is aimed at users experienced\nat the handling of FPs and at installations with a high security\nrequirement.\n- Paranoia level 4 further restricts special characters.\nThe highest level is advised for experienced users protecting\ninstallations with very high security requirements. Running PL4 will\nlikely produce a very high number of FPs which have to be\ntreated before the site can go productive.\nRules in paranoia level 2 or higher will log their PL to the audit log;\nexample: [tag \"paranoia-level/2\"]. This allows you to deduct from the\naudit log how the WAF behavior is affected by paranoia level.\nIt is important to also look into the variable\ntx.enforce_bodyproc_urlencoded (Enforce Body Processor URLENCODED)\ndefined below. Enabling it closes a possible bypass of CRS.\nUncomment this rule to change the default:",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.executing_paranoia_level'] = {
    "id": "900001",
    "name": "tx.executing_paranoia_level",
    "description": "It is possible to execute rules from a higher paranoia level but not include",
    "type": "select",
    "value": "1",
    "help": "It is possible to execute rules from a higher paranoia level but not include\nthem in the anomaly scoring. This allows you to take a well-tuned system on\nparanoia level 1 and add rules from paranoia level 2 without having to fear\nthe new rules would lead to false positives that raise your score above the\nthreshold.\nThis optional feature is enabled by uncommenting the following rule and\nsetting the tx.executing_paranoia_level.\nTechnically, rules up to the level defined in tx.executing_paranoia_level\nwill be executed, but only the rules up to tx.paranoia_level affect the\nanomaly scores.\nBy default, tx.executing_paranoia_level is set to tx.paranoia_level.\ntx.executing_paranoia_level must not be lower than tx.paranoia_level.\nPlease notice that setting tx.executing_paranoia_level to a higher paranoia\nlevel results in a performance impact that is equally high as setting\ntx.paranoia_level to said level.",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.enforce_bodyproc_urlencoded'] = {
    "id": "900010",
    "name": "tx.enforce_bodyproc_urlencoded",
    "description": "ModSecurity selects the body processor based on the Content-Type request",
    "type": "bool",
    "value": "1",
    "help": "ModSecurity selects the body processor based on the Content-Type request\nheader. But clients are not always setting the Content-Type header for their\nrequest body payloads. This will leave ModSecurity with limited vision into\nthe payload.  The variable tx.enforce_bodyproc_urlencoded lets you force the\nURLENCODED body processor in these situations. This is off by default, as it\nimplies a change of the behaviour of ModSecurity beyond CRS (the body\nprocessor applies to all rules, not only CRS) and because it may lead to\nfalse positives already on paranoia level 1. However, enabling this variable\ncloses a possible bypass of CRS so it should be considered.\nUncomment this rule to change the default:"
}
setvar['tx.critical_anomaly_score'] = {
    "id": "900100",
    "name": "tx.critical_anomaly_score",
    "description": "Each rule in the CRS has an associated severity level.",
    "type": "select",
    "value": "5",
    "help": "Each rule in the CRS has an associated severity level.\nThese are the default scoring points for each severity level.\nThese settings will be used to increment the anomaly score if a rule matches.\nYou may adjust these points to your liking, but this is usually not needed.\n- CRITICAL severity: Anomaly Score of 5.\nMostly generated by the application attack rules (93x and 94x files).\n- ERROR severity: Anomaly Score of 4.\nGenerated mostly from outbound leakage rules (95x files).\n- WARNING severity: Anomaly Score of 3.\nGenerated mostly by malicious client rules (91x files).\n- NOTICE severity: Anomaly Score of 2.\nGenerated mostly by the protocol rules (92x files).\nIn anomaly mode, these scores are cumulative.\nSo it's possible for a request to hit multiple rules.\n(Note: In this file, we use 'phase:1' to set CRS configuration variables.\nIn general, 'phase:request' is used. However, we want to make absolutely sure\nthat all configuration variables are set before the CRS rules are processed.)",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.error_anomaly_score'] = {
    "id": "900100",
    "name": "tx.error_anomaly_score",
    "description": "Each rule in the CRS has an associated severity level.",
    "type": "select",
    "value": "4",
    "help": "Each rule in the CRS has an associated severity level.\nThese are the default scoring points for each severity level.\nThese settings will be used to increment the anomaly score if a rule matches.\nYou may adjust these points to your liking, but this is usually not needed.\n- CRITICAL severity: Anomaly Score of 5.\nMostly generated by the application attack rules (93x and 94x files).\n- ERROR severity: Anomaly Score of 4.\nGenerated mostly from outbound leakage rules (95x files).\n- WARNING severity: Anomaly Score of 3.\nGenerated mostly by malicious client rules (91x files).\n- NOTICE severity: Anomaly Score of 2.\nGenerated mostly by the protocol rules (92x files).\nIn anomaly mode, these scores are cumulative.\nSo it's possible for a request to hit multiple rules.\n(Note: In this file, we use 'phase:1' to set CRS configuration variables.\nIn general, 'phase:request' is used. However, we want to make absolutely sure\nthat all configuration variables are set before the CRS rules are processed.)",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.warning_anomaly_score'] = {
    "id": "900100",
    "name": "tx.warning_anomaly_score",
    "description": "Each rule in the CRS has an associated severity level.",
    "type": "select",
    "value": "3",
    "help": "Each rule in the CRS has an associated severity level.\nThese are the default scoring points for each severity level.\nThese settings will be used to increment the anomaly score if a rule matches.\nYou may adjust these points to your liking, but this is usually not needed.\n- CRITICAL severity: Anomaly Score of 5.\nMostly generated by the application attack rules (93x and 94x files).\n- ERROR severity: Anomaly Score of 4.\nGenerated mostly from outbound leakage rules (95x files).\n- WARNING severity: Anomaly Score of 3.\nGenerated mostly by malicious client rules (91x files).\n- NOTICE severity: Anomaly Score of 2.\nGenerated mostly by the protocol rules (92x files).\nIn anomaly mode, these scores are cumulative.\nSo it's possible for a request to hit multiple rules.\n(Note: In this file, we use 'phase:1' to set CRS configuration variables.\nIn general, 'phase:request' is used. However, we want to make absolutely sure\nthat all configuration variables are set before the CRS rules are processed.)",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.notice_anomaly_score'] = {
    "id": "900100",
    "name": "tx.notice_anomaly_score",
    "description": "Each rule in the CRS has an associated severity level.",
    "type": "select",
    "value": "2",
    "help": "Each rule in the CRS has an associated severity level.\nThese are the default scoring points for each severity level.\nThese settings will be used to increment the anomaly score if a rule matches.\nYou may adjust these points to your liking, but this is usually not needed.\n- CRITICAL severity: Anomaly Score of 5.\nMostly generated by the application attack rules (93x and 94x files).\n- ERROR severity: Anomaly Score of 4.\nGenerated mostly from outbound leakage rules (95x files).\n- WARNING severity: Anomaly Score of 3.\nGenerated mostly by malicious client rules (91x files).\n- NOTICE severity: Anomaly Score of 2.\nGenerated mostly by the protocol rules (92x files).\nIn anomaly mode, these scores are cumulative.\nSo it's possible for a request to hit multiple rules.\n(Note: In this file, we use 'phase:1' to set CRS configuration variables.\nIn general, 'phase:request' is used. However, we want to make absolutely sure\nthat all configuration variables are set before the CRS rules are processed.)",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.inbound_anomaly_score_threshold'] = {
    "id": "900110",
    "name": "tx.inbound_anomaly_score_threshold",
    "description": "Here, you can specify at which cumulative anomaly score an inbound request,",
    "type": "select",
    "value": "5",
    "help": "Here, you can specify at which cumulative anomaly score an inbound request,\nor outbound response, gets blocked.\nMost detected inbound threats will give a critical score of 5.\nSmaller violations, like violations of protocol/standards, carry lower scores.\n[ At default value ]\nIf you keep the blocking thresholds at the defaults, the CRS will work\nsimilarly to previous CRS versions: a single critical rule match will cause\nthe request to be blocked and logged.\n[ Using higher values ]\nIf you want to make the CRS less sensitive, you can increase the blocking\nthresholds, for instance to 7 (which would require multiple rule matches\nbefore blocking) or 10 (which would require at least two critical alerts - or\na combination of many lesser alerts), or even higher. However, increasing the\nthresholds might cause some attacks to bypass the CRS rules or your policies.\n[ New deployment strategy: Starting high and decreasing ]\nIt is a common practice to start a fresh CRS installation with elevated\nanomaly scoring thresholds (>100) and then lower the limits as your\nconfidence in the setup grows. You may also look into the Sampling\nPercentage section below for a different strategy to ease into a new\nCRS installation.\n[ Anomaly Threshold / Paranoia Level Quadrant ]\nHigh Anomaly Limit   |   High Anomaly Limit\nLow Paranoia Level   |   High Paranoia Level\n-> Fresh Site        |   -> Experimental Site\n------------------------------------------------------\nLow Anomaly Limit    |   Low Anomaly Limit\nLow Paranoia Level   |   High Paranoia Level\n-> Standard Site     |   -> High Security Site\nUncomment this rule to change the defaults:",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.outbound_anomaly_score_threshold'] = {
    "id": "900110",
    "name": "tx.outbound_anomaly_score_threshold",
    "description": "Here, you can specify at which cumulative anomaly score an inbound request,",
    "type": "select",
    "value": "4",
    "help": "Here, you can specify at which cumulative anomaly score an inbound request,\nor outbound response, gets blocked.\nMost detected inbound threats will give a critical score of 5.\nSmaller violations, like violations of protocol/standards, carry lower scores.\n[ At default value ]\nIf you keep the blocking thresholds at the defaults, the CRS will work\nsimilarly to previous CRS versions: a single critical rule match will cause\nthe request to be blocked and logged.\n[ Using higher values ]\nIf you want to make the CRS less sensitive, you can increase the blocking\nthresholds, for instance to 7 (which would require multiple rule matches\nbefore blocking) or 10 (which would require at least two critical alerts - or\na combination of many lesser alerts), or even higher. However, increasing the\nthresholds might cause some attacks to bypass the CRS rules or your policies.\n[ New deployment strategy: Starting high and decreasing ]\nIt is a common practice to start a fresh CRS installation with elevated\nanomaly scoring thresholds (>100) and then lower the limits as your\nconfidence in the setup grows. You may also look into the Sampling\nPercentage section below for a different strategy to ease into a new\nCRS installation.\n[ Anomaly Threshold / Paranoia Level Quadrant ]\nHigh Anomaly Limit   |   High Anomaly Limit\nLow Paranoia Level   |   High Paranoia Level\n-> Fresh Site        |   -> Experimental Site\n------------------------------------------------------\nLow Anomaly Limit    |   Low Anomaly Limit\nLow Paranoia Level   |   High Paranoia Level\n-> Standard Site     |   -> High Security Site\nUncomment this rule to change the defaults:",
    "select": {
        "0": "0 (off)",
        "1": "1 (standard)",
        "2": "2 (extended)",
        "3": "3 (excessive)",
        "4": "4 (banking sector)",
        "5": "5 (absurd)"
    }
}
setvar['tx.crs_exclusions_cpanel'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_cpanel",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.crs_exclusions_drupal'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_drupal",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.crs_exclusions_dokuwiki'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_dokuwiki",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.crs_exclusions_nextcloud'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_nextcloud",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.crs_exclusions_wordpress'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_wordpress",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.crs_exclusions_xenforo'] = {
    "id": "900130",
    "name": "tx.crs_exclusions_xenforo",
    "description": "Modify and uncomment this rule to select which application:",
    "type": "bool",
    "value": "1",
    "help": "Modify and uncomment this rule to select which application:"
}
setvar['tx.allowed_methods'] = {
    "id": "900200",
    "name": "tx.allowed_methods",
    "description": "HTTP methods that a client is allowed to use.",
    "type": "str",
    "value": "GET HEAD POST OPTIONS",
    "help": "HTTP methods that a client is allowed to use.\nDefault: GET HEAD POST OPTIONS\nExample: for RESTful APIs, add the following methods: PUT PATCH DELETE\nExample: for WebDAV, add the following methods: CHECKOUT COPY DELETE LOCK\nMERGE MKACTIVITY MKCOL MOVE PROPFIND PROPPATCH PUT UNLOCK\nUncomment this rule to change the default."
}
setvar['tx.allowed_request_content_type'] = {
    "id": "900220",
    "name": "tx.allowed_request_content_type",
    "description": "Content-Types that a client is allowed to send in a request.",
    "type": "text",
    "value": "application/x-www-form-urlencoded|multipart/form-data|text/xml|application/xml|application/soap+xml|application/x-amf|application/json|application/octet-stream|application/csp-report|application/xss-auditor-report|text/plain",
    "help": "Content-Types that a client is allowed to send in a request.\nDefault: application/x-www-form-urlencoded|multipart/form-data|text/xml|\\\napplication/xml|application/soap+xml|application/x-amf|application/json|\\\napplication/octet-stream|application/csp-report|\\\napplication/xss-auditor-report|text/plain\nUncomment this rule to change the default."
}
setvar['tx.allowed_http_versions'] = {
    "id": "900230",
    "name": "tx.allowed_http_versions",
    "description": "Allowed HTTP versions.",
    "type": "str",
    "value": "HTTP/1.0 HTTP/1.1 HTTP/2 HTTP/2.0",
    "help": "Allowed HTTP versions.\nDefault: HTTP/1.0 HTTP/1.1 HTTP/2 HTTP/2.0\nExample for legacy clients: HTTP/0.9 HTTP/1.0 HTTP/1.1 HTTP/2 HTTP/2.0\nNote that some web server versions use 'HTTP/2', some 'HTTP/2.0', so\nwe include both version strings by default.\nUncomment this rule to change the default."
}
setvar['tx.restricted_extensions'] = {
    "id": "900240",
    "name": "tx.restricted_extensions",
    "description": "Forbidden file extensions.",
    "type": "text",
    "value": ".asa/ .asax/ .ascx/ .axd/ .backup/ .bak/ .bat/ .cdx/ .cer/ .cfg/ .cmd/ .com/ .config/ .conf/ .cs/ .csproj/ .csr/ .dat/ .db/ .dbf/ .dll/ .dos/ .htr/ .htw/ .ida/ .idc/ .idq/ .inc/ .ini/ .key/ .licx/ .lnk/ .log/ .mdb/ .old/ .pass/ .pdb/ .pol/ .printer/ .pwd/ .rdb/ .resources/ .resx/ .sql/ .swp/ .sys/ .vb/ .vbs/ .vbproj/ .vsdisco/ .webinfo/ .xsd/ .xsx/",
    "help": "Forbidden file extensions.\nGuards against unintended exposure of development/configuration files.\nDefault: .asa/ .asax/ .ascx/ .axd/ .backup/ .bak/ .bat/ .cdx/ .cer/ .cfg/ .cmd/ .com/ .config/ .conf/ .cs/ .csproj/ .csr/ .dat/ .db/ .dbf/ .dll/ .dos/ .htr/ .htw/ .ida/ .idc/ .idq/ .inc/ .ini/ .key/ .licx/ .lnk/ .log/ .mdb/ .old/ .pass/ .pdb/ .pol/ .printer/ .pwd/ .rdb/ .resources/ .resx/ .sql/ .swp/ .sys/ .vb/ .vbs/ .vbproj/ .vsdisco/ .webinfo/ .xsd/ .xsx/\nExample: .bak/ .config/ .conf/ .db/ .ini/ .log/ .old/ .pass/ .pdb/ .rdb/ .sql/\nUncomment this rule to change the default."
}
setvar['tx.restricted_headers'] = {
    "id": "900250",
    "name": "tx.restricted_headers",
    "description": "Forbidden request headers.",
    "type": "text",
    "value": "/proxy/ /lock-token/ /content-range/ /translate/ /if/",
    "help": "Forbidden request headers.\nHeader names should be lowercase, enclosed by /slashes/ as delimiters.\nBlocking Proxy header prevents 'httpoxy' vulnerability: https://httpoxy.org\nDefault: /proxy/ /lock-token/ /content-range/ /translate/ /if/\nUncomment this rule to change the default."
}
setvar['tx.static_extensions'] = {
    "id": "900260",
    "name": "tx.static_extensions",
    "description": "File extensions considered static files.",
    "type": "text",
    "value": "/.jpg/ /.jpeg/ /.png/ /.gif/ /.js/ /.css/ /.ico/ /.svg/ /.webp/",
    "help": "File extensions considered static files.\nExtensions include the dot, lowercase, enclosed by /slashes/ as delimiters.\nUsed in DoS protection rule. See section \"Anti-Automation / DoS Protection\".\nDefault: /.jpg/ /.jpeg/ /.png/ /.gif/ /.js/ /.css/ /.ico/ /.svg/ /.webp/\nUncomment this rule to change the default."
}
setvar['tx.allowed_request_content_type_charset'] = {
    "id": "900280",
    "name": "tx.allowed_request_content_type_charset",
    "description": "Content-Types charsets that a client is allowed to send in a request.",
    "type": "str",
    "value": "utf-8|iso-8859-1|iso-8859-15|windows-1252",
    "help": "Content-Types charsets that a client is allowed to send in a request.\nDefault: utf-8|iso-8859-1|iso-8859-15|windows-1252\nUncomment this rule to change the default.\nUse \"|\" to separate multiple charsets like in the rule defining\ntx.allowed_request_content_type."
}
setvar['tx.max_num_args'] = {
    "id": "900300",
    "name": "tx.max_num_args",
    "description": "Block request if number of arguments is too high",
    "type": "str",
    "value": "255",
    "help": "Block request if number of arguments is too high\nDefault: unlimited\nExample: 255\nUncomment this rule to set a limit."
}
setvar['tx.arg_name_length'] = {
    "id": "900310",
    "name": "tx.arg_name_length",
    "description": "Block request if the length of any argument name is too high",
    "type": "str",
    "value": "100",
    "help": "Block request if the length of any argument name is too high\nDefault: unlimited\nExample: 100\nUncomment this rule to set a limit."
}
setvar['tx.arg_length'] = {
    "id": "900320",
    "name": "tx.arg_length",
    "description": "Block request if the length of any argument value is too high",
    "type": "str",
    "value": "400",
    "help": "Block request if the length of any argument value is too high\nDefault: unlimited\nExample: 400\nUncomment this rule to set a limit."
}
setvar['tx.total_arg_length'] = {
    "id": "900330",
    "name": "tx.total_arg_length",
    "description": "Block request if the total length of all combined arguments is too high",
    "type": "str",
    "value": "64000",
    "help": "Block request if the total length of all combined arguments is too high\nDefault: unlimited\nExample: 64000\nUncomment this rule to set a limit."
}
setvar['tx.max_file_size'] = {
    "id": "900340",
    "name": "tx.max_file_size",
    "description": "Block request if the file size of any individual uploaded file is too high",
    "type": "str",
    "value": "1048576",
    "help": "Block request if the file size of any individual uploaded file is too high\nDefault: unlimited\nExample: 1048576\nUncomment this rule to set a limit."
}
setvar['tx.combined_file_sizes'] = {
    "id": "900350",
    "name": "tx.combined_file_sizes",
    "description": "Block request if the total size of all combined uploaded files is too high",
    "type": "str",
    "value": "1048576",
    "help": "Block request if the total size of all combined uploaded files is too high\nDefault: unlimited\nExample: 1048576\nUncomment this rule to set a limit."
}
setvar['tx.sampling_percentage'] = {
    "id": "900400",
    "name": "tx.sampling_percentage",
    "description": "Adding the Core Rule Set to an existing productive site can lead to false",
    "type": "str",
    "value": "100",
    "help": "Adding the Core Rule Set to an existing productive site can lead to false\npositives, unexpected performance issues and other undesired side effects.\nIt can be beneficial to test the water first by enabling the CRS for a\nlimited number of requests only and then, when you have solved the issues (if\nany) and you have confidence in the setup, to raise the ratio of requests\nbeing sent into the ruleset.\nAdjust the percentage of requests that are funnelled into the Core Rules by\nsetting TX.sampling_percentage below. The default is 100, meaning that every\nrequest gets checked by the CRS.  The selection of requests, which are going\nto be checked, is based on a pseudo random number generated by ModSecurity.\nIf a request is allowed to pass without being checked by the CRS, there is no\nentry in the audit log (for performance reasons), but an error log entry is\nwritten.  If you want to disable the error log entry, then issue the\nfollowing directive somewhere after the inclusion of the CRS\n(E.g., RESPONSE-999-EXCEPTIONS.conf).\nSecRuleUpdateActionById 901150 \"nolog\"\nATTENTION: If this TX.sampling_percentage is below 100, then some of the\nrequests will bypass the Core Rules completely and you lose the ability to\nprotect your service with ModSecurity.\nUncomment this rule to enable this feature:"
}
setvar['tx.block_search_ip'] = {
    "id": "900500",
    "name": "tx.block_search_ip",
    "description": "Optionally, you can check the client IP address against the Project Honey Pot",
    "type": "bool",
    "value": "1",
    "help": "Optionally, you can check the client IP address against the Project Honey Pot\nHTTPBL (dnsbl.httpbl.org). In order to use this, you need to register to get a\nfree API key. Set it here with SecHttpBlKey.\nProject Honeypot returns multiple different malicious IP types.\nYou may specify which you want to block by enabling or disabling them below.\nRef: https://www.projecthoneypot.org/httpbl.php\nRef: https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#wiki-SecHttpBlKey\nUncomment these rules to use this feature:\n#SecHttpBlKey XXXXXXXXXXXXXXXXX"
}
setvar['tx.block_suspicious_ip'] = {
    "id": "900500",
    "name": "tx.block_suspicious_ip",
    "description": "Optionally, you can check the client IP address against the Project Honey Pot",
    "type": "bool",
    "value": "1",
    "help": "Optionally, you can check the client IP address against the Project Honey Pot\nHTTPBL (dnsbl.httpbl.org). In order to use this, you need to register to get a\nfree API key. Set it here with SecHttpBlKey.\nProject Honeypot returns multiple different malicious IP types.\nYou may specify which you want to block by enabling or disabling them below.\nRef: https://www.projecthoneypot.org/httpbl.php\nRef: https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#wiki-SecHttpBlKey\nUncomment these rules to use this feature:\n#SecHttpBlKey XXXXXXXXXXXXXXXXX"
}
setvar['tx.block_harvester_ip'] = {
    "id": "900500",
    "name": "tx.block_harvester_ip",
    "description": "Optionally, you can check the client IP address against the Project Honey Pot",
    "type": "bool",
    "value": "1",
    "help": "Optionally, you can check the client IP address against the Project Honey Pot\nHTTPBL (dnsbl.httpbl.org). In order to use this, you need to register to get a\nfree API key. Set it here with SecHttpBlKey.\nProject Honeypot returns multiple different malicious IP types.\nYou may specify which you want to block by enabling or disabling them below.\nRef: https://www.projecthoneypot.org/httpbl.php\nRef: https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#wiki-SecHttpBlKey\nUncomment these rules to use this feature:\n#SecHttpBlKey XXXXXXXXXXXXXXXXX"
}
setvar['tx.block_spammer_ip'] = {
    "id": "900500",
    "name": "tx.block_spammer_ip",
    "description": "Optionally, you can check the client IP address against the Project Honey Pot",
    "type": "bool",
    "value": "1",
    "help": "Optionally, you can check the client IP address against the Project Honey Pot\nHTTPBL (dnsbl.httpbl.org). In order to use this, you need to register to get a\nfree API key. Set it here with SecHttpBlKey.\nProject Honeypot returns multiple different malicious IP types.\nYou may specify which you want to block by enabling or disabling them below.\nRef: https://www.projecthoneypot.org/httpbl.php\nRef: https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual#wiki-SecHttpBlKey\nUncomment these rules to use this feature:\n#SecHttpBlKey XXXXXXXXXXXXXXXXX"
}
setvar['tx.dos_burst_time_slice'] = {
    "id": "900700",
    "name": "tx.dos_burst_time_slice",
    "description": "Optional DoS protection against clients making requests too quickly.",
    "type": "str",
    "value": "60",
    "help": "Optional DoS protection against clients making requests too quickly.\nWhen a client is making more than 100 requests (excluding static files) within\n60 seconds, this is considered a 'burst'. After two bursts, the client is\nblocked for 600 seconds.\nRequests to static files are not counted towards DoS; they are listed in the\n'tx.static_extensions' setting, which you can change in this file (see\nsection \"HTTP Policy Settings\").\nFor a detailed description, see rule file REQUEST-912-DOS-PROTECTION.conf.\nUncomment this rule to use this feature:"
}
setvar['tx.dos_counter_threshold'] = {
    "id": "900700",
    "name": "tx.dos_counter_threshold",
    "description": "Optional DoS protection against clients making requests too quickly.",
    "type": "str",
    "value": "100",
    "help": "Optional DoS protection against clients making requests too quickly.\nWhen a client is making more than 100 requests (excluding static files) within\n60 seconds, this is considered a 'burst'. After two bursts, the client is\nblocked for 600 seconds.\nRequests to static files are not counted towards DoS; they are listed in the\n'tx.static_extensions' setting, which you can change in this file (see\nsection \"HTTP Policy Settings\").\nFor a detailed description, see rule file REQUEST-912-DOS-PROTECTION.conf.\nUncomment this rule to use this feature:"
}
setvar['tx.dos_block_timeout'] = {
    "id": "900700",
    "name": "tx.dos_block_timeout",
    "description": "Optional DoS protection against clients making requests too quickly.",
    "type": "str",
    "value": "600",
    "help": "Optional DoS protection against clients making requests too quickly.\nWhen a client is making more than 100 requests (excluding static files) within\n60 seconds, this is considered a 'burst'. After two bursts, the client is\nblocked for 600 seconds.\nRequests to static files are not counted towards DoS; they are listed in the\n'tx.static_extensions' setting, which you can change in this file (see\nsection \"HTTP Policy Settings\").\nFor a detailed description, see rule file REQUEST-912-DOS-PROTECTION.conf.\nUncomment this rule to use this feature:"
}
setvar['tx.crs_validate_utf8_encoding'] = {
    "id": "900950",
    "name": "tx.crs_validate_utf8_encoding",
    "description": "The CRS can optionally check request contents for invalid UTF-8 encoding.",
    "type": "bool",
    "value": "1",
    "help": "The CRS can optionally check request contents for invalid UTF-8 encoding.\nWe only want to apply this check if UTF-8 encoding is actually used by the\nsite; otherwise it will result in false positives.\nUncomment this rule to use this feature:"
}
setvar['tx.do_reput_block'] = {
    "id": "900960",
    "name": "tx.do_reput_block",
    "description": "Blocking based on reputation is permanent in the CRS. Unlike other rules,",
    "type": "bool",
    "value": "1",
    "help": "Blocking based on reputation is permanent in the CRS. Unlike other rules,\nwhich look at the indvidual request, the blocking of IPs is based on\na persistent record in the IP collection, which remains active for a\ncertain amount of time.\nThere are two ways an individual client can become flagged for blocking:\n- External information (RBL, GeoIP, etc.)\n- Internal information (Core Rules)\nThe record in the IP collection carries a flag, which tags requests from\nindividual clients with a flag named IP.reput_block_flag.\nBut the flag alone is not enough to have a client blocked. There is also\na global switch named tx.do_reput_block. This is off by default. If you set\nit to 1 (=On), requests from clients with the IP.reput_block_flag will\nbe blocked for a certain duration.\nVariables\nip.reput_block_flag      Blocking flag for the IP collection record\nip.reput_block_reason    Reason (= rule message) that caused to blocking flag\ntx.do_reput_block        Switch deciding if we really block based on flag\ntx.reput_block_duration  Setting to define the duration of a block\nIt may be important to know, that all the other core rules are skipped for\nrequests, when it is clear that they carry the blocking flag in question.\nUncomment this rule to use this feature:"
}
setvar['tx.reput_block_duration'] = {
    "id": "900970",
    "name": "tx.reput_block_duration",
    "description": "Uncomment this rule to change the blocking time:",
    "type": "str",
    "value": "300",
    "help": "Uncomment this rule to change the blocking time:\nDefault: 300 (5 minutes)"
}


#-- group
def mk_groups():
    plugins = {}
    groups = [
        ["global", "module", "CoreRuleSet variables", "Update CRS setvars in\n", "^id|^fn|tx\.paranoia|executing|sampling|score_threshold"],
        ["allow", "allowdeny", "Allowed/Restricted", "White and blacklist some HTTP parameters", "allowed|restricted|urlencoded|static_ext"],
        ["args", "args", "Arguments", "GET and POST parameter restrictions", "args|arg_|file_size|utf8"],
        ["excl", "exclusion", "Exclusions", "Some rules to skip (this should have been tags, but here we are)", "exclusions"],
        ["class", "classification", "Paranoia level classification", "Assign default levels", "anomaly_score(?!_threshold$)"],
        ["else", "setvar:else", "Other flags", "RBL blocking and DOS protection", "-"]
    ]
    """
        "name": "tx.block_search_ip",
        "name": "tx.block_suspicious_ip",
        "name": "tx.block_harvester_ip",
        "name": "tx.block_spammer_ip",
        "name": "tx.dos_burst_time_slice",
        "name": "tx.dos_counter_threshold",
        "name": "tx.dos_block_timeout",
        "name": "tx.do_reput_block",
        "name": "tx.reput_block_duration",
        "name": "tx.crs_setup_version",
    """

    groups[-1][-1] = "^(?!.*(" + ("|".join([d[4] for d in groups])) + "))"  # "else" gets opposite of other regexps
    for grp, cat, title, desc, rx in groups:
        plugins[grp] = {
            "id": grp,
            "api": "mod_security",
            "title": title,
            "description": desc,
            "version": "3.x.x",
            "type": "config",
            "category": cat,
            "config": [o for o in setvar.values() if re.search(rx, o["name"])]
        }
    return plugins


def find_crs_version():
    for id,r in vhosts.rules.items():
        v = r.setvar.get("tx.crs_setup_version")
        if v:
            return re.sub("(?<=\d)(?=\d)", ".", v)
    else:
        return "3.x"

def window(confn):

    # prepare config list
    plugins = mk_groups()
    setvar["id"]["value"] = "5999" if not re.search("crs/crs-setup", confn) else "900999"
    setvar["fn"]["value"] = confn
    setvar["fn"]["select"] = {v:v for v in vhosts.list_vhosts()}
    plugins["global"]["description"] += confn
    plugins["global"]["version"] = find_crs_version()
    plugin_states = {k:1 for k in plugins.keys()}
    
    # add declared options, if any
    pmd = pluginconf.plugin_meta(fn=srvroot.fn(confn))
    if pmd.get("title") and pmd.get("config") and pmd.get("type")=="config":
        plugins[pmd["id"]] = pmd

    # read config variables directly from file (using vhosts would be more work, since .ruledecl and .rules{} had to be searched for .setvar)
    conf = {}
    if srvroot.exists(confn):
        conf = read_setvars(confn)
    # unset defaults
    if not utils.conf.get("crsopt_defaults"):
        for k,c in setvar.items():
            if k in conf or k in ("id", "fn"):
                continue
            elif c["type"] == "bool":
                conf[k] = 0
            else:
                conf[k] = ""
    prev = copy.copy(conf)

    # show
    save = pluginconf.gui.window(
        conf, plugin_states, files=[], plugins=plugins,
        title="mod_security option directives", icon=icons.crs,
        opt_label=True, size=(710,770)
    )
    if not save:
        return
        
    # id,fn
    id = int(conf["id"])
    confn = conf["fn"]
    del conf["id"], conf["fn"]
    
    # combine into SecRule
    act = []
    rem_id = []
    for k,v in conf.items():
        #print(k, " := ", repr(v), type(v), repr(prev.get(k)), type(prev.get(k)))
        if v in (None, "\n", "", prev.get(k)):
            continue
        elif type(v) is bool:
            v = "1" if v else "0"
        if re.search("^\\w+$", v):
            act.append(f"setvar:{k}={v}")
        else:
            act.append(f"setvar:'{k}={v.strip()}'")
        if utils.conf.get("crsopt_undefine") and id < 100000 and setvar.get(k,{}).get("id") and setvar[k]['id'] not in rem_id:
            act.append(f"   ctl:ruleRemoveById={setvar[k]['id']}")
            rem_id.append(setvar[k]['id'])
    act = ", \\\n    ".join(act)
    secrule = f"""SecAction "id:{id},pass,nolog,noauditlog,t:none, \\\n    {act}"\n"""
    print(secrule)
    
    # prepare update
    replace_rx = re.compile(f"""     # just ↓ in case user picks a different secrule id
        ^[\ \t]*   SecAction   \s+   \"id:({id}|5999|900999),[^"]+\"   .*\\n
    """, re.X|re.M)

    # redirect to *.preconf if ctl:ruleRemove mentioned
    confn = writer.fn_preconf(fn=confn, addsrc=str(secrule))
    writer.update_or_add(confn, {replace_rx:secrule})


# rescan a *.conf file just for setvar:
def read_setvars(fn):
    src = srvroot.read(fn)
    r = {}
    rx = re.compile("""
        ^\s*SecAction\s+\"([^\"]+)\"
    """, re.X|re.M|re.I)
    rx2 = re.compile("""
        setvar:\'?([\w\-\.]+)=([^\'\,]+)\'?
    """, re.X)
    for secaction in rx.findall(src):
        for var,val in rx2.findall(secaction):
            r[var] = val
    return r

