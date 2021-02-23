from typing import TypeVar, Type

T = TypeVar('T')


def resource(resource_path: str):
    def decorator(cls: Type[T]) -> Type[T]:
        cls._proxy = {
            '_resource_path':  resource_path,
            '_cookies': None
        }
        return cls
    return decorator

