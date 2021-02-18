
try:
    from tempfile import TemporaryDirectory as TD
except ImportError:
    from backports.tempfile import TemporaryDirectory as TD

try:
    from unittest.mock import Mock as Mk
except ImportError:
    from mock import Mock as Mk

TemporaryDirectory = TD
Mock = Mk

INFINITY = float("inf")
