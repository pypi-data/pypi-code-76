"""dora cli
Usage:
    dora configure [--provider <cloud>] [--debug] [--show]
    dora start [--image <docker-image>] [--debug]
    dora filesystem [ls] [--debug]
    dora storage [ls] [--debug]
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

arguments = docopt(__doc__, version='0.0.5')
# Enable debug messages
if arguments['--debug']:
    logger.setLevel(getattr(logging,'DEBUG'))
# Load configuration file
logger.debug(arguments)
_config = configure.get_config()
if _config == dict():
    _config = configure.setup(None)
if _config.get('provider') == 'hwc':
    from dora_cli import hwc as provider_cli
if _config.get('provider') == 'aws':
    from dora_cli import aws as provider_cli

# "configure" option
if arguments['configure']:
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
    try:
        puts(colored.green("STARTING..."))
        container = provider_cli.start(_config, arguments)
        puts(colored.green(f"{container.name}:{container.status}"))
    except Exception as err:
        puts(colored.red("ERROR"))
        logger.error(err)

# "OBS" option
if arguments['storage']:
    puts(colored.cyan("Object Storage"))
    if arguments['ls']:
        bkt_list = provider_cli.list_buckets(
            access_key=_config['credentials']['access_key'],
            secret_key=_config['credentials']['secret_key'],
            region_key=_config['credentials']['region_key'])
        logger.debug(bkt_list)
        for bkt in bkt_list:
            if bkt['return']==_config['storages']['bucket_name']:
                puts(colored.cyan(f"> {bkt['prompt']}"))
                continue
            puts(colored.cyan(f"  {bkt['prompt']}"))
        sys.exit()

# "SFS" option
if arguments['filesystem']:
    puts(colored.cyan("File Service"))
    if arguments['ls']:
        fs_list = provider_cli.list_fs(_config)
        logger.debug(fs_list)
        sys.exit()
