from .magic import line_magic, arg, LINE_MAGIC
from ..kernel_logger import logger

from iot_device import Config
from termcolor import colored

import logging
import os


@arg('path', nargs="?", default=Config.iot49_dir(), help="New working directory. Default: $IOT49.")
@line_magic
def cd_magic(kernel, args):
    """Change the working directory."""
    os.chdir(args.path)
    kernel.print(os.getcwd())


@arg('-v', '--verbose', action='store_true', help="Show detailed help for each line magic.")
@line_magic
def lsmagic_magic(kernel, args):
    """List all magic functions."""
    if args.verbose:
        for k, v in sorted(LINE_MAGIC.items()):
            if not v[1]: continue
            kernel.print(f"MAGIC %{k} {'-'*(70-len(k))}")
            v[0](kernel, "-h")
            kernel.print("\n")
        return

    kernel.print("Line Magic:    -h shows help (e.g. %discover -h)")
    for k, v in sorted(LINE_MAGIC.items()):
        if not v[1]: continue
        kernel.print("  %{:10s}  {}".format(k, v[1]))
    kernel.print("  {:11s}  {}".format('!', "Pass line to bash shell for evaluation."))
    kernel.print("\nCell Magic:")
    kernel.print("  {:11s}  {}".format('%%host', "Pass cell to host (cPython) for evaluation."))
    kernel.print("  {:11s}  {}".format('%%bash', "Pass cell to the bash shell for evaluation."))
    kernel.print("  {:11s}  {}".format('%%connect', "Evaluate code sequentially on named devices."))
    kernel.print("  {:11s}  {}".format('', "--host executes on host (cPython)."))
    kernel.print("  {:11s}  {}".format('', "--all executes on all connected devices."))


@arg('level', nargs='?', default='INFO', const='INFO', choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="logging levels")
@arg('logger', nargs='?', help="name of logger to apply level to")
@line_magic
def loglevel_magic(kernel, args):
    """Set logging level.
Without arguments lists name and level of all available loggers.

Example:
    %loglevel device_registry INFO
    """
    if args.logger:
        logger = logging.getLogger(args.logger)
        logger.setLevel(args.level)
        for h in logging.getLogger().handlers:
            h.setLevel(args.level)
        kernel.print(f"Logger {args.logger} level set to {args.level}")
    else:
        fmt = "{:30}  {}"
        kernel.print(fmt.format('Logger', 'Level'))
        kernel.print('')
        colors = {
            'DEBUG': 'green',
            'INFO': 'blue',
            'WARNING': 'cyan',
            'ERROR': 'red',
            'CRITICAL': 'magenta',
        }
        for k, v in logging.root.manager.loggerDict.items():
            s = str(v)
            if '(' in s:
                level = fmt.format(k, s[s.find("(")+1:s.find(")")])
                kernel.print(level, colors.get(level.split(' ')[-1], 'grey'))
    # set global level
    # logging.basicConfig(level=args.level)
    # logger.setLevel(args.level)
    # logger.info("set logger level to '{}'".format(args.level))


if False:
    @arg('-v', '--verbose', action='store_true', help="also list hosts defined in $host_dir/config/hosts.py")
    @line_magic
    def config_magic(kernel, args):
        """Show kernel configuration and hosts
    Change configuration defaults in $IOT49/projects/config/config.py and
    assign host names in $IOT49/projects/config/devices.py.
    """
        for k, v in Config.get_config().items():
            doc = None
            if isinstance(v, dict):
                doc = v.get('doc')
                v = v.get('value')
            v = str(v)
            if len(v) > 60:  v = v[:80] + ' ...'
            kernel.print(colored(f"{k:20} {v}\n", 'blue'))
            if doc:
                kernel.print(f"{'':20} {colored(doc, 'green')}")

        if not args.verbose:
            return
        kernel.print("\nDevices:")
        devices = Config.get_config(file='devices.py').get('devices', {})
        for name, v in devices.items():
            if ':' in name: continue
            if isinstance(v, dict):
                uid = v.get('uid', name)
                projects = v.get('projects', '')
            kernel.print("{:15}\n    {}\n    {}\n".format(name, ', '.join(projects), uid))
