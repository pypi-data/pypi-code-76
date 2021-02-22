"""Settings and variables for TOS."""
import os
import platform


DIRNAME = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
PLATFORM = platform.system()

#:
DEFAULT_DB_ADDRESS = "mongodb://localhost:27017/"
