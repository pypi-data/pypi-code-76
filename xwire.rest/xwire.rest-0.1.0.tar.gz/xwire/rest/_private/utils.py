import inspect
from typing import Type, TypeVar, Dict, Callable

T = TypeVar('T')


def deserialize(json, clazz: Type[T]) -> T:
    if isinstance(json, list):
        return clazz(*json)
    else:
        return clazz(**json)


def get_cookies(self) -> Dict[str, str]:
    cookies_method: Callable[..., Dict[str, str]] = self._proxy['_cookies']
    if cookies_method is None:
        methods = inspect.getmembers(self, inspect.ismethod)
        for _, method in methods:
            if hasattr(method, '__proxy_cookies'):
                cookies_method = method
                self._proxy['_cookies'] = cookies_method
                return cookies_method()
        return {}
    else:
        return cookies_method()
