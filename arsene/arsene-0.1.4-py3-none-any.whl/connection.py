from json import loads
from typing import Optional, Callable
from redis import Redis
from .data_convert import (
    set_data, resolve_data,
    object_hook, date_serial
)


class RedisConnection():
    def __init__(
        self, *, host: str, port: int = 6379,
        db=0, password: str = None,
        socket_connect_timeout: int = 1,
        set_data: Callable = set_data,
        resolve_data: Callable = resolve_data,
        object_hook: Callable = object_hook,
        json_serial: Callable = date_serial
    ):
        self.db = db
        self.host = host
        self.port = port
        self.status = False
        self.password = password
        self.set_data = set_data
        self.object_hook = object_hook
        self.json_serial = json_serial
        self.resolve_data = resolve_data
        self.socket_connect_timeout = socket_connect_timeout
        self.client = self.create_client()

    def create_client(self):
        return Redis(
            host=self.host, port=self.port, db=self.db, password=self.password,
            socket_connect_timeout=self.socket_connect_timeout
        )

    def test_connection(self):
        self.client.ping()
        self.status = True

    def set(self, *, key: str, expire: Optional[int] = None, data):
        data_convert = self.set_data(
            data, serializable=self.json_serial
        )
        self.client.set(key, data_convert, ex=expire)

    def get(self, *, key: str):
        if not self.client.get(key):
            return None

        data_convert = self.client.get(key).decode('utf-8')
        data_json = loads(data_convert)
        return self.resolve_data(
            data_json, object_hook=self.object_hook
        )

    def delete(self, *, key: str):
        self.client.delete(key)
