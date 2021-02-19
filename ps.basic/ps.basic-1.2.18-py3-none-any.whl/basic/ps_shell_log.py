# psf: ta=4, -*-Python-*-, vi: set et ts=4: coding: utf-8
__doc__ = """
ps_shell_log writes strings to the ps logging of the DEV_STAGE.
It should be used from accompanying Programms e.g. shell-scripts to
write logging Messages which will be integrated to the other logging
messages on the correlated DEV_STAGE.

  Usage: ps_shell_log [-v] [ --level=LEVEL ] [ --service_name=name ] \
            [ --have_config_file=true/false]  TEXT ...

  Arguments:
    TEXT  Message to be printed

  Options:
    -h --help             Show this screen.
    -v                    verbose
    --level=LEVEL         LogLevel (DEBUG,INFO,ERROR,WARNING,FATAL)
    --service_name=value   the system_id of the message

"""
import sys

import docopt

from ps.basic import Config
from ps.basic import __version__ as version

SERVICE_NAME = "shell_log"
VERBOSE = False


def main():
    """Add Log to logging stream."""
    global SERVICE_NAME, VERBOSE
    options = docopt.docopt(__doc__, version=version)
    if options["-v"]:
        VERBOSE = True
    if options["--have_config_file"] is not None:
        assert options["--have_config_file"] in ["True", "False"]
        have_config_file = eval(options["--have_config_file"])
    else:
        have_config_file = False
    if options["--level"] is not None:
        level = options["--level"]
    else:
        level = "info"
    if options["--service_name"] is not None:
        SERVICE_NAME = options["--service_name"]

    try:
        the_singleton = Config.Basic(
            SERVICE_NAME, have_config_file=have_config_file
        )

        if VERBOSE:
            the_singleton.verbose()
        exec(
            'Config.logger.%s("%s",extra={"package_version":"%s"})'
            % (level.lower(), options["TEXT"], str(version))
        )
    except Config.ForbiddenInitialisationOfSingleton:
        s = "Exception while calling ps_shell_log"
        sys.stderr.write(s)
        Config.logger.exception(s)
