"""
    CONFIG UTILITIES
        - classes that parse your config file, build a query iterable and yield queries
"""
import yaml


# pylint: disable=invalid-name, unused-argument
def _generate_queries(query_config: list):
    """
    args:
        queryConfig (list): SailThru query config containing endpoint, parameters, etc.
    yields:
        query generator of queries to run
    """
    for config in query_config:
        endpoint = config.get('endpoint', None)
        if endpoint is None:
            raise Exception('ClientError: Expected parameter endpoint.')

        parameters = config.get('parameters', None)
        if endpoint is None:
            raise Exception('ClientError: Expected parameters.')

        fields = {
            "endpoint": endpoint,
            "parameters": parameters}
        # building similar queries per vid
        yield [fields]


def _parser(file_name: str) -> list:
    """Parse config in to dictionary"""
    # load config
    with open(file_name, 'r') as file_:
        config = yaml.safe_load(file_)

    return config.get('queryConfig')


# pylint: disable=too-few-public-methods
class SailThruConfigManager:
    """
        Class that parses config .yaml for queries, reader, writer
        Uses these configs to build required query objects.
    """

    def __init__(self, file_name):
        # load config
        self.config = _parser(file_name=file_name)

    def get_query(self, config=None):
        """
        Gets the query parameters from the config file
        :param config: configurations
        :return: query parameters
        """
        if config is None:
            config = self.config

        return _generate_queries(config)
