import requests
from typing import Dict, Type, TypeVar, get_type_hints, Callable
from xwire.rest._private.utils import deserialize, get_cookies

T = TypeVar('T')


def _do_post(url: str, json: Dict[str, str], return_class: Type[T], **kwargs) -> T:
    response = requests.post(url, json=json, timeout=5, **kwargs)
    if response.status_code >= 400:
        response.raise_for_status()
    elif return_class is not None:
        return deserialize(response.json(), return_class)
    else:
        return None


def post(path: str):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return_type = get_type_hints(func)['return']

        def wrapper(self, *args):
            url = self.base_url + self._proxy['_resource_path'] + path
            body = args[0]
            return _do_post(url, body.serialize(), return_type, cookies=get_cookies(self))

        return wrapper
    return decorator