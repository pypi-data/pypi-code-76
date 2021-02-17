"""dora cli
Usage:
    dora configure [--provider <cloud>] [--debug] [--show]
    dora start [--image <docker-image>] [--debug]
    dora -h|--help
    dora --version

Options:
    --help          User guide.
    --version       Show version.
    --debug         Show debug messages
    --provider      Cloud provider.
    --show          Show information.
    <cloud>         Supports: hwc or aws.
    <docker-image>  Docker image name.
"""
import logging
import sys
from clint.textui import puts
from clint.textui import colored
from docopt import docopt
from dora_cli import logger
from dora_cli import config as configure

arguments = docopt(__doc__, version='0.0.2')
# Enable debug messages
if arguments['--debug']:
    logger.setLevel(getattr(logging,'DEBUG'))
logger.debug(arguments)
# "configure" option
if arguments['configure']:
    _config = configure.get_config()
    logger.debug("CONFIG:LOADED:%s", _config)
    # Show configuration file
    if arguments['--show']:
        puts(colored.green(configure.show(_config)))
        sys.exit()
    # Setup configuration file
    else:
        _config = configure.setup(_config, provider=arguments['<cloud>'])
        logger.debug("CONFIG:SETUP:%s", _config)
# "start" option
if arguments['start']:
    _config = configure.get_config()
    if _config == dict():
        _config = configure.setup(None, provider=arguments['<cloud>'])
    if _config.get('provider') == 'hwc':
        from dora_cli import hwc as provider_cli
    if _config.get('provider') == 'aws':
        from dora_cli import aws as provider_cli
    try:
        puts(colored.green("STARTING..."))
        container = provider_cli.start(_config, arguments)
        puts(colored.green(f"{container.name}:{container.status}"))
    except Exception as err:
        puts(colored.red("ERROR"))
        logger.error(err)
