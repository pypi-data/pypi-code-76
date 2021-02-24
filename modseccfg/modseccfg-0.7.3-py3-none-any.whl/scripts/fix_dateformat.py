#!/usr/bin/env python3
# type: filter
# category: preprocess
# title: fix datetime formats
# description: ISO8601FTW
# priority: hidden
# params: {logfn}
#
# Param can be '-' to use stdin.
#

import sys, os, re, dateutil.parser

# extract and conversion
rx_dt = re.compile("\[([^\]]*\d\d+[^\]]*\d:\d\d[^\]]*)\]")
def cnv(m):
    d = dateutil.parser.parse(m.group(1), fuzzy=True)
    return "[{}]".format(d.isoformat())

# filename
fn = "/dev/stdin"
if len(sys.argv) > 1 and sys.argv[1] != "-":
    fn = sys.argv[1]

# iterate over lines
with open(fn, "r", encoding="utf-8") as f:
    for line in f:
        print(re.sub(rx_dt, cnv, line, 1), end="")

