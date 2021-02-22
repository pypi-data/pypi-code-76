# -*- coding: utf-8 -*-

# Simple Type Data
INTEGER_VALUE = "([+|-]?\\d+)"
FLOAT_VALUE = "([+-]?\\d+\\.?\\d+)"
HEX_VALUE = "([0-9abcdefABCDEF]+)"
NOSPACE_VALUE = "([^\\s]+)"

# Special Type Data
VERSION_VALUE = "(\\d+(\\.\\d+){0,3})"
FQDN_VALUE = "([a-zA-Z\\d-]+(\\.[a-zA-Z\\d-]+)*)"
ABSOLUTE_PATH_VALUE = "((\\/[^/]+)+\\/?)"
OID_VALUE = "(\\d+(\\.\\d+)*)"
IPV4SEG  = "(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])"
IPV4ADDR = "(({IPV4SEG}\.){{3,3}}{IPV4SEG})".format(IPV4SEG=IPV4SEG)
IPV6SEG = "([0-9a-fA-F]{1,4})"
IPV6ADDR = """(
    ({IPV6SEG}:){{7,7}}{IPV6SEG}|
    ({IPV6SEG}:){{1,7}}:|
    ({IPV6SEG}:){{1,6}}:{IPV6SEG}|
    ({IPV6SEG}:){{1,5}}(:{IPV6SEG}){{1,2}}|
    ({IPV6SEG}:){{1,4}}(:{IPV6SEG}){{1,3}}|
    ({IPV6SEG}:){{1,3}}(:{IPV6SEG}){{1,4}}|
    ({IPV6SEG}:){{1,2}}(:{IPV6SEG}){{1,5}}|
    {IPV6SEG}:((:{IPV6SEG}){{1,6}})|
    :((:{IPV6SEG}){{1,7}}|:)|
    fe80:(:{IPV6SEG}){{0,4}}%[0-9a-zA-Z]{{1,}}|
    ::(ffff(:0{{1,4}}){{0,1}}:){{0,1}}{IPV4ADDR}|
    ({IPV6SEG}:){{1,4}}:{IPV4ADDR}
    )""".format(IPV6SEG=IPV6SEG, IPV4ADDR=IPV4ADDR).replace(" ", "").replace("\r", "").replace("\n", "")
IPV4 = IPV4ADDR
IPV4_VALUE = IPV4
IPV6 = IPV6ADDR
IPV6_VALUE = IPV6
IP_VALUE = "({IPV4ADDR}|{IPV6ADDR})".format(IPV4ADDR=IPV4ADDR, IPV6ADDR=IPV6ADDR)
IP_ADDR = IP_VALUE

LISTENING_PORT = "(\\d{1,5})"
IPV4_SERVICE = "({IPV4}:{LISTENING_PORT})".format(IPV4=IPV4, LISTENING_PORT=LISTENING_PORT)

IP = "(?P<ip>{IP_VALUE})".format(IP_VALUE=IP_VALUE)

# Datetime
YEAR_VALUE = "(\\d{4})"
MONTH_VALUE = "(\\d{2})"
DAY_VALUE = "(\\d{2})"
HOUR_VALUE = "(\\d{2})"
MINUTE_VALUE = "(\\d{2})"
SECOND_VALUE = "(\\d{2})"
MICROSECOND_VALUE = "(\\d{6})"
NANOSECOND_VALUE = "(\\d{9})"
MONTH_SHORT_NAME_VALUE = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
DATE_SIMPLE_VALUE = "({YEAR_VALUE}{MONTH_VALUE}{DAY_VALUE})".format(YEAR_VALUE=YEAR_VALUE, MONTH_VALUE=MONTH_VALUE, DAY_VALUE=DAY_VALUE)
DATE_VALUE = "({YEAR_VALUE}-{MONTH_VALUE}-{DAY_VALUE})".format(YEAR_VALUE=YEAR_VALUE, MONTH_VALUE=MONTH_VALUE, DAY_VALUE=DAY_VALUE)
DATE_DMY_VALUE = "({DAY_VALUE}/{MONTH_SHORT_NAME_VALUE}/{YEAR_VALUE})".format(DAY_VALUE=DAY_VALUE, MONTH_SHORT_NAME_VALUE=MONTH_SHORT_NAME_VALUE, YEAR_VALUE=YEAR_VALUE)
DATE_YMD_VALUE = "{YEAR_VALUE}-{MONTH_VALUE}-{DAY_VALUE}".format(YEAR_VALUE=YEAR_VALUE, MONTH_VALUE=MONTH_VALUE, DAY_VALUE=DAY_VALUE)
TIME_SIMPLE_VALUE = "({HOUR_VALUE}{MINUTE_VALUE}{SECOND_VALUE})".format(HOUR_VALUE=HOUR_VALUE, MINUTE_VALUE=MINUTE_VALUE, SECOND_VALUE=SECOND_VALUE)
TIME_VALUE = "({HOUR_VALUE}:{MINUTE_VALUE}:{SECOND_VALUE})".format(HOUR_VALUE=HOUR_VALUE, MINUTE_VALUE=MINUTE_VALUE, SECOND_VALUE=SECOND_VALUE)
DATETIME_SIMPLE_VALUE = "({DATE_SIMPLE_VALUE}{TIME_SIMPLE_VALUE})".format(DATE_SIMPLE_VALUE=DATE_SIMPLE_VALUE, TIME_SIMPLE_VALUE=TIME_SIMPLE_VALUE)
DATETIME_VALUE = "({DATE_VALUE} {TIME_VALUE})".format(DATE_VALUE=DATE_VALUE, TIME_VALUE=TIME_VALUE)
TIMEZONE_VALUE = "([+|-]\\d{2}:?\\d{2})"

