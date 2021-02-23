import configparser
from pathlib import Path
from typing import Union

import yaml
from pika import PlainCredentials, ConnectionParameters


class RabbitConfig:

    def __init__(self,
                 host: str,
                 port: int,
                 exchange_name: str,
                 credentials: PlainCredentials) -> None:
        self.host = host
        self.port = port
        self.exchange_name: str = exchange_name
        self.credentials = credentials
        self.params = ConnectionParameters(host, port, '/', self.credentials)

    @staticmethod
    def from_yaml_file(path: Union[Path, str]) -> 'RabbitConfig':
        if isinstance(path, str):
            path = Path(path)
        data = yaml.safe_load(path.read_text())
        return RabbitConfig._from_dict(data)

    @staticmethod
    def from_ini_file(path: Union[Path, str]) -> 'RabbitConfig':
        if isinstance(path, str):
            path = Path(path)
        config = configparser.ConfigParser()
        config.read(path)
        rabbit_config = config['rabbit']
        return RabbitConfig._from_dict(rabbit_config)

    @staticmethod
    def _from_dict(
            dictionary: Union[dict[str, any], configparser.SectionProxy]
    ) -> 'RabbitConfig':
        host = dictionary['host']
        port = int(dictionary['port'])
        exchange_name = dictionary['exchange_name']
        credentials = PlainCredentials(dictionary['user'], dictionary['pass'])
        return RabbitConfig(host, port, exchange_name, credentials)
