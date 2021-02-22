from dataclasses import dataclass, fields
from typing import TypeVar, Type, Dict, Any, Callable

from xwire.common import decorator_utils

T = TypeVar('T')


def _compile_metadata(instance: T) -> Dict[str, Any]:
    return {
        'fields': {field.name: getattr(instance, field.name) for field in fields(instance)}
    }


def _wrap_init(init_fn: Callable[..., None]) -> Callable[..., None]:
    def wrapper(self: T, *args, **kwargs) -> None:
        init_fn(self, *args, **kwargs)
        decorator_utils.set_decorator_metadata(self, serializable, _compile_metadata(self))

    return wrapper


def serializable(cls: Type[T]) -> Type[T]:
    data_class = dataclass(cls)
    data_class.__init__ = _wrap_init(data_class.__init__)
    decorator_utils.set_decorator_metadata(data_class, serializable, {})

    return data_class
