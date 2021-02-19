# encoding: utf-8
"""
Klity class used to process each test.
"""

import os

import psycopg2
import yaml


def postgresql_connect(configuration):
    """
    Opening connection to postgresql database.
    """
    # Default values
    if "host" not in configuration or configuration["host"] == "":
        configuration["host"] = "127.0.0.1"
    if "port" not in configuration or configuration["port"] == "":
        configuration["port"] = 5432
    # Connection to database
    return {
        "type": "postgresql",
        "connection": psycopg2.connect(
            host=configuration["host"],
            port=configuration["port"],
            database=configuration["database"],
            user=configuration["user"],
            password=configuration["password"],
        ),
    }


def postgresql_execute(connection, request, parameters):
    result = None
    cursor = connection["connection"].cursor()
    cursor.execute(request, parameters)
    result = {
        "columns": [],
        "query": cursor.query,
        "rowcount": cursor.rowcount,
        "lastrowid": cursor.lastrowid,
        "results": [],
    }
    try:
        result["columns"] = [column[0] for column in cursor.description]
        result["results"] = cursor.fetchall()
    except:
        # No result to fetch...
        pass
    connection["connection"].commit()
    cursor.close()
    return result


def postgresql_close(connection):
    connection["connection"].close()


class Klity:
    def __init__(self, args=None):
        # Default configuration
        self.configuration = {
            "behave": {"lang": "fr",},
            "databases": [],
            "variables": [],
        }
        # Specific configuration
        try:
            with open(os.path.join(os.getcwd(), "configuration.yml")) as f:
                self.configuration.update(yaml.load(f, Loader=yaml.SafeLoader))
        except FileNotFoundError:
            # No specific config
            pass

        # Session variables
        self.variables = {}
        # Requests
        self.connections = {}
        self.requests = {}

    def before_feature(self, context, feature):
        # Loading available requests for this specific feature
        self.load_requests(feature.filename)

    def after_feature(self, context, feature):
        # Cleaning connections after feature, if necessary
        for connection in self.connections:
            if self.connections[connection]["type"].lower() == "postgresql":
                return postgresql_close(self.connections[connection])

    def before_scenario(self, context, feature):
        # Before each scenario, session is cleaned
        self.session = {}
        # Loading global variables
        self.variables = {}
        for variable in self.configuration["variables"]:
            self.variables[variable] = self.configuration["variables"][variable]

    def after_scenario(self, context, feature):
        # Before each scenario, session and variables are cleaned
        self.session = {}
        self.variables = {}

    def load_requests(self, feature_file):
        self.requests = {}
        # Loading requests
        feature_path = os.path.join(
            os.getcwd(), os.path.dirname(feature_file).replace("/", os.path.sep)
        )
        feature_name = os.path.basename(feature_file)
        if feature_name.endswith(".setup.feature"):
            size = 14
        elif feature_name.endswith(".teardown.feature"):
            size = 17
        else:
            size = 8
        request_file = os.path.join(feature_path, feature_name[:-size] + ".sql")
        if not os.path.exists(request_file):
            return
        with open(request_file) as f:
            requests = yaml.load(f, Loader=yaml.SafeLoader)
        for request in requests["requests"]:
            if isinstance(request, str):
                request_object = requests["requests"][request]
                self.requests[request] = request_object
            else:
                key = str(len(self.requests))
                self.requests[key] = request
        # Connecting to database if necessary
        for request in self.requests:
            self.connect(self.requests[request]["config"])

    def connect(self, connection):
        if connection not in self.connections:
            configuration = self.configuration["databases"][connection]
            if configuration["type"].lower() == "postgresql":
                self.connections[connection] = postgresql_connect(configuration)

    def execute(self, request, parameters=None):
        connection = self.connections[self.requests[request]["config"]]
        if connection["type"].lower() == "postgresql":
            return postgresql_execute(
                connection, self.requests[request]["request"], parameters
            )
