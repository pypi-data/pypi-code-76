"""neatlog: A neat logging configuration

LICENSE
   MIT (https://mit-license.org/)

COPYRIGHT
   © 2020 Steffen Brinkmann <s-b@mailbox.org>
"""

__version__ = "0.1.8"

from .log_decorator import log  # noqa: F401
from .log_fmt import (config_logger, file_handler, set_log_level,  # noqa: F401
                      stream_handler)
