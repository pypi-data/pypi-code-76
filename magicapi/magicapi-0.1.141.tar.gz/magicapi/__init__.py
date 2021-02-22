__version__ = "0.1.0"

"""Imports the Routes and the app and glues them all together"""
# from .config import settings
from magicapi.Globals.G import g

from magicapi.app_factory import (
    create_app,
    create_handler,
    add_magic_routers,
    use_route_names_as_operation_ids,
)