# Parameters
QUOTED_RAW_VALUE = "((\\\\\\\"|[^\\\"])*)"
QUOTED_VALUE = "(\"?{QUOTED_RAW_VALUE}\"?)".format(QUOTED_RAW_VALUE=QUOTED_RAW_VALUE)
NAME_VALUE = "([a-zA-Z_][a-zA-Z0-9-_]*)"
OPTION = "({NAME_VALUE}={QUOTED_VALUE})".format(NAME_VALUE=NAME_VALUE, QUOTED_VALUE=QUOTED_VALUE)

# Datetime with named groups
YEAR = "(?P<year>{YEAR_VALUE})".format(YEAR_VALUE=YEAR_VALUE)
MONTH = "(?P<month>{MONTH_VALUE})".format(MONTH_VALUE=MONTH_VALUE)
MONTH_SHORT_NAME = "(?P<month_short_name>{MONTH_SHORT_NAME_VALUE})".format(MONTH_SHORT_NAME_VALUE=MONTH_SHORT_NAME_VALUE)
DAY = "(?P<day>{DAY_VALUE})".format(DAY_VALUE=DAY_VALUE)
HOUR = "(?P<hour>{HOUR_VALUE})".format(HOUR_VALUE=HOUR_VALUE)
MINUTE = "(?P<minute>{MINUTE_VALUE})".format(MINUTE_VALUE=MINUTE_VALUE)
SECOND = "(?P<second>{SECOND_VALUE})".format(SECOND_VALUE=SECOND_VALUE)
MICROSECOND = "(?P<microsecond>{MICROSECOND_VALUE})".format(MICROSECOND_VALUE=MICROSECOND_VALUE)
NANOSECOND = "(?P<nanosecond>{NANOSECOND_VALUE})".format(NANOSECOND_VALUE=NANOSECOND_VALUE)
DATE_SIMPLE = "(?P<date_simple>{YEAR}{MONTH}{DAY})".format(YEAR=YEAR, MONTH=MONTH, DAY=DAY)
DATE = "(?P<date>{YEAR}-{MONTH}-{DAY})".format(YEAR=YEAR, MONTH=MONTH, DAY=DAY)
DATE_DMY = "(?P<date_dmy>{DAY}/{MONTH_SHORT_NAME}/{YEAR})".format(YEAR=YEAR, MONTH_SHORT_NAME=MONTH_SHORT_NAME, DAY=DAY)
DATE_YMD = "(?P<date_ymd>{YEAR}-{MONTH}-{DAY})".format(YEAR=YEAR, MONTH=MONTH, DAY=DAY)
TIME_SIMPLE = "(?P<time_simple>{HOUR}{MINUTE}{SECOND})".format(HOUR=HOUR, MINUTE=MINUTE, SECOND=SECOND)
TIME = "(?P<time>{HOUR}:{MINUTE}:{SECOND})".format(HOUR=HOUR, MINUTE=MINUTE, SECOND=SECOND)
DATETIME_SIMPLE = "(?P<datetime_simple>{DATE_SIMPLE}{TIME_SIMPLE})".format(DATE_SIMPLE=DATE_SIMPLE, TIME_SIMPLE=TIME_SIMPLE)
DATETIME = "(?P<datetime>{DATE} {TIME})".format(DATE=DATE, TIME=TIME)
TIMEZONE = "(?P<timezone>(?P<timezone_flag>[+|-])(?P<timezone_hour>\\d{2}):?(?P<timezone_minute>\\d{2}))"
ISO_FORMAT_TIME_VALUE = "({DAY_VALUE}/{MONTH_SHORT_NAME_VALUE}/{YEAR_VALUE}:{HOUR_VALUE}:{MINUTE_VALUE}:{SECOND_VALUE} {TIMEZONE})".format(
    DAY_VALUE=DAY_VALUE,
    MONTH_SHORT_NAME_VALUE=MONTH_SHORT_NAME_VALUE,
    YEAR_VALUE=YEAR_VALUE,
    HOUR_VALUE=HOUR_VALUE,
    MINUTE_VALUE=MINUTE_VALUE,
    SECOND_VALUE=SECOND_VALUE,
    TIMEZONE=TIMEZONE,
    )
