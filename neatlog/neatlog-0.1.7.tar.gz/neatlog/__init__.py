"""neatlog: A neat logging configuration

LICENSE
   MIT (https://mit-license.org/)

COPYRIGHT
   © 2020 Steffen Brinkmann <s-b@mailbox.org>
"""

__version__ = "0.1.7"

from .log_fmt import (  # noqa: F401
    config_logger,
    set_log_level,
    stream_handler,
    file_handler,
)

from .log_decorator import log  # noqa: F401
