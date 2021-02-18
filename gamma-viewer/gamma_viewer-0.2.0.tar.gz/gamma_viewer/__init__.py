"""Initialize jupyter nb extension path."""
from .gamma_viewer import *


def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'gamma_viewer',
        'require': 'gamma_viewer/extension'
    }]
