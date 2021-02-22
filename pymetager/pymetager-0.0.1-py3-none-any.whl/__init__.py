import os

from importlib.metadata import version

__module_dir__ = os.path.dirname(os.path.abspath(__file__))
__version__ = version(__name__)
