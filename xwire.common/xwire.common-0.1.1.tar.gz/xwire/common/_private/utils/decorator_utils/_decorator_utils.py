from typing import Any, Callable, Dict, Union
from xwire.common._private.utils import symbols


def has_decorator(obj: Any, decorator: Callable[..., Any]) -> bool:
    decorator_key = f'__{decorator.__name__}'
    return hasattr(obj, symbols.XWIRE) and decorator_key in getattr(obj, symbols.XWIRE)


def get_decorator_metadata(obj: Any, decorator: Callable[..., Any]) -> Union[Dict[str, Any], None]:
    if not has_decorator(obj, decorator):
        return None

    serializable_key = f'__{decorator.__name__}'
    return getattr(obj, symbols.XWIRE)[serializable_key]


def set_decorator_metadata(obj: Any, decorator: Callable[..., Any], data: Dict[str, Any]) -> None:
    decorator_key = f'__{decorator.__name__}'
    setattr(obj, symbols.XWIRE, {decorator_key: data})

