from pkg_resources import DistributionNotFound, get_distribution


try:
    __version__ = get_distribution("coveragespace").version
except DistributionNotFound:  # pragma: no cover
    __version__ = "(local)"

CLI = "coveragespace"
API = "https://api.coverage.space"

VERSION = "{0} v{1}".format(CLI, __version__)
