from pathlib import Path
from typing import Union

import toml
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
    def from_toml_file(path: Union[Path, str]) -> 'RabbitConfig':
        if isinstance(path, str):
            path = Path(path)
        data = toml.load(path)['rabbit']
        return RabbitConfig.from_dict(data)

    @staticmethod
    def from_dict(dictionary: dict[str, any]) -> 'RabbitConfig':
        host = dictionary['host']
        port = int(dictionary['port'])
        exchange_name = dictionary['exchange_name']
        credentials = PlainCredentials(dictionary['user'], dictionary['pass'])
        return RabbitConfig(host, port, exchange_name, credentials)
