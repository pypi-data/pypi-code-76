"""
Utility Functions
=================


"""
import logging
import os
from argparse import Namespace

import yaml

logger = logging.getLogger(__name__)


def validate_folder(folder: str) -> None:
    """Validate target folder exists, if not exist, an empty folder will be created.

    :param folder: folder path
    """
    if os.path.isfile(folder):
        raise FileExistsError("Target folder path exists by file")
    os.makedirs(os.path.abspath(folder), exist_ok=True)


def set_log(level: str = 'info') -> None:
    """Set Logger level

    :param level: info|warn|error|critical etc.
    """
    try:
        level = getattr(logging, level.upper())
    except AttributeError:
        level = logging.INFO
        print("Logging level (%s) not match, use default level (info)" % level)

    logging.basicConfig(level=level,
                        format='%(name)-25s:%(funcName)20s: %(levelname)-8s: %(message)s')


def load_yaml_namespace(filename: str) -> Namespace:
    """Load YAML config into a Namespace object

    :param filename: YAML file
    :return: Namespace object that attributes are accessible directly
    """
    config = yaml.safe_load(open(filename))
    return Namespace(**config)
