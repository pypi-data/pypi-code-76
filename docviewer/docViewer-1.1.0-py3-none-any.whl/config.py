import logging
import os
import tempfile

from p_config import Config

CURRENT_DIR = os.path.abspath(os.path.curdir)

default_config = {
    'cache_root': tempfile.mktemp(prefix='docViewer/'),
    'plantuml.server': 'https://www.plantuml.com/plantuml/',
    'plantuml.image_format': 'svg',
    'logging.level': logging.WARNING,
}
CONFIG = Config(**default_config)

config_files = [
    os.path.abspath(os.path.expanduser('~/.config/docViewer.yaml')),
    os.path.join(CURRENT_DIR, 'docViewer.yaml')
]
for config_file in config_files:
    if os.path.exists(config_file):
        CONFIG.load(config_file)