ISO_FORMAT_TIME_WITH_MICROSECOND_VALUE = "({DAY_VALUE}/{MONTH_SHORT_NAME_VALUE}/{YEAR_VALUE}:{HOUR_VALUE}:{MINUTE_VALUE}:{SECOND_VALUE}(\\.{MICROSECOND_VALUE})? {TIMEZONE})".format(
    DAY_VALUE=DAY_VALUE,
    MONTH_SHORT_NAME_VALUE=MONTH_SHORT_NAME_VALUE,
    YEAR_VALUE=YEAR_VALUE,
    HOUR_VALUE=HOUR_VALUE,
    MINUTE_VALUE=MINUTE_VALUE,
    SECOND_VALUE=SECOND_VALUE,
    MICROSECOND_VALUE=MICROSECOND_VALUE,
    TIMEZONE=TIMEZONE,
    )
ISO_FORMAT_TIME = "((?P<datetime>{DATE_DMY}:{TIME} {TIMEZONE}))".format(
    DATE_DMY=DATE_DMY,
    TIME=TIME,
    TIMEZONE=TIMEZONE,
    )
ISO_FORMAT_TIME_WITH_MICROSECOND = "((?P<datetime>{DATE_DMY}:{TIME}\\.{MICROSECOND} {TIMEZONE}))".format(
    DATE_DMY=DATE_DMY,
    TIME=TIME,
    MICROSECOND=MICROSECOND,
    TIMEZONE=TIMEZONE,
    )
ISO_FORMAT_TIME_WITH_NANOSECOND = "((?P<datetime>{DATE_DMY}:{TIME}\\.{NANOSECOND} {TIMEZONE}))".format(
    DATE_DMY=DATE_DMY,
    TIME=TIME,
    NANOSECOND=NANOSECOND,
    TIMEZONE=TIMEZONE,
    )
LOG_LEVEL = "(?P<log_level>debug|info|warn|warning|err|error|critical|notice|DEBUG|INFO|NOTICE|WARN|WARNING|ERR|ERROR|CRITICAL)"


# HTTP
HTTP_REQUEST = "(?P<request>(?P<request_method>.+) (?P<request_path>[^\\?]+)(\\?(?P<request_query>.+))? (?P<http_version>.+))"
DEFAULT_NGINX_ACCESS = "(?P<remote_addr>.+) (?P<server_name>.+) (?P<remote_user>.+) \\[(?P<time_local>.+)\\] \\\"{HTTP_REQUEST}\\\" (?P<status>\\d+) (?P<body_bytes_sent>\\d+) \\\"(?P<http_referer>.+)\\\" \\\"(?P<http_user_agent>.+)\\\" \\\"(?P<http_x_forwarded_for>.+)\\\""
SIMPLE_NGINX_ACCESS = "{DEFAULT_NGINX_ACCESS} (?P<upstream_status>.+) (?P<upstream_addr>.+) (?P<request_time>.+) (?P<upstream_response_time>.+) \\\"(?P<request_body>.+)\\\""

# OTHER
MESSAGE = "(?P<message>.*)"


import re
import copy
import string


def get_default_rules():
    """Get default rule sets.
    """
    rules = {}
    _globals = dict(globals())
    for key, value in _globals.items():
        if not key.startswith("_") and key[0] in string.ascii_uppercase:
            rules[key] = value
    return expend_vars(rules)


def expend_vars(vars):
    """Expand with variables.

    Returns
        return expanded vars.

    Raise exception
        If some variable expand failed.
    """
    vars = copy.copy(vars)
    VAR = "(?P<var>\\{[A-Z_][A-Z_0-9]*\\})"
    while True:
        all_expended_flag = True
        for key in vars.keys():
            value = vars[key]
            names = re.findall(VAR, value)
            if names:
                all_expended_flag = False
                vars[key] = value.format(**vars)
        if all_expended_flag:
            break
    return vars

