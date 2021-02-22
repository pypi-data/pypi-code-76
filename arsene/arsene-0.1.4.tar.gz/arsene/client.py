from functools import wraps
from typing import Dict, List, Tuple, Optional, Union
from arsene.schemas.redis import RedisModel
from arsene.key_builder import generate_key
from arsene.exceptions import ValidationBroker
from arsene.logger import logger


class Arsene():
    def __init__(
        self, *, redis_connection: Optional[RedisModel] = None,
        global_expire: Optional[int] = None
    ):
        self.global_expire = global_expire
        self.redis_connection = redis_connection
        self.store = self.create_store()

    def create_store(self):
        if self.redis_connection:
            store = self.redis_conn()
        else:
            raise ValidationBroker
        return store

    def redis_conn(self):
        from arsene.connection import RedisConnection
        r = RedisConnection(
            host=self.redis_connection.host
        )
        r.test_connection()
        return r

    def set(self, *, key: str, expire: Optional[int] = None, data: Union[
        str, int, Dict, List, float,
        bytes, Tuple
    ]):
        ex = expire if expire else self.global_expire
        self.store.set(key=key, expire=ex, data=data)

    def get(self, *, key: str):
        return self.store.get(key=key)

    def delete(self, *, key: str):
        return self.store.delete(key=key)

    def clean_key(self, *, key: str):
        self.delete(key=key)

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def cache(
        self, *, key: str, expire: Optional[int] = None, check_params: bool = False,
        kwargs_list: Optional[List] = None, check_args_params: bool = False,
        check_kwargs_params: bool = False
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = generate_key(
                    key=key, args=args, kwargs=kwargs,
                    kwargs_list=kwargs_list, check_params=check_params,
                    check_args_params=check_args_params,
                    check_kwargs_params=check_kwargs_params
                )
                key_data = self.get(key=name)
                if key_data:
                    logger.info(f'Find key data {name}')
                    return key_data
                elif key_data is None:
                    logger.info(f'Save key data {name}')
                    ex = expire if expire else self.global_expire
                    response = func(*args, **kwargs)
                    self.set(key=name, data=response, expire=ex)
                    return response
            return wrapper
        return decorator
