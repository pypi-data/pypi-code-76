# import os, sys
# DIRNAME = os.path.dirname(os.path.abspath(__file__))
# PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
# sys.path.append(PACKAGE_ROOT)

from tos.task_object_storage import TaskObjectStorage
from .dynamic_library import DynamicLibrary


class TOSLibrary(DynamicLibrary):
    """Robot Framework layer for TOS."""

    def __init__(self, db_server, db_name, db_user="", db_passw="", db_auth_source=""):
        """
        Initialize the MongoDB client and collection.

        Register the methods inside ``tos.TaskObjectStorage`` as
        ``TOSLibrary`` keywords.

        :param db_server: Mongodb server uri and port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str
        """
        super(TOSLibrary, self).__init__()
        self.tos = TaskObjectStorage(
            db_server=db_server,
            db_name=db_name,
            db_user=db_user,
            db_passw=db_passw,
            db_auth_source=db_auth_source,
        )
        self.tos.initialize_tos()

        self.add_component(self.tos)
