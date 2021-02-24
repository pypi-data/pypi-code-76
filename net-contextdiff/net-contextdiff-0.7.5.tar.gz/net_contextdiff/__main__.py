# contextdiff.__main__


# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>
#
# This script compares Cisco IOS configuration files and outputs a
# configuration file which will convert the former into the latter.



import net_contextdiff

import argparse
import re
import sys

from net_contextdiff.configrules import ConfigElementRules
from net_contextdiff.iosparser import CiscoIOSConfigParser
from net_contextdiff.iosdiff import CiscoIOSConfigDiff



# --- constants ---



# PLATFORMS = dict
#
# This dictionary specifies the available platforms available to compare
# configurations in.  The dictionary is keyed on the user-specified platform
# name and specifies two values in a tuple, giving the object classes to be
# used for that platform: the first is the parser an the second is the
# difference comparator.

PLATFORMS = {
    "ios": (CiscoIOSConfigParser, CiscoIOSConfigDiff)
}



# --- command line arguments ---



# create the parser and add in the available command line options

parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a module
    # directory will use '__main__' by default - this name isn't necessarily
    # correct, but it looks better than that
    prog="cfg-contextdiff",

    # we want the epilog help output to be printed as it and not reformatted or
    # line wrapped
    formatter_class=argparse.RawDescriptionHelpFormatter,

    epilog="""\
Rules are added using the '-r' and '-R'. options.  Each rule is specified in
string form in the format '[!][{+-=}][<area>][:<id>]':

* a leading '!' (or not) specifies the action for this rule: a '!' indicates
  the rule should exclude matching elements; if the character is omitted, they
  should be included

* next (or first, if '!' is not specified) indicates the 'action' being
  matched:

    '+' - add/create/set actions,,
    '-' - remove/delete/unset actions, and
    '=' - update actions (changing an already-set value for another)

The list of rules starts empty, with the default case being to include the
element.

The '-e' option is useful for displaying the rules which would match included
difference output.
""")


parser.add_argument(
    "-r", "--rules",
    dest="rules_items",
    nargs="+",
    help="add rule(s) to include or exclude specified element(s) of the "
         "configuration (will be added before the rules read from a file "
         "with the -R option, if both used)")

parser.add_argument(
    "-R", "--rules-filename",
    dest="rules_filename",
    help="read rules from file")

parser.add_argument(
    "-e", "--explain-includes",
    dest="explain_includes",
    action="store_true",
    help="explain which rule includes a configuration element")

parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="when generating configuration for multiple devices, don't print the "
         "name of each device, as it's generated")

parser.add_argument(
    "-D", "--debug",
    action="store_true",
    help="enable debugging of contextual parsing")

parser.add_argument(
    "platform",
    choices=PLATFORMS,
    help="platform used for configuration files")

parser.add_argument(
    "from_filename",
    metavar="from",
    help="initial ('from') configuration file; '%%' can be used to substitute "
         "in the name of the device into the filename")

parser.add_argument(
    "to_filename",
    metavar="to",
    help="destination ('to') configuration file; '%%' can be used to "
         "substitute in the name of the device into the filename")

parser.add_argument(
    "output_filename",
    nargs="?",
    metavar="output",
    help="write differences configuration to named file instead of stdout; "
         "'%%' can be used to substitute in the name of the device into the "
         "filename")

parser.add_argument(
    "devicenames",
    metavar="devicename",
    nargs="*",
    help="name(s) of the device(s) to calculate differences in the "
         "configuration for")

parser.add_argument(
    "--version",
    action="version",
    version=("%(prog)s " + net_contextdiff.__version__))



# parse the supplied command line against these options, storing the results

args = parser.parse_args()

config_parser_class, config_diff_class = PLATFORMS[args.platform]

rules_items = args.rules_items
rules_filename = args.rules_filename
explain_includes = args.explain_includes
quiet = args.quiet
debug = args.debug
from_filename = args.from_filename
to_filename = args.to_filename
output_filename = args.output_filename
devicenames = args.devicenames



# read the rules for what to include/exclude in the comparison

rules = ConfigElementRules()

if rules_items:
    # add the rules specified directly on the command line (do this
    # before reading those from a file, if specified, below)
    rules.add_rules(rules_items)

if rules_filename:
    rules.read_rules(rules_filename)



# check a couple of nonsensical configurations aren't being use related to
# multiple devices

if len(devicenames) == 0:
    if from_filename.find("%") != -1:
        print("warning: no device names specified, so operating on a single "
              "file, yet 'from' filename has '%' character - no substitution "
              "will be performed",

              file=sys.stderr)

    if to_filename.find("%") != -1:
        print("warning: no device names specified, so operating on a single "
              "file, yet 'to' filename has '%' character - no substitution "
              "will be performed",

              file=sys.stderr)

    if output_filename and (output_filename.find("%") != -1):
        print("warning: no device names specified, so operating on a single "
              "file, yet 'output' filename has '%' character - no "
              "substitution will be performed",

              file=sys.stderr)


elif len(devicenames) > 1:
    if from_filename.find("%") == -1:
        print("warning: multiple device names specified but 'from' filename "
              "does not contain '%' - same file will be read",

              file=sys.stderr)

    if to_filename.find("%") == -1:
        print("warning: multiple device names specified but 'to' filename "
              "does not contain '%' - same file will be read",

              file=sys.stderr)


    if not output_filename:
        print("warning: multiple device names specified but outputting to "
              "standard output - all configurations will be concatenated",

              file=sys.stderr)

    elif output_filename.find("%") == -1:
        print("error: multiple device names specified but 'output' filename "
              "does not contain '%' - same file would be overwritten",

              file=sys.stderr)

        exit(1)



# --- compare ---



def diffconfig(from_filename, to_filename, output_filename=None):
    """This function compares the 'from' and 'to' configurations for
    the specified device and writes a difference configuration file
    (one that transforms the configuration of a running device from the
    'from' to the 'to' state).

    The filenames for the configuration files, as well as the output
    are taken from the arguments parsed above and stored in global
    variables used directly by this function.

    The function returns True iff the parsing and comparison succeeded.
    Most problems result in the function aborting with an exception,
    but some minor warnings may be ignored and the program continue
    with devices.
    """

    # this function makes use of global variables defined outside it so
    # must appear here in the code


    # create configuration parsing objects and read in 'from' and 'to' configs

    from_cfg = config_parser_class()
    from_cfg.parse_file(from_filename, debug)

    to_cfg = config_parser_class()
    to_cfg.parse_file(to_filename, debug)


    # compare the two configurations

    diff = config_diff_class(rules, explain_includes)

    diff.diff_configs(from_cfg.get_config(), to_cfg.get_config())


    # if there were differences, print them

    diffs = diff.get_diffs()

    if output_filename:
        if debug:
            print("debug: writing to output file: %s" % output_filename,
                  file=sys.stderr)

        with open(output_filename, "w") as output_file:
            if diffs:
                print(diffs, file=output_file)

    else:
        if debug:
            print("debug: writing to standard output", file=sys.stderr)

        if diffs:
            print(diffs)


    return True



# this flag will change to False if any configuration fails to generate and
# is used to affect the return code from the script

complete_success = True


if devicenames:
    for devicename in devicenames:
        if not quiet:
            print(devicename)

        complete_success = diffconfig(
                               from_filename.replace("%", devicename),
                               to_filename.replace("%", devicename),
                               output_filename.replace("%", devicename))


else:
    complete_success = diffconfig(from_filename, to_filename, output_filename)


exit(0 if complete_success else 1)
