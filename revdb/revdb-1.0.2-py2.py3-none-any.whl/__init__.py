"""a light layer for revtel mongodb"""

__version__ = "1.0.2"

from revdb.db import connect, connect_v2, make_model_class

__all__ = ["make_model_class", "connect", "connect_v2"]
