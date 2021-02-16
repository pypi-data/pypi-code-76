# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import logging
from sys import exit as s_exit
from pathlib import Path
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from .parse_args import args

logger = logging.getLogger(__name__)

# CONFIG = ConfigParser()
CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
CONFIG.optionxform = lambda option: option

def load_config():
    """Reload configuration from disk.

    Config locations, by priority (first one wins)
    """
    files = []
    if args.config is not None:
        if not Path(args.config).exists():
            logger.error(F"Cannot file specified config file: {args.config}")
            s_exit(3)
        files += [ Path(args.config) ]

    logger.info("reading config")

    files += [
        Path('./regapp-tools.conf'),
        Path(Path.home(),'.config','regapp-tools.conf'),
        Path('/etc/regapp-tools.conf')
    ]

    read_a_config = False
    for f in files:
        try:
            if f.exists():
                logger.info("Using this config file: {}".format(f))
                CONFIG.read(f)
                read_a_config = True
                break
        except PermissionError:
            pass
    if not read_a_config:
        logger.error(F"Could not read any config file from {files}")
        s_exit(4)

def test_config():
    try:
        delme = CONFIG['backend.bwidm']['url']
        delme = CONFIG['backend.bwidm']['org_id']
        delme = CONFIG['backend.bwidm.auth']['http_user']
        delme = CONFIG['backend.bwidm.auth']['http_pass']
    except KeyError as e:
        logging.error(F"Cannot find required config entry: {e}")
        s_exit(3)

load_config()
test_config()
