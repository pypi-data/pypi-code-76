"""
Task Object Storage module.

Note that this module has no Robot Framework
dependencies, i.e. can be used with pure
Python applications.
"""
import atexit

import pymongo

from tos.components import (
    creators,
    finders,
    setters,
    updaters,
)
from tos.settings import (
    DEFAULT_DB_ADDRESS,
)


class TaskObjectStorage(creators.TaskCreators,
                        finders.TaskFinders,
                        setters.TaskSetters,
                        updaters.TaskUpdaters):

    def __init__(self, **options):
        """
        :param options: A dictionary of MongoDB options for the
         database server URL and port, and the process database
         name, username and password.

        The following is a list of accepted options as keyword arguments:

        :param db_server: Mongodb server uri and optional port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str

        Example usage:

        .. code-block:: python

            tos = TaskObjectStorage(
                    db_server="localhost:27017",
                    db_name="testing",
                    db_auth_source="admin",
                    db_user="robo-user",
                    db_passw="secret-word",
            )
            tos.initialize_tos()

        where ``db_auth_source`` is the same as ``db_name`` by default.

        """
        self.options = options

        self.client = self.connect()
        self._check_connection_established(self.client)
        self.tos = None  # TOS collection
        atexit.register(self.disconnect)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to MongoDB.

        :returns: MongoDB client object.
        :rtype: pymongo.MongoClient
        """
        server = self.options.get("db_server") or DEFAULT_DB_ADDRESS
        # conn_string = (
        #     f"mongodb+srv://"
        #     f'{self.options["db_user"]}'
        #     f':{self.options["db_passw"]}'
        #     f'@{server}'
        # )
        if self.options.get("db_passw"):
            client = pymongo.MongoClient(
                host=server,
                authSource=self.options.get("db_auth_source") or self.options["db_name"],
                authMechanism="SCRAM-SHA-1",
                username=self.options["db_user"],
                password=self.options["db_passw"],
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )
        else:
            client = pymongo.MongoClient(
                host=server,
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )

        return client

    def disconnect(self):
        self.client.close()

    def _check_connection_established(self, client):
        """Get active nodes (DB servers).

        :raises: ServerSelectionTimeoutError if no
                 connections active.
        """
        try:
            return client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            raise Exception("Is MongoDB running?") from err

    def initialize_tos(self):
        """Initialize Mongo database and collection objects."""
        database = self.client[self.options["db_name"]]
        self.tos = database["task_objects"]
