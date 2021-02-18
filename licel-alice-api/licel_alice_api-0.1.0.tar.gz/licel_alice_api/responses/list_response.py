from typing import TypeVar, Generic, Callable

from .status_response import StatusResponse
from ..utils import dict_prop, DictListWrapper

T = TypeVar("T")


class ListResponse(StatusResponse, Generic[T]):
    _item_wrapper: Callable[[dict], T] = None
    size: int = dict_prop()
    list: DictListWrapper[T] = dict_prop(is_list=True, wrapper_attr="_item_wrapper")

    def __init__(self, response: dict, item_wrapper: Callable[[dict], T] = None):
        super().__init__(response)
        self._item_wrapper = item_wrapper
