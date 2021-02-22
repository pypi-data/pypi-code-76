import logging
from logging import NullHandler

__title__ = "lilili"
__description__ = "List the Licenses of the Libraries."
__url__ = "https://github.com/poyo46/lilili"
__version__ = "0.1.0"
__author__ = "poyo46"
__author_email__ = "poyo4rock@gmail.com"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021 poyo46"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
